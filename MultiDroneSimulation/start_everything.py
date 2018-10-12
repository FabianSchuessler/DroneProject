#! /usr/bin/env python3
#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de

"""
This was optimized to work with gnome-terminal, but you can try to use another terminal instead.
Pressing Ctrl-C in the corresponding tab/terminal will stop the different components.
If you want to see all error messages make sure to set your terminal settings to keep open after finishing command.
"""

# imports
import sys
import os
import subprocess
import time

# Components
PATH_Q_GROUND_CONTROL        = os.path.join("components", "QGroundControl"       , "QGroundControl.AppImage")
PATH_MULTI_DRONE_COORDINATOR = os.path.join("components", "MultiDroneCoordinator", "coordinator.py"         )
PATH_MAVLINK_WIRETAP         = os.path.join("components", "MavlinkWiretap"       , "main.py"                )
PATH_SIMULATION              = os.path.join("components", "Simulation"           , "my_sim_vehicle.py"      )
PATH_FLIGHTGEAR_VIEW         = os.path.join("components", "Simulation"           , "my_fg_quad_view.sh"     )


# number of vehicles to spawn (must not be more than supported by simulation - depending on number of copies of the ardupilot repository)
locations = ["60.397,5.318,10,0",
			 "60.395,5.323,10,0",
			]
n = len(locations)

def in_new_tab(name, command):
	new_tab_command = ["gnome-terminal","--tab", "-t", name, "-e", " ".join(command)]
	return subprocess.Popen(new_tab_command)


print("launching components")

# start n instances of the following:
simulations  = []
flightgears  = []
mavwiretaps  = []
for i, l in enumerate(locations):
	time.sleep(1)
	simulations.append( in_new_tab( "arducopter%i" % i, [PATH_SIMULATION, "-I", str(i), "-v", "ArduCopter", "-l", l] ) )
	time.sleep(0.1)
	flightgears.append( in_new_tab( "flightgear%i" % i, [PATH_FLIGHTGEAR_VIEW , str(i)] ) )
	time.sleep(0.1)
	mavwiretaps.append( in_new_tab( "mavwiretap%i" % i, [PATH_MAVLINK_WIRETAP, "-I %i" % i] ) )

time.sleep(20)

# start of GCS(s)
gcss = []
#q_ground_control = subprocess.Popen( [PATH_Q_GROUND_CONTROL] )
#gcss.append(q_ground_control)
multi_drone_coordinator = in_new_tab( "MultiDroneCoordinator" , [PATH_MULTI_DRONE_COORDINATOR, "%i" % n] )
gcss.append(multi_drone_coordinator)

print("started all components")
print("close all components by pressing ctr-c in the respective terminals/tabs")
# wait until everything is closed again
for p  in gcss + simulations + flightgears + mavwiretaps:
	p.wait()
