from smart_greedy_agent import SmartGreedy
from greedy_agent import Greedy
from simulator import HurricaneSimulator
from utils import *
from copy import deepcopy


class AIAgent(SmartGreedy):
    ADVERSERIAL = 1
    SEMI_COOPERATIVE = 2
    FULLY_COOPERATIVE = 3
    MAX_DEPTH = 2

    def __init__(self, state, game_type=2):
        SmartGreedy.__init__(self, state)
        self.game_type = game_type

    def is_terminal(self, sim=HurricaneSimulator()):
        """
        Checks if reached a terminal point, i.e., no more people to save, or time is up
        :param sim:
        :return:
        """
        if sim.time >= sim.deadline:
            return True
        if (sim.get_number_of_people_in_towns() + sum([agent.people_in_vehicle for agent in sim.all_agents])) == 0:
            return True
        return False

    def value(self, sim=HurricaneSimulator()):
        """ How many people were saved by each agent """
        return [agent.people_saved for agent in sim.all_agents]

    def calculate_heuristic_for_agent(self, agent, sim=HurricaneSimulator()):
        people_able_to_save = 0  # number_of_people_in_towns + agent.people_in_vehicle
        cost_to_people = agent.find_people(sim)  # Find costs for all vertices with people
        cost_to_shelter = agent.find_sheleter(sim)  # Find costs for all shelter vertices

        if len(cost_to_shelter) == 0:
            """ No shelter, we are all doomed :("""
            return 0
        """ Find closest shelter """
        closest_shelter = find_closest(cost_to_shelter)[1]
        if (1 + sim.K * agent.people_in_vehicle) * closest_shelter + sim.get_time() < sim.deadline:
            """ People in vehicle can be saved """
            people_able_to_save += agent.people_in_vehicle
        else:
            """ Unable to reach shelter """
            return 0
        """ Find people in towns """
        shelter_nodes = sim.get_shelter()
        time_elapsed = sim.get_time()
        for people in cost_to_people:
            path_to_shelter_for_person = find_closest(agent.search_grid(shelter_nodes, people[2], sim))
            time_elapsed_for_person = time_elapsed + people[1] + \
                                      (1 + sim.K * sim.graph[people[2]][people[2]].num_of_people) \
                                      * path_to_shelter_for_person[1]
            if time_elapsed_for_person < sim.deadline:
                people_able_to_save += sim.graph[people[2]][people[2]].num_of_people
        return people_able_to_save

    def heuristic(self, sim=HurricaneSimulator()):
        """
        For cutoff purposes.
        The heuristic calculates most optimistic results for each agent.
        The heuristic for an agent assumes that there are no other agents in the game,
        and calculates how many people it is possible to save.
        """
        return [agent.people_saved + self.calculate_heuristic_for_agent(agent, sim) for agent in sim.all_agents]

    def is_new_action_better(self, best_value, new_value, sim_emulator=HurricaneSimulator()):
        """ check, based on game type, if the new value is better than current best value """
        if self.game_type == self.SEMI_COOPERATIVE:
            return (new_value[sim_emulator.agent_index - 1] > best_value[sim_emulator.agent_index - 1] or
                    (new_value[sim_emulator.agent_index - 1] == best_value[sim_emulator.agent_index - 1] and
                    new_value[sim_emulator.agent_index] > best_value[sim_emulator.agent_index]))

        if self.game_type == self.FULLY_COOPERATIVE:
            return sum(new_value) > sum(best_value)

        if self.game_type == self.ADVERSERIAL:
            return new_value[sim_emulator.agent_index - 1] - new_value[sim_emulator.agent_index] >= \
                   best_value[sim_emulator.agent_index - 1] - best_value[sim_emulator.agent_index]

    def recursive_tree(self, depth, sim=HurricaneSimulator()):
        """
        Main function. Recursively find for each action what is the score and return the action with the best score
        :param depth:
        :param sim:
        :return:
        """
        ''' Check if terminal or depth reached an end '''
        if self.is_terminal(sim):
            return self.value(sim)
        if depth == self.MAX_DEPTH:
            return self.heuristic(sim)
        ''' Set vars '''
        best_value = [-2 ** 31] * len(sim.all_agents)
        best_move = [-1, 1]
        ''' Check all possible actions '''
        for action in self.get_all_possible_actions(sim):
            sim_emulator = deepcopy(sim)
            sim_emulator.apply_action(action[0])
            new_value = self.recursive_tree(depth + 1, sim_emulator)
            if self.is_new_action_better(best_value, new_value, sim_emulator):
                best_value = new_value
                best_move = action
        ''' return values '''
        if depth == 0:
            return best_move
        else:
            return best_value

    def choose_next_option(self, sim=HurricaneSimulator()):
        if self.is_terminal(sim):
            return -1
        best = self.recursive_tree(0, sim)
        return best[0]

