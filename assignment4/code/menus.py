EVIDENCE_TYPE_FLOOD = 1
EVIDENCE_TYPE_NOT_FLOOD = 2
EVIDENCE_TYPE_EVACUESS = 3
EVIDENCE_TYPE_NOT_EVACUESS = 4
EVIDENCE_TYPE_BLOCKAGE = 5
EVIDENCE_TYPE_NOT_BLOCKAGE = 6


def main_menu():
    print '\n\n\n'
    inp = input("1. Reset evidence list to empty.\n"
                "2. Add piece of evidence to evidence list.\n"
                "3. Do probabilistic reasoning (1, 2, 3, 4, or 5, whichever your program supports) and report the results.\n"
                "4. Quit.\n")

    inp = int(inp)
    return inp


def reasoning_menu():
    print '\n\n\n'
    inp = input("1. What is the probability that each of the vertices contains evacuees?\n"
                "2. What is the probability that each of the vertices is flooded?\n"
                "3. What is the probability that each of the edges is blocked?\n"
                "4. What is the probability that a certain path (set of edges) is free from blockages?\n"
                "(Note that the distributions of blockages in edges are NOT necessarily independent.)\n"
                "5. What is the path from a given location to a goal that has the highest probability of being free from blockages? (bonus)\n")
    inp = int(inp)
    return inp


def evidence_menu():
    evidence_type = int(input('\n\n1. There is a flood?\n2. There is no flood?\n3. There are evacuees?\n'
                              '4. There are no evacuees?\n5. There is blockage?\n6. There is no blockage?\n'))
    if evidence_type is EVIDENCE_TYPE_BLOCKAGE or evidence_type is EVIDENCE_TYPE_NOT_BLOCKAGE:
        vertex = int(input("\n\nWhich edge?"))

    else:
        vertex = int(input("\n\nWhich vertex?"))

    return evidence_type, vertex


