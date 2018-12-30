from my_parser import load_from_file
from simulator import Simulator
from value_iteration import value_iteration


if __name__ == '__main__':
    #TODO blockage is currently ignored

    sim = load_from_file("input2.txt", Simulator)
    sim.build_state_when_finished_loading_graph()
    # print(sim.utility)
    sim.print_graph_as_string()
    value_iteration(sim, 200)
    # for v in sim.utility:
    #     print (v, sim.utility[v])
    # print(sim.utility)


    print(sim)
    while not sim.is_state_terminal():
        sim.act_based_utility()
        print(sim)
    #
    # print (sim)
    # sim.apply_action(1)
    # print (sim)
    # sim.apply_action(2)
    # print (sim)
