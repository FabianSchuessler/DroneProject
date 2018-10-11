#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


if __name__ == "__main__":
	from agent import Agent
else:
	from .agent import Agent
import sys, os, time, threading

# mavparse is used to get the message structure
import pymavlink.generator.mavparse as mavparse

# babeltrace is used for creating the traces
import babeltrace
from babeltrace import CTFWriter as btw

class Silencer(object):
	"""A context handler for temporary voiding anything sent to stdout"""
	def __enter__(self):
		self.realstdout = sys.stdout
		sys.stdout = open("/dev/null","w")
	
	def __exit__(self,*args):
		sys.stdout = self.realstdout


class CTFWriter(Agent):
	def __init__(self, message_definition_path, trace_path, protocol_version = "2.0"):
		super(CTFWriter, self).__init__()
		self.xmls = []
		self.streams = {}
		self.load_message_definition_xml(message_definition_path, protocol_version)
		self.init_babeltrace(trace_path)
		self.init_events()
		self.acceptlock = threading.Lock()

	def load_message_definition_xml(self, message_definition_path, protocol_version):
		with Silencer():
			xml = mavparse.MAVXML(message_definition_path,protocol_version)
			
		for include in xml.include:
			include_path = os.path.join(os.path.dirname(message_definition_path),include)
			self.load_message_definition_xml(include_path, protocol_version)
		self.xmls.append(xml)

	def init_babeltrace(self, trace_path):
		# directory holding the CTF trace
		print('trace path: {}'.format(trace_path))
		self.writer = btw.Writer(trace_path)

		self.clock = btw.Clock('my_clock')
		self.clock.description = 'this is my clock'
		self.writer.add_clock(self.clock)


		self.stream_class = btw.StreamClass('my_stream')
		self.stream_class.clock = self.clock

		def new_int_field_decl(signed,bit):
			# n-bit [un]signed integer field declaration
			field_decl = btw.IntegerFieldDeclaration(bit)
			field_decl.signed = signed
			field_decl.base = btw.IntegerFieldDeclaration.IntegerBase.INTEGER_BASE_HEXADECIMAL
			return field_decl

		# char field declaration
		char_field_decl = new_int_field_decl(False, 8)
		char_field_decl.encoding = babeltrace.CTFStringEncoding.ASCII

		# IEEE 754 single precision floating point number field declaration
		float_field_decl = btw.FloatFieldDeclaration()
		float_field_decl.exponent_digits = btw.FloatFieldDeclaration.FLT_EXP_DIG
		float_field_decl.mantissa_digits = btw.FloatFieldDeclaration.FLT_MANT_DIG


		"""
		# string field declaration
		string_field_decl = btw.StringFieldDeclaration()
		string_field_decl.encoding = babeltrace.CTFStringEncoding.UTF8
		"""

		self.field_declarations = {
			'float'    : float_field_decl,
			#'double'   : None,
			'char'     : char_field_decl,
			'int8_t'   : new_int_field_decl(signed=True,  bit= 8),
			'uint8_t'  : new_int_field_decl(signed=False, bit= 8),
			#'uint8_t_mavlink_version'  : None, #special mavlink datatype that gets automatically filled when sending mavlink packages, for reading it's just a normal uint8_t
			'int16_t'  : new_int_field_decl(signed=True,  bit=16),
			'uint16_t' : new_int_field_decl(signed=False, bit=16),
			'int32_t'  : new_int_field_decl(signed=True,  bit=32),
			'uint32_t' : new_int_field_decl(signed=False, bit=32),
			'int64_t'  : new_int_field_decl(signed=True,  bit=64),
			'uint64_t' : new_int_field_decl(signed=False, bit=64),
			}

	def init_events(self):
		enums = {}
		self.events = {}
		for xml in self.xmls:
			# create enums
			for enum in xml.enum:
				# enumeration field declaration (based on the 5-bit unsigned integer above)
				enum_field_decl = btw.EnumerationFieldDeclaration(self.field_declarations["uint32_t"])
				for entry in enum.entry:
					enum_field_decl.add_mapping(entry.name, entry.value, entry.value)
					#enum_field_decl.add_mapping('DAZED', 3, 11)
				enums[enum.name] = enum_field_decl

			# create events
			for message in xml.message:
				#if message.name != "HEARTBEAT": #only try with heartbeat message for now
				#	continue
				event_class = btw.EventClass(message.name)
				for field in message.fields:
					if field.enum:
						field_decl = enums[field.enum]
					else:
						field_decl = self.field_declarations[field.type]
					if field.array_length:
						field_decl = btw.ArrayFieldDeclaration(field_decl, field.array_length)
					event_class.add_field(field_decl, field.name)
				self.stream_class.add_event_class(event_class)
				self.events[message.name] = event_class

	def accept(self, msg):
		with self.acceptlock:
			# get some metadata
			source = getattr(msg, "source", "default")
			self.clock.time = timestamp = getattr(msg, "timestamp", int(round(time.time()*1000000)))
			msgname = msg['mavpackettype']
			
			# create event
			if msgname not in self.events:
				print("encountered undefined message %s" %msgname)
				return
			event = btw.Event(self.events[msgname])
			for field, value in msg.items():
				if field == 'mavpackettype':
					continue
				try:
					payload = event.payload(field)
				except:
					print("Some extensions seem to be enabled, while others aren't?!... ignoring additional values")
					continue
				if isinstance(payload, btw.EnumerationField):
					payload.container.value = value
				elif isinstance(payload, btw.ArrayField):
					if isinstance(value, str):
						i = -1
						for i,v in enumerate(value):
							payload.field(i).value = ord(v)
						try:
							while True:
								i = i+1
								payload.field(i).value = 0
						except IndexError:
							pass
					else:
						for i,v in enumerate(value):
							payload.field(i).value = v
				else:
					payload.value = value
			
			# if necessary create stream
			if source not in self.streams:
				self.streams[source] = self.writer.create_stream(self.stream_class)
				self.writer.flush_metadata()
				print("created stream %s" % source)
			stream = self.streams[source]
			
			# append event and flush
			try:
				stream.append_event(event)
			except:
				print("May be due to wrong protocol version (therefore enabled or disabled extensions -> mismatch in available/required fields)")
				raise
			#stream.flush() #makes connection not work for some reason I couldn't figure out
		
		def flush():
			for stream in self.streams.values():
				stream.flush()

################################################################################

if __name__ == "__main__":
	import ast
	
	class myDict(dict):
		pass

	class LogReader(Agent):
		def __init__(self, log_path):
			super(LogReader, self).__init__()
			self.log_path = log_path
		
		def read(self):
			with open(self.log_path,"r") as logfile:
				logstring = logfile.read()
				logstring = logstring.replace("defaultdict(<class 'list'>,","(")
				log = ast.literal_eval(logstring)
			my_messages = []
			for src, messages in log["messages"].items():
				for timestamp, msg in messages:
					if isinstance(msg, str):
						msg = ast.literal_eval(msg)
					msg = myDict(msg)
					msg.timestamp = int(round(timestamp*1000000))
					msg.source = src
					my_messages.append(msg)
			my_messages.sort(key=lambda msg: msg.timestamp)
			for msg in my_messages:
				self.emit(msg)

	sys.path.append("..")
	import agents

	message_definition_path = "../message_definitions/v1.0/ardupilotmega.xml"
	trace_path = "../ctf_trace"
	log_path = "../log.txt"

	logReader = LogReader(log_path)
	#messageAssembler = agents.MessageAssembler()
	#messageDecoder = agents.MessageDecoder()
	ctfWriter = CTFWriter(message_definition_path, trace_path)
	
	#logReader.send_output_to(messageAssembler)
	#messageAssembler.send_output_to(messageDecoder)
	#messageDecoder.send_output_to(ctfWriter)
	
	logReader.send_output_to(ctfWriter)
	
	logReader.read()
