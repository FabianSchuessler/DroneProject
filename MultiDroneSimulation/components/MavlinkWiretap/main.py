#! /usr/bin/env python3
#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


"""
This script is supposed to be used to listen to and extract data from a mavlink connection.
It works as a proxy between drone and ground control station.
Currently it is configured to be run on the GCS side of the communication,
but it can easily be reconfigured to run on the drone.

The different functionalities of this project are provided by classes called Agents.
They accept input with an "accept" method and once they are able to create an output they emit that output to all registered listeners.
Some Agents like Udp- and SerialHandler emmit output independently from any input using concurrent receiving threads.
They are used with a context manager.

You will need to make sure the following packages or a similar version is installed:
- pymavlink 2.2.10
- babeltrace 1.5.3
- pyserial 3.4
All of them are available via pip[3] install command.

If you want to connect your drone via Serial just switch out the first line in main for the version in the comment there.
(Hint: If you need a udp instead of a serial connections or vice versa and don't want to modify the code try using socat.)
"""

from agents import *
import sys, os, inspect, time
import serial

try:
    i = sys.argv.index("-I")
except ValueError:
    I = 0
else:
    I = int(sys.argv[i+1])

interval = 0.001

serial_config = {
    "port" : "/dev/ttyUSB0",
    "baudrate" : 57600,
    "timeout" : interval,
    "parity" : serial.PARITY_NONE,
}

udp_config_uav = {
    "port" : 14550 + 10*I,
    "timeout" : interval,
}

udp_config_gcs = {
    "port" : 50000 + 10*I,
    "address": ("127.0.0.1", 24550 + 10*I),
    "timeout" : interval,
}

COLOR_MAGENTA = "\x1b[35m"
COLOR_CYAN    = "\x1b[36m"

PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
message_definition_path =  os.path.join(PATH, "message_definitions", "v1.0", "ardupilotmega.xml")
trace_path = os.path.join(PATH, "ctf_trace%i" % I)
log_path = os.path.join(PATH, "log%i.txt" % I)

def main():
    # set up agents
    uav = UdpHandler(**udp_config_uav)
    #uav = SerialHandler(serial_config)

    uav_assembler = MessageAssembler()
    uav_decoder = MessageDecoder()
    uav_logger = Logger("UAV", COLOR_CYAN)

    gcs = UdpHandler(**udp_config_gcs)
    gcs_assembler = MessageAssembler()
    gcs_decoder = MessageDecoder()
    gcs_logger = Logger("GCS", COLOR_MAGENTA)
    
    ctfWriter = CTFWriter(message_definition_path, trace_path, "1.0")

    # connect agents
    uav.send_output_to(gcs)
    uav.send_output_also_to(uav_assembler)
    uav_assembler.send_output_to(uav_decoder)
    uav_decoder.send_output_to(uav_logger)
    uav_decoder.send_output_also_to(ctfWriter)

    gcs.send_output_to(uav)
    gcs.send_output_also_to(gcs_assembler)
    gcs_assembler.send_output_to(gcs_decoder)
    gcs_decoder.send_output_to(gcs_logger)
    gcs_decoder.send_output_also_to(ctfWriter)

    with uav, gcs: #activate receiving threads
        try:
            while True:
                time.sleep(interval)
                sys.stdout.flush()
        except KeyboardInterrupt:
            pass

    Logger.save_to_file(logpath)
    ctfWriter.flush()

if __name__ == "__main__":
    main()
