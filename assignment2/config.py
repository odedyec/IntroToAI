from human_agent import Human
from adverserial_agent import AdverserialAgent
from fully_coop_agent import FullyCoopAgent


""" Global variables """
config_file = 'input_graph2.txt'
K = 0.1  # Set to a value to stop asking for input

agents = [AdverserialAgent(0), AdverserialAgent(2)]  # Set an agent to stop asking for input
DEBUG = True
f_value = -10