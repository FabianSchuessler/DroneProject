# Hardware components:

## Frame
Arms, Power distribution board, Battery fix, ...

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
ublox
has a red led and multiple green leds
red led lights up when the device is powered
green leds blink when a GPS connection was established -> wait outside for some minutes
to see if it does something check $$ sudo screen /dev/ttyS0 -> random characters appearing means it works
missing wires are normal, uart only needs 4 pins and i2c needs 4 as well but uses ground/vdd from uart

## Telemetry
screen /dev/ttyUSB{X} 57600
enter +++
enter ATI commands -> http://ardupilot.org/copter/docs/common-3dr-radio-advanced-configuration-and-technical-information.html

## ErleBrain3
Raspberry Pi 3
ROS Hat
