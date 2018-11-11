from human_agent import Human
from greedy_agent import Greedy
from vandal_agent import Vandal
from smart_greedy_agent import SmartGreedy
from a_star_agent import A_Star


""" Global variables """
K = 1  # Set to a value to stop asking for input
#agents = [A_Star(0)]  # Set an agent to stop asking for input
agents = [Greedy(0), A_Star(0)]  # Set an agent to stop asking for input
DEBUG = True
f_value = -10