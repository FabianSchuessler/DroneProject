#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


from .agent import Agent

import pymavlink.dialects.v20.ardupilotmega as mavlink
    
class MessageDecoder(Agent):
    def __init__(self):
        super(MessageDecoder, self).__init__()
        # create a mavlink instance, without a file object (some methods will fail, but we just won't use them)
        self.mav = mavlink.MAVLink(None)
        self.fails = 0
        self.succeeds = 0

    def accept(self, msgbytes):
        try:
            # decode message
            msg = self.mav.decode(msgbytes)
        except Exception as e:
            print(e)
            self.fails += 1
        else:
            self.succeeds += 1
            self.emit(msg.to_dict())

    def feedback():
        print("decoded %i of %i messages" %(succeeds, fails+succeeds))
