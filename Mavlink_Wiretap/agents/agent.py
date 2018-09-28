#* encoding: utf-8 *#

# (c) 2018 Joram Brenz
# joram.brenz@online.de


class Agent(object):
    def __init__(self):
        self.receivers = set()
    
    def accept(self, item):
        raise NotImplementedError("Agent %s doesn't now what to do with received item." %self)

    def send_output_to(self, agent):
        self.receivers = set()
        self.send_output_also_to(agent)
    
    def send_output_also_to(self, agent):
        self.receivers.add(agent)
    
    def stop_sending_output_to(self, agent):
        self.receivers.discard(agend)
        
    def emit(self, item):
        for receiver in self.receivers:
            receiver.accept(item)
