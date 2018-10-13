This folder is set up to
	launch 2 (or more) simulated drones,
	show them in 3D using flightgear
	show them on a map using my own Groundstation or QGroundControl

My own Groundstation shows how 2 Drones can work together by dynamically distributing tasks (flying along lines) to them.

This was not really tested a lot, so I guess it works only on the PC of the developer. :(
But if you try to get it to work on your machine and need help just send me a mail:
joram.brenz@online.de



edit: some more steps for installation:

- get this repository (most likely already done)
- go to components/Simulation and clone the ardupilot repository
	git clone https://github.com/ArduPilot/ardupilot
- get all dependencies of ardupilot (see below), however you can also just install them once you encounter missing dependency errors
- go into the ardupilot repository
	cd ardupilot
- if you are in a network with restrictive firewall settings (like eduroam in Universities) use this workaround to use url.https: instead of git: protocol
	git config --global url.https://github.com/.insteadOf git://github.com/
	(if you misspell something the first time you execute this command you may need to delete the created entry from your git config before retrying)
- initialise submodules of ardupilot
	git submodule update --init --recursive
- copy folder to components/Simulation/ardupilot0, components/Simulation/ardupilot1, ... so you have as many folders as you want to have simulated drones
- in each of those folders open the file ardupilot{i}/ArduCopter/config.h and replace MAV_SYSTEM_ID so it is unique (I suggest taking the same number as the folder has)
- then do the following steps in each ardupilot{i} folder to compile it
	export PATH=$PATH:$HOME/ardupilot/Tools/autotest
	./waf configure --board sitl
	./waf --targets bin/arducopter		-> don't do this step before copying the repository folder or the compiled files may link to the same virtual eeprom and things will get messy
- now just run the start_everything.py file

dependencies: (list may not be complete; also some may not be necessary if you dont want to use MAVProxy's GUI)
	install from your os/distribution package source (apt-get install for debian/ubuntu/alike)

		ccache -> .. but apparently it also works without (?)
		build-essential
		g++
		gawk
		git
		make
		wget
		libtool
		python-pip
		python-dev
		python-setuptools
		python-numpy

		xterm
		libtool-bin
		libxml2-dev
		libxslt1-dev
		python-matplotlib
		python-scipy
		python-opencv
		python-pyparsing
		python-wxgtk3.0
		python3-babeltrace (not available via pip)
		python3-pip

	pip for python2 (pip install ...)
		lxml
		pymavlink
		MAVProxy
		future

	pip3 for python3 (pip3 install ...)
		dronekit
		pyserial (you can also get this as python3-serial from package manager)
		pymavlink
		MAVProxy
