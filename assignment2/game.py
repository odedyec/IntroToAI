from simulator import HurricaneSimulator


""" Global variables """
from config import *


def game():
    query()
    sim = HurricaneSimulator(agents, K, config_file=config_file)
    while sim.ok():
        if DEBUG:
            sim.print_all()
            print("=================================\n\n\n\n")
        action = sim.current_agent.choose_next_option(sim)
        sim.apply_action(action)
    print("\n\n\n-------------------------\n#### Final result ####\n\n")
    sim.print_all()
    # print("+++++ Agent expanded %d nodes +++++" % agent.expanded_nodes)
    # P = sim.people_saved * f_value + agent.expanded_nodes
    # print("##### Agent performance is %d #####" % P)


def query():
    global K
    if K is None:
        K = float(input("Set a slow-down value [K]"))
    if len(agents) == 0:
        n = 2  # 2 agents are operating simultaniously
        for i in range(n):
            agent_type = input("Set agent type[1-2]\n\n1. Human agent\n2. AI agent\n")
            agent_loc = int(input("Set agent's initial vertex"))
            if agent_type is '1':
                agents.append(Human(agent_loc))
            elif agent_type is '2':
                pass


if __name__ == '__main__':
    game()

