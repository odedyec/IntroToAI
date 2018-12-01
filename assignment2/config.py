from human_agent import Human
from ai_agent import AIAgent


""" Global variables """
config_file = 'input_graph2.txt'
K = 0.1  # Set to a value to stop asking for input
GAME_TYPE = AIAgent.FULLY_COOPERATIVE
agents = [AIAgent(0, GAME_TYPE), AIAgent(2, GAME_TYPE)]  # Set an agent to stop asking for input
DEBUG = True
f_value = -10