#! /usr/bin/env python3
#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de

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


# start of GCS(s)
gcss = []
#q_ground_control = subprocess.Popen( [PATH_Q_GROUND_CONTROL] )
#gcss.append(q_ground_control)
multi_drone_coordinator = subprocess.Popen( [PATH_MULTI_DRONE_COORDINATOR, "%i" % n] )
gcss.append(multi_drone_coordinator)

def in_new_tab(name, command):
	new_tab_command = ["gnome-terminal","--tab", "-t", name, "-e", " ".join(command)]
	return subprocess.Popen(new_tab_command)


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

# wait until everything is closed again
for p  in gcss + simulations + flightgears + mavwiretaps:
	p.wait()

print("finished start_everything.py")
