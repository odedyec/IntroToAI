from human_agent import Human
from greedy_agent import Greedy
from vandal_agent import Vandal
from smart_greedy_agent import SmartGreedy
from a_star_agent import A_Star
from real_time_a_star_agent import Real_Time_A_Star


""" Global variables """
config_file='input_graph2.txt'
K = 0.4  # Set to a value to stop asking for input
agents = [SmartGreedy(0), A_Star(0), Real_Time_A_Star(0)]  # Set an agent to stop asking for input
DEBUG = False
f_value = -10