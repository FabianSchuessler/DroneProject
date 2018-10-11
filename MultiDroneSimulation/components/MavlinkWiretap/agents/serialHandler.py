#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


from .agent import Agent

import serial, threading

class SerialHandler(Agent):
    def __init__(self, config):
        super(SerialHandler, self).__init__()
        self.config = config
        self.active_flag = threading.Event()
        self.serial_lock = threading.Lock()
        self.serial = serial.Serial(**config)
        self.loopthread = threading.Thread(target=self.loop)

    def __enter__(self):
        self.serial = serial.Serial(**self.config)
        self.active_flag.set()
        self.loopthread.start()

    def __exit__(self, *args):
        with self.serial_lock:
            self.active_flag.clear()
        self.loopthread.join()
        self.serial.close()

    def accept(self, packet):
        with self.serial_lock:
            if self.active_flag.is_set():
                self.serial.write(packet)
            else:
                print("unactive %s can't accept packet" %self)
    
    def loop(self):
        # receive
        while self.active_flag.is_set():
            packet = self.serial.readline()
            if packet:
                self.emit(packet)

