from my_parser import load_from_file
from simulator import Simulator


if __name__ == '__main__':
    sim = load_from_file("input_graph.txt", Simulator)
    sim.build_state_when_finished_loading_graph()
    print (sim)
    sim.apply_action(1)
    print (sim)
    sim.apply_action(2)
    print (sim)
