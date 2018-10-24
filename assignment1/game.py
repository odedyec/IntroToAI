from simulator import HurricaneSimulator
from human_agent import Human


""" Global variables """
K = 0.1 # None  # Set to a value to stop asking for input
agents = [Human(0)]  # []  # Set an agent to stop asking for input


def game():
    query()
    for agent in agents:
        sim = HurricaneSimulator(K)
        sim.state = agent.get_state()
        while sim.ok():
            sim.print_all()
            action = agent.choose_next_option()
            sim.apply_action(action)
        print("\n\n=================================\n\n")
        sim.print_all()

def query():
    global K
    if K is None:
        K = float(input("Set a slow-down value [K]"))
    if len(agents) == 0:
        n = int(input("How many agents operate?"))
        for i in range(n):
            agent_type = input("Set agent type[1-3]\n\n1. Human agent\n2. Greedy agent\n3. Vandal agent")
            agent_loc = int(input("Set agent's initial vertex"))
            if agent_type is '1':
                agents.append(Human(agent_loc))
            elif agent_type is '2':
                pass
            elif agent_type is '3':
                pass


if __name__ == '__main__':
    game()

