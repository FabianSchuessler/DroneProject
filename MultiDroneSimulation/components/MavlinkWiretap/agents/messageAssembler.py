#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


from .agent import Agent

class MessageAssembler(Agent):
    def __init__(self):
        super(MessageAssembler, self).__init__()
        self.msgbytes = bytearray()
    
    def accept(self, packet):
        for byte in packet:
            self.accept_byte(byte)
    
    def accept_byte(self, byte):
        # collect bytes
        if self.msgbytes or byte == 0xFE:
            self.msgbytes.append(byte)
        else:
            print(repr(byte), repr("\xFE"))
            print("UNEXPECTED BYTE")
        
        # trigger decoding
        if len(self.msgbytes) >= 2:
            if len(self.msgbytes) >= self.msgbytes[1]+8:
                self.emit(self.msgbytes)
                self.msgbytes = bytearray()
