from bayes_network import BayesNetwork
from parser import load_from_file


bn = load_from_file()
bn.print_vertices([0])
bn.print_edges([1])