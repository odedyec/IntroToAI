from cnf_parser import parser, create_predicat_from_string, create_axiom_from_line
from kb_handler import KnoledgeBase
from copy import deepcopy


def ui(list_of_axioms):
    print "\n --- What would you like to reolve --- "
    print("0. No way to coninue? ")
    for i, ax in enumerate(list_of_axioms):
        print("{}. {}".format(i+1, ax))
    print("{}. Custom".format(len(list_of_axioms)+1))
    idx = input("\n")
    return int(idx) - 1


def custom_input():
    line = raw_input("Enter an axiom\n")
    return create_axiom_from_line(line)

if __name__ == '__main__':
    """ Test with new parser """
    l = parser('cnfs/hurricane_cnf.txt')
    KB = KnoledgeBase([create_predicat_from_string("Timeup(S6)", [])])
    init_states = parser('cnfs/hurricane_init.txt')
    [KB.unite_axiom(ax) for ax in init_states]
    while not KB.is_query_false():
        idx = ui(l)
        if idx == -1:
            print("\n--------------\nQuery can not be disproven\n------------\n")
            break
        if idx == len(l):
            KB.resolve(custom_input(), True)
        elif KB.resolve(deepcopy(l[idx]), True) is False:
                print("\n==============\nCONTRADICTION\nQuery is True\n==============\n")
                exit(0)
    if KB.is_query_false():
        print("\n==============\nQuery is False\n==============\n")

