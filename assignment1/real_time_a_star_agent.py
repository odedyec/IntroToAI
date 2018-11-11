from greedy_agent import Greedy
from agent import BaseAgent
from simulator import HurricaneSimulator
from numpy import inf
from shortest_path import dijkstra_shortest_path
from smart_greedy_agent import SmartGreedy
from smart_greedy_agent import Node
from agent import BaseAgent
from a_star_agent import A_Star
import copy


# PEOPLE_UNSAVED_VALUE = 100


class Real_Time_A_Star(A_Star):

    def __init__(self, state, expands=inf):
        super(Real_Time_A_Star, self).__init__(state)
        self.max_expands = expands





