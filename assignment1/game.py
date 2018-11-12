from simulator import HurricaneSimulator
from human_agent import Human
from greedy_agent import Greedy
from vandal_agent import Vandal
from smart_greedy_agent import SmartGreedy


""" Global variables """
from config import *


def game():
    query()
    for agent in agents:
        sim = HurricaneSimulator(K, config_file=config_file)
        sim.state = agent.get_state()
        while sim.ok():
            if DEBUG:
                sim.print_all()
                print("=================================\n\n\n\n")
            action = agent.choose_next_option(sim)
            sim.apply_action(action, agent.should_pick_and_drop)
        print("\n\n\n-------------------------\n#### Final result ####\n\n")
        sim.print_all()
        print("+++++ Agent explored %d steps +++++"%agent.steps_explored)
        P = sim.people_saved * f_value + agent.steps_explored
        print("##### Agent performance is %d #####"%P)


def query():
    global K
    if K is None:
        K = float(input("Set a slow-down value [K]"))
    if len(agents) == 0:
        n = int(input("How many agents operate?"))
        for i in range(n):
            agent_type = input("Set agent type[1-6]\n\n1. Human agent\n2. Greedy agent\n3. Vandal agent\n4. Smart Greedy agent\n5. A* agent\n6. Real-Time A* agent")
            agent_loc = int(input("Set agent's initial vertex"))
            if agent_type is '1':
                agents.append(Human(agent_loc))
            elif agent_type is '2':
                agents.append(Greedy(agent_loc))
            elif agent_type is '3':
                agents.append(Vandal(agent_loc))
            elif agent_type is '4':
                agents.append(SmartGreedy(agent_loc))
            elif agent_type is '5':
                pass
                agents.append(A_Star(agent_loc))
            elif agent_type is '6':
                pass
                # agents.append(RTAStar(agent_loc))

if __name__ == '__main__':
    game()

