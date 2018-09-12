# Documentation

## Approach

### Assembly

The Erle Copter was assembled according to the [Erle Copter: Assembly Instructions](http://docs.erlerobotics.com/erle_robots/erle_copter/assembly/erle_brain_2/EN). Additionally to the described tools, fitting screwdrivers, a nut wrench, four AA batteries for the RC Controller, a scissor, a micro-USB cable, and a knife were used, contrarily the super glow was not used. The 3D printed battery holder was cut with the knife for a better fit. There were no instructions for the [Anti-Vibration System](http://docs.erlerobotics.com/brains/erle-brain-3/anti-vibration_system). Currently, the vibration system has to rebuild after every hard landing. The micro-USB cable is necessary since the UART port is blocked by the GPS and only one micro-USB cable is provided, which is in use for the laptop-to-telemetry connection.

### Software

For this part, several guides were used such as [First Flight](http://docs.erlerobotics.com/erle_robots/erle_copter/first_flight), [Connect via SSH](http://docs.erlerobotics.com/brains/discontinued/erle-brain-2/getting_started/ssh), and [Connect APM](http://docs.erlerobotics.com/erle_robots/related/ground_control_station/apm_planner/connection_to_erle_brain_2). The OS image and arducopter/APM was preinstalled on the microSD. The Erle Brain 3 has an HDMI connection, which was used for direct access. The drone received internet access via ethernet from a windows laptop, which shared his Wifi access. Direct access to the university's internet was not possible via ethernet or wifi. The command to update (curl) the keys on the drone gives back an error "gpg: keyserver timed out", maybe because of the proxy settings of the used public network. Not all packages can be updated since the package apm-copter-erlebrain cannot be found. SSH access to the drone via ethernet is possible, the IP address of the drone change with every reboot. Calibration was done with QGroundControl via telemetry on a Linux laptop, the program does not show the GPS information. Listening to the UART connection shows that when the GPS is connected, information is sent and no information is received if not. On a windows laptop, QGroundControl shows some information, but an error message was displayed that the vehicle did not respond to the parameter request. The telemetry connection frequently dis- and reconnects. Once the APMPlaner2 showed some information on the windows laptop but this has not been reproduced yet.

#### After firmware reflashing

To receive the image of the erle brain operating system, it is required to send an email to Erle Robotics. After making a backup of the old OS, we flashed Erle-Brain-3-frambuesa-update-04-07-2017.img on the microSD. We installed apm-copter-3.5-stable-erlebrain using apt (apm-copter-erlebrain package was not available even after the successful key update). For the key update, we had to use a mobile connection since the public network available to us seems to have interfering proxy settings. We calibrated the RC Controller with the Drone and heard the music sound. We connected with windows and Linux laptops to the WiFi network provided by the copter. Windows does not receive an IP address in the drone's WiFi automatically, therefore the IP has to be manually set to 10.0.0.2. The windows firewall was also disabled. We loaded .params according to this [link](http://forum.erlerobotics.com/t/esc-calibration-failed/4050/2?u=ibaiape). We used QGroundControl to calibrate the compass and accelerometer. We added /bin/sleep 10 before while loop in ./apm.sh, this might not be necessary. Connection via WiFi makes interaction with APM and QGroundControl possible. Telemetry requires 57600 baud rate. To get GPS Fix the drone needs to be outdoors. It might take five or more minutes to get several satellites, seven satellites and a GPS speed of less than 1.0 are needed by QGroundControl, otherwise, it will not allow take off.

#### Control the drone via mobile phone

Install QGroundControl on an android phone. Connect to the drone via WiFi or telemetry radio. WiFi has a higher bandwidth, so the initialization/loading of the parameters is faster. WiFi should have about 200m range and telemetry radio more than 300m. Check if the QGroundControl app has the UDP link configured.

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

### QGroundControl - GPX Fix
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/QGroundControl%20-%20GPX%20Fix.png?raw=true "QGroundControl - GPX Fix")

### Drone in the guided mode in the air controlled by QGroundControl on an android phone via telemetry
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180912_100601.jpg?raw=true" "Drone in the guided mode in the air controlled by QGroundControl on an android phone via telemetry")

### Drone in the guided mode in the air controlled by QGroundControl on an android phone via telemetry
![alt text](https://github.com/FabianSchuessler/DroneProject/blob/master/images/20180912_100603.gif?raw=true" "Drone in the guided mode in the air controlled by QGroundControl on an android phone via telemetry")

## More links

[Ardupilot Copter Documentation](http://ardupilot.org/copter/index.html)

[Flight modes](http://ardupilot.org/copter/docs/flight-modes.html#full-list-of-flight-modes)

[Mission commands](http://ardupilot.org/copter/docs/mission-command-list.html)

[Forum Guide for new users](http://forum.erlerobotics.com/t/erle-copter-new-users-assembly-setup-tips/1317/4)

[Erlerobotics Forum](http://forum.erlerobotics.com/)

[core Flight System (NASA)](https://cfs.gsfc.nasa.gov/)