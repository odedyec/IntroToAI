from simulator import HurricaneSimulator
from human_agent import Human


""" Global variables """
K = 5
agents = None


def game():
    hs = HurricaneSimulator()
    hs.load_from_file()
    agent = Human()
    agent.state = initial_state
    for i in range(5):
        new_state = agent.choose_next_option()
        agent.traverse(new_state, K, hs)


def query():
    global K
    K = int(input("Set a slow-down value [K]"))
    n = int(input("How many agents operate?"))
    for i in range(n):
        agent_type = input("Set agent type[1-3]\n\n1. Human agent\n2. Greedy agent\n3. Vandal agent")
        agent_loc = int(input("Set agent's initial vertex"))

if __name__ == '__main__':
    game()

