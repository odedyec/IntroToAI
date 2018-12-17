from bayes_network import BayesNetwork
from parser import load_from_file
from menus import *


class UserInterface(BayesNetwork):
    def print_flood_in_all_vertices(self):
        for vertex in self._vertices:
            print "Vertex {}\n-----------".format(vertex.id)
            vertex.print_prob_for_flood()

    def print_evacuees_in_all_vertices(self):
        for vertex in self._vertices:
            print "Vertex {}\n-----------".format(vertex.id)
            vertex.print_prob_for_evacuees()

    def print_blocked_of_all_edges(self):
        for edge in self._edges:
            print "Edge {}\n------------".format(edge.id)
            edge.print_prob_for_blockage()

    def query(self):
        inp = reasoning_menu()
        if inp is 1:
            self.print_flood_in_all_vertices()
        elif inp is 2:
            self.print_evacuees_in_all_vertices()
        elif inp is 3:
            self.print_blocked_of_all_edges()
        else:
            print 'Please learn how to read'

    def reset_evidence_list(self):
        for vertex in self._vertices:
            vertex.reset()
        for edge in self._edges:
            edge.reset()

    def add_evidence(self):
        evidence_type, vertex = evidence_menu()
        if evidence_type is EVIDENCE_TYPE_FLOOD:
            self._vertices[vertex].flood_reported()
        elif evidence_type is EVIDENCE_TYPE_EVACUESS:
            pass
        else:
            print 'Please learn how to read'

    def menu(self):
        inp = main_menu()
        if inp is 1:
            self.reset_evidence_list()
        elif inp is 2:
            self.add_evidence()
        elif inp is 3:
            self.query()
        elif inp is 4:
            return False
        else:
            print 'Please learn how to read'
        return True


if __name__ == '__main__':
    ui = load_from_file()
    ui.print_vertices()
    ui.print_edges()
    while ui.menu():
        pass
