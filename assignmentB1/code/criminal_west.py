from cnf_parser import parser, create_predicat_from_string
from kb_handler import KnoledgeBase


if __name__ == '__main__':
    """ Test with new parser """
    l = parser('criminal_west_cnf.txt')
    KB = KnoledgeBase([create_predicat_from_string("!Criminal(West)", [])])
    KB.print_status()
    KB.resolve_axiom_list(l)

