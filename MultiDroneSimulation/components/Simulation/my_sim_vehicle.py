#! /usr/bin/env python3
#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de

import os, sys, inspect, subprocess
PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


try:
    i = sys.argv.index("-I")
except ValueError:
    I = 0
else:
    I = int(sys.argv[i+1])

# set correct cwd
cwd_path = os.path.join(PATH, "ardupilot%i" % I, "ArduCopter")
os.chdir(cwd_path)
sim_path = os.path.join(PATH, "ardupilot%i" % I, "Tools", "autotest", "sim_vehicle.py")

subprocess.run([sim_path] + sys.argv)
