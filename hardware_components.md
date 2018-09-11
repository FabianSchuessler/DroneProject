# Hardware components:

## Frame

### Legs
There are 4 Legs, which, in contrast to many other parts of the frame are properly injection molded and look really sturdy.  
(but fortunately while not looking like it the 3D Printed parts are also pretty solid)  
The red Legs are the front ones, they are in the same direction as the arrow on the brain.  

### Power distribution Board
The Legs are connected by 2 circuit boards (top and bottom one), the bottom one is used for power distribution, while the top one is only for mounting things.  

### Battery Holder
didn't even fit, because the holes for the solderpoints on the power distribution board were to small.  

## Battery
has a 4 pin connector for charging  
and a 2 pin connector for powering something with it  
only ever use one of them at a time (according to manual)  

## Battery Module
provide power from battery to brain and power distribution board (thereby ESCs and Motors)  
also measure battery voltage and current and report them to brain  

## Motors
2 with right and 2 with left thread threaded screws -> turn in opposite directions and shall be mounted crosswise on the frame  
brushless, speed regulated  
3 wires -> (problably) for three-phase electrical power -> connect to ESC  

## ESC (Electrical speed controller)
connected to Power distribution board, get pwm? signal from ErleBrain (ROS Hat PWM header)  

## GPS + Compass
ublox NEO-M8N-0-01 69202068561 1736 1300 25  
has a red led and multiple green leds  
red led lights up when the device is powered  
green leds blink when a GPS connection was established -> wait outside for some minutes  
to see if it does something check $$ sudo screen /dev/ttyS0 -> random characters appearing means it works  
missing wires are normal, uart only needs 4 pins and i2c needs 4 as well but uses ground/vdd from uart  

## Telemetry
The Telemetry Radio provides a serial connection between the Drone and the Base Station (Laptop).  
In our case it's on both sides connected via USB and on a Linux machine shows up as /dev/ttyUSB{X} where X is some number - most of the time 0.  
The telemetry radio has a green LED (and some red ones). If the green LED is blinking that means it's searching for a connection and if it's steady on that means the connection was successfully established.  
The telemetry has some parameters that can be set in the two devices and that have to be compatible in order for them to connect.
You can check (and correct) those settings with the following steps:  
* look at http://ardupilot.org/copter/docs/common-3dr-radio-advanced-configuration-and-technical-information.html to know what you are doing
* use a linux device (for instance the drone, or your laptop)
* take a look at the connected devices: ls /dev
* connect your telemetry device
* take another look at the connected devices. The new one is the telemetry.
* sudo screen /dev/ttyUSB{X} 57600 #connect to your device using the correct baud rate (57600 if it wasn't changed)
* make sure no other programm uses the device
* wait at least one second
* enter "+++" to enter configuration mode, (without the quotation marks - also do not press enter)
* after another second "OK" should appear on the screen and you will be able to see your keyboard input
* use the ATI commands from the link to view (ATI5) and change (ATS{n}=i) the parameters
* if necessary make sure to save (AT&W) your changes, before rebooting (ATZ) the device.  

Values that work:
S0:FORMAT= do not change this (values were 25 and 26)  
S1:SERIAL_SPEED=57  
S2:AIR_SPEED=64  
S3:NETID=25  
S4:TXPOWER=20  
S5:ECC=0  
S6:MAVLINK=1  
S7:OPPRESEND=0  
S8:MIN_FREQ=433050  
S9:MAX_FREQ=434790  
S10:NUM_CHANNELS=10  
S11:DUTY_CYCLE=100  
S12:LBT_RSSI=0  
S13:MANCHESTER=0  
S14:RTSCTS=0  
S15:MAX_WINDOW=131  

## ErleBrain3
Raspberry Pi 3  
ROS Hat
