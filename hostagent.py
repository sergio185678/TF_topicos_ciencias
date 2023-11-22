from sys import argv
import threading
from PySide6.QtWidgets import QApplication
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import display_message,start_loop
from truckagent import TruckAgent
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage

from globals import Global
from gui import Gui

class MyTimedBehaviour(TimedBehaviour):
    def __init__(self, agent,other, time):
        super(MyTimedBehaviour, self).__init__(agent, time)
        self.agent = agent

        self.other = other

    def on_time(self):
        super(MyTimedBehaviour, self).on_time()
        self.agent.truck.move()

        gui.update()

        if(self.agent.truck.txt!=""):
            message = ACLMessage(ACLMessage.INFORM)
            message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            message.add_receiver(AID(self.other))
            message.set_content(self.agent.truck.txt)
            self.agent.send(message)

class YourTimedBehaviour(TimedBehaviour):
    def __init__(self, agent, time):
        super(YourTimedBehaviour, self).__init__(agent, time)
        self.agent = agent

    def on_time(self):
        super(YourTimedBehaviour, self).on_time()
        
        

class HostAgent(Agent):
    gui = None
    truck = None

    def __init__(self, aid,receiver, extra_parameter=None):
        super(HostAgent, 
              self).__init__(aid=aid, debug=False)

        self.truck = TruckAgent(extra_parameter)

        mytimed = MyTimedBehaviour(self,receiver, .9)
        yourtimed = YourTimedBehaviour(self, 9)
        self.behaviours.append(mytimed)
        self.behaviours.append(yourtimed)

class ReceiverAgent(Agent):
    def __init__(self, aid):
        super(ReceiverAgent, self).__init__(aid=aid, debug=False)

    def react(self, message):
        super(ReceiverAgent, self).react(message)
        display_message(self.aid.localname,
                        f"{message.sender.name}: {message.content}")

def agentsexec():
    start_loop(agents)

if __name__ == '__main__':

    agents = list()

    port = int(argv[1])
    receiver_agent_name = 'receiver_agent_{}@localhost:{}'.format(port, port)
    receiver_agent = ReceiverAgent(AID(name=receiver_agent_name))
    agents.append(receiver_agent)

    c=1000
    for i in range(Global.num_trucks):
        port = int(argv[1]) + c
        truck_agent_name = 'agent_truck_{}@localhost:{}'.format(port, port)
        truck_agent = HostAgent(AID(name=truck_agent_name),receiver_agent_name,i+1)
        agents.append(truck_agent)
        c += 1

    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    gui = Gui(agents[1:])
    gui.show()
    app.exec()
    x.join()
