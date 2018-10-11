#! /usr/bin/env python3
#* encoding: utf-8 *#

"""
(c) 2018 Joram Brenz
joram.brenz@online.de

THIS IS A LAST MINUTE SCRIPT, IT MAY CONTAIN REALLY BAD CODE STRUCTURE AND ALMOST NO DOCUMENTATION. YOU HAVE BEEN WARNED!

some parts where taken from the following dronekit example:

	© Copyright 2015-2016, 3D Robotics.
	simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

	Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.

	Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

import sys, ast, math
import time
import threading
import dronekit

# Move this somewhere else :/
import combiserver
HTTP_PORT = 8000
WEBSOCKET_PORT = 9001
#UAV_BASE_PORT = 14550
UAV_BASE_PORT = 24550
print("serving at ports", HTTP_PORT, WEBSOCKET_PORT)
server = combiserver.CombiServer(HTTP_PORT,WEBSOCKET_PORT)


def arm_and_takeoff(vehicle, aTargetAltitude):
	"""
	Arms vehicle and fly to aTargetAltitude.
	"""

	print("Vehicle %i: Basic pre-arm checks" % vehicle.instance_index)
	# Don't try to arm until autopilot is ready
	print("Vehicle %i: Waiting for vehicle to initialise..."  % vehicle.instance_index)
	while not vehicle.is_armable:
		time.sleep(1)

	print("Vehicle %i: Arming motors" % vehicle.instance_index)
	# Copter should arm in GUIDED mode
	vehicle.mode = dronekit.VehicleMode("GUIDED")
	vehicle.armed = True    

	# Confirm vehicle armed before attempting to take off
	print("Vehicle %i: Waiting for arming..." % vehicle.instance_index)
	while not vehicle.armed:      
		time.sleep(1)

	print("Vehicle %i: Taking off!" % vehicle.instance_index)
	vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

	# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
	#  after Vehicle.simple_takeoff will execute immediately).
	while True:
		print("Vehicle %i: Altitude: " % vehicle.instance_index, vehicle.location.global_relative_frame.alt)
		#Break and return from function just below target altitude.        
		if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
			print("Vehicle %i: Reached target altitude" % vehicle.instance_index)
			break
		time.sleep(1)

	print("Vehicle %i: Set default/target airspeed to 5" % vehicle.instance_index)
	vehicle.airspeed = 5

def do_for_all(vehicles, function):
	threads = [threading.Thread(target=lambda v=v:function(v)) for v in vehicles]
	for t in threads:
		t.start()
	for t in threads:
		t.join()


def position_tracker(vehicle):
	while True:
		position = [vehicle.location.global_frame.lat, vehicle.location.global_frame.lon]
		vehicle_id = vehicle.instance_index
		#print (vehicle, position)
		server.send_message_to_all(repr([vehicle_id,position]))
		time.sleep(0.1)

undistributed_lines = []

# Called when a client sends a message
def message_received(client, server, message):
	""" adding new lines that user draw on map """
	lines = ast.literal_eval(message)
	lines = [[dronekit.LocationGlobal(point["lat"],point["lng"],20) for point in line] for line in lines]
	undistributed_lines.extend(lines)
server.set_fn_message_received(message_received)

"""
Prepare:
"""

instance_count = int(sys.argv[1]) # script expects one command line argument which is the instance count

vehicles = []

for instance_index in range(instance_count):
	port = UAV_BASE_PORT + 10 * instance_index

	connection_string = "127.0.0.1:%i" % port #connect to port on localhost

	# Connect to the Vehicle
	print('Connecting to vehicle %i on: %s' % (instance_index, connection_string))
	for _ in range(60):
		try:
			vehicle = dronekit.connect(connection_string, wait_ready=True)
		except Exception as e:
			print(e)
			time.sleep(1)
		else:
			vehicle.instance_index = instance_index
			vehicle.nextlocations = []
			
			vehicles.append(vehicle)
			break

print(vehicles)

do_for_all(vehicles, lambda v:arm_and_takeoff(v, 10))

position_tracker_threads = []
for vehicle in vehicles:
	t = threading.Thread(target=lambda:position_tracker(vehicle))
	t.daemon = True
	t.start()
	position_tracker_threads.append(t)

"""
This is where the main stuff happens:
"""

def distance(location1, location2):
	(x1,y1) = location1.lat, location1.lon
	(x2,y2) = location2.lat, location2.lon
	try:
		d = math.acos(math.sin(math.radians(x1))*math.sin(math.radians(x2)) + math.cos(math.radians(x1))*math.cos(math.radians(x2))*math.cos(math.radians(y2-y1)))*6378.137
	except ValueError:
		print("ValueError in distance calculation for ", x1,y1, "to", x2,y2)
		d = 0.0
	return d

def isnear(location1, location2):
	return distance(location1, location2) < 0.001 # this could be done better with some time series analysis etc. but for the simulation a hardcoded value is good enough

def distribute_tasks(free_vehicles, undistributed_lines):
	while free_vehicles and undistributed_lines:
		v_best = None #vehicle
		l_best = None #line
		d_best = None
		swap = None
		for vehicle in free_vehicles:
			for line in undistributed_lines:
				d_s = distance(vehicle.location.global_frame, line[0])
				d_e = distance(vehicle.location.global_frame, line[1])
				d = min(d_e, d_s)
				if (d_best == None) or (d < d_best):
					d_best = d
					v_best = vehicle
					l_best = line
					swap = (d_e < d_s)
		if d_best == None:
			raise RuntimeError("Unexpected Error in distribute tasks: if there are tasks then there should be an optimal one")
		free_vehicles.remove(v_best)
		undistributed_lines.remove(l_best)
		if swap:
			l_best = reversed(l_best)
		v_best.nextlocations.extend(l_best)
		v_best.simple_goto(v_best.nextlocations[0])

try:
	with server:
		while True:
			time.sleep(1)
			# search for vehicles that got nothing to do or have to have their target changed
			free_vehicles = []
			for vehicle in vehicles:
				if not vehicle.nextlocations:
					free_vehicles.append(vehicle)
				elif isnear(vehicle.nextlocations[0], vehicle.location.global_frame):
					vehicle.nextlocations.pop(0)
					if vehicle.nextlocations:
						vehicle.simple_goto(vehicle.nextlocations[0])
					else:
						free_vehicles.append(vehicle)
			distribute_tasks(free_vehicles, undistributed_lines)
except KeyboardInterrupt:
	pass



for vehicle in vehicles:
	print("Vehicle %i: Returning to Launch" % vehicle.instance_index)
	vehicle.mode = dronekit.VehicleMode("RTL")

	#Close vehicle object before exiting script
	print("Vehicle %i: Close vehicle object" % vehicle.instance_index)
	vehicle.close()
