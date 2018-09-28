#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


from .agent import Agent

import socket, select, threading

class UdpHandler(Agent):
    def __init__(self, port, timeout, address = None):
        super(UdpHandler, self).__init__()
        self.port = port
        self.timeout = timeout
        self.address = address
        self.active_flag = threading.Event()
        self.socket_lock = threading.Lock()
        self.loopthread = threading.Thread(target=self.loop)
        
    def __enter__(self):
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1",self.port))
        self.active_flag.set()
        self.loopthread.start()

    def __exit__(self, *args):
        with self.socket_lock:
            self.active_flag.clear()
        self.loopthread.join()
        self.socket.close()

    def accept(self, packet):
        # send
        if not self.address:
            print("%s dismissed packet because recipient is not known (yet)" %s)
            return
        with self.socket_lock:
            if self.active_flag.is_set():
                self.socket.sendto(packet, self.address)
            else:
                print("unactive %s can't accept packet" %self)

    def loop(self):
        # receive
        while self.active_flag.is_set():
            if select.select([self.socket],[],[],self.timeout)[0]:
                packet, self.address = self.socket.recvfrom(100000000) #some big number, so messages are definitely shorter, because otherwise they get cut off and the rest is lost
                if packet:
                    self.emit(packet)
