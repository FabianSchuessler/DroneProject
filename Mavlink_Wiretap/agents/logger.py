#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


from .agent import Agent

import sys, time, collections, pprint, string

COLOR_RESET   = "\x1b[0m"

class Logger(Agent):
    log = {
        "version":"1.0.2",
        "t_begin":time.time(),
        "messages":collections.defaultdict(list),
    }
    
    def __init__(self, name, color):
        super(Logger, self).__init__()
        self.name = name
        self.color = color
        
    def accept(self, msg):
        msg = str(msg)
        # Log
        self.log["messages"][self.name].append((time.time(), msg))
        # Print
        sys.stdout.write(self.color)
        for char in msg:
            if char in string.printable:
                sys.stdout.write(char)
            else:
                sys.stdout.write("_")
                #sys.stdout.write(hex(ord(char)))
        sys.stdout.write("\n\n")
        sys.stdout.write(COLOR_RESET)

    @classmethod
    def save_to_file(cls, filename):
        with open(filename,"w") as logfile:
            pprint.pprint(cls.log, logfile)
