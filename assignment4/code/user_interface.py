from bayes_network import BayesNetwork
from menus import *
from copy import deepcopy


class UserInterface(BayesNetwork):
    def print_flood_in_all_vertices(self):
        for vertex in self._vertices:
            print ("Vertex {}\n-----------".format(vertex.id))
            print(vertex.print_prob_for_flood())

    def print_evacuees_in_all_vertices(self):
        for vertex in self._vertices:
            copy = deepcopy(self)
            print("Vertex {}\n-----------".format(vertex.id))
            print(vertex.print_prob_for_evacuees())
            q = self.enumeration_ask(vertex.evacuees, copy._evidence_list)
            print("P(Evacuees {} | {}) = {}\n".format(vertex.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))

    def print_blocked_of_all_edges(self):
        for edge in self._edges:
            print("my evidence")
            print(i.get_name() for (i, j) in self._evidence_list)
            copy = deepcopy(self)
            print("copy evidence")
            print(i.get_name() for (i, j) in copy._evidence_list)
            print ("Edge {}\n------------".format(edge.id))
            # print(edge.print_prob_for_blockage())
            q = self.enumeration_ask(edge.blockage, copy._evidence_list)
            print("P(Blockage {} | {}) = {}\n".format(edge.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))


    def query(self):
        inp = reasoning_menu()
        if inp is 2:
            self.print_flood_in_all_vertices()
        elif inp is 1:
            self.print_evacuees_in_all_vertices()
        elif inp is 3:
            self.print_blocked_of_all_edges()
        elif inp is 4:
            path = str(input("Please insert the wanted path by the edges separated by white-space\n"))
            path = path.split(' ')
            path = list(map(int, list(path)))
            self.path_free_of_blockages(path)
        else:
            print('Please learn how to read')

    def reset_evidence_list(self):
        for vertex in self._vertices:
            vertex.reset()
        for edge in self._edges:
            edge.reset()
        self._evidence_list = []

    def add_evidence(self):
        evidence_type, vertex = evidence_menu()
        if evidence_type is EVIDENCE_TYPE_FLOOD:
            self._vertices[vertex].flood_reported()
            self._evidence_list.append((self._vertices[vertex].flood_p, True))
        elif evidence_type is EVIDENCE_TYPE_NOT_FLOOD:
            self._vertices[vertex].flood_reported(False)
            self._evidence_list.append((self._vertices[vertex].flood_p, False))
        elif evidence_type is EVIDENCE_TYPE_EVACUESS:
            self._vertices[vertex].evacuees_reported()
            self._evidence_list.append((self._vertices[vertex].evacuees, True))
        elif evidence_type is EVIDENCE_TYPE_NOT_EVACUESS:
            self._vertices[vertex].evacuees_reported(False)
            self._evidence_list.append((self._vertices[vertex].evacuees, False))
        elif evidence_type is EVIDENCE_TYPE_BLOCKAGE:
            self._edges[vertex].blockage_reported()
            self._evidence_list.append((self._edges[vertex].blockage, True))
        elif evidence_type is EVIDENCE_TYPE_NOT_BLOCKAGE:
            self._edges[vertex].blockage_reported(False)
            self._evidence_list.append((self._edges[vertex].blockage, False))
        else:
            print('Please learn how to read')

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
            print('Please learn how to read')
        return True
