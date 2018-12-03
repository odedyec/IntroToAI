from human_agent import Human
from adverserial_agent import AdverserialAgent
from fully_coop_agent import FullyCoopAgent
from semi_coop_agent import SemiCoopAgent


""" Global variables """
config_file = 'input_graph2.txt'
K = 1  # Set to a value to stop asking for input

agents = [FullyCoopAgent(0), FullyCoopAgent(4)]  # Set an agent to stop asking for input
DEBUG = True
f_value = -10