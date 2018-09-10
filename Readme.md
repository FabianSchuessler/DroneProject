# Documentation

## Approach

### Assembly

The Erle Copter was assembled according to the [Erle Copter: Assembly Instructions](http://docs.erlerobotics.com/erle_robots/erle_copter/assembly/erle_brain_2/EN). Additionally to the described tools, fitting screwdrivers, a nut wrench, four AA batteries for the RC Controller, a scissor, a micro-USB cable, and a knife were used, contrarily the super glow was not used. The 3D printed battery holder was cut with the knife for a better fit. There were no instructions for the [Anti-Vibration System](http://docs.erlerobotics.com/brains/erle-brain-3/anti-vibration_system). Currently, the vibration system has to rebuild after every hard landing. The micro-USB cable is necessary since the UART port is blocked by the GPS and only one micro-USB cable is provided, which is in use for the laptop-to-telemetry connection.

### Software

For this part, several guides were used such as [First Flight](http://docs.erlerobotics.com/erle_robots/erle_copter/first_flight), [Connect via SSH](http://docs.erlerobotics.com/brains/discontinued/erle-brain-2/getting_started/ssh), and [Connect APM](http://docs.erlerobotics.com/erle_robots/related/ground_control_station/apm_planner/connection_to_erle_brain_2). The OS image and arducopter/APM was preinstalled on the microSD. The Erle Brain 3 has an HDMI connection, which was used for direct access. The drone received internet access via ethernet from a windows laptop, which shared his Wifi access. Direct access to the university's internet was not possible via ethernet or wifi. The command to update (curl) the keys on the drone gives back an error "gpg: keyserver timed out", maybe because of the proxy settings of the used public network. Not all packages can be updated since the package apm-copter-erlebrain cannot be found. SSH access to the drone via ethernet is possible, the IP address of the drone change with every reboot. Calibration was done with QGroundControl via telemetry on a Linux laptop, the program does not show the GPS information. Listening to the UART connection shows that when the GPS is connected, information is sent and no information is received if not. On a windows laptop, QGroundControl shows some information, but an error message was displayed that the vehicle did not respond to the parameter request. The telemetry connection frequently dis- and reconnects. Once the APMPlaner2 showed some information on the windows laptop but has not been reproduced yet.

[Ardupilot Copter Documentation](http://ardupilot.org/copter/index.html)
[core Flight System (NASA)](https://cfs.gsfc.nasa.gov/)

## Pictures

### After (Step 6) ESCs and before (Step 5) Fixing the Erle-Brain 2 (1/2)
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_093011.jpg?raw=true "After (Step 6) ESCs and before (Step 5) Fixing the Erle-Brain 2 (1/2)")

### After (Step 6) ESCs and before (Step 5) Fixing the Erle-Brain 2 (2/2)
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_093017.jpg?raw=true "After (Step 6) ESCs and before (Step 5) Fixing the Erle-Brain 2 (2/2)")

### After (Step 5) Fixing the Erle-Brain 2
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_100249.jpg?raw=true "After (Step 5) Fixing the Erle-Brain 2")

### (Step 6.3) Connecting the ESCs to the Erle-Brain 2
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_100643.jpg?raw=true "(Step 6.3) Connecting the ESCs to the Erle-Brain 2")

### After the assembly, view of the drone's user interface
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_121226.jpg?raw=true "After the assembly, view of the drone's user interface")

### Erle-Brain has internet via ethernet from Laptop
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180905_144911.jpg?raw=true "Erle-Brain has internet via ethernet from Laptop")

### Laptop accesses Erle-Brain with SSH via ethernet
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180906_152034.jpg?raw=true "Laptop accesses Erle-Brain with SSH via ethernet")

### Before the first flights
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180907_112122.jpg?raw=true "Before the first flights")




