from statements_axioms_variables import *


class KnoledgeBase(Axiom):
    def is_query_false(self):
        if len(self.predicats) == 0:
            return True
        return False

    def print_status(self):
        if self.is_query_false():
            print("\n==============\nQuery is False\n==============\n")
        else:
            for i in range(len(self.predicats)):
                print(str(self.predicats[i])),

                if i == len(self.predicats) - 1: continue

                print('V'),

            print('')

    def pretty_print_resolve(self, obj):
        print("\n----------------\nResolving   "),
        print(str(obj)),
        print("  With   "),
        self.print_status()
        print("Result    "),

    def resolve(self,obj, obj_is_axiom=False):
        self.pretty_print_resolve(obj)
        res, KB = self.unite(obj, obj_is_axiom)
        if res is False:
            KB.print_status()
            print("\n==============\nCONTRADICTION\nQuery is True\n==============\n")
        self.predicats = KB.predicats
        self.remove_similar()

    def remove_similar(self):
        list_to_remove = []
        for i in range(len(self.predicats)):
            for j in range(i+1, len(self.predicats)):
                if self.predicats[i] == self.predicats[j]:
                    list_to_remove.append(i)
                    break
        for idx in list_to_remove:
            self.predicats.pop(idx)
