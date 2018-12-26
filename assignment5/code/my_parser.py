"""
Parser
"""
from graph import Graph
SET_NUM_OF_VERTICES = 0
SET_EDGE_WEIGHT = 1
SET_VERTEX_EVACUEES = 2
SET_DEADLINE = 3
SET_EDGE_BLOCKAGE = 4
SET_START = 5
SET_SHELTER = 6


def parse_line(line):
    line = line.split(';')[0]
    s_line = line.split()
    if "#V" in line:
        if len(s_line) == 2:
            return SET_NUM_OF_VERTICES, (int(s_line[1]))
        else:
            if "Ev" in s_line:
                return SET_VERTEX_EVACUEES, (int(s_line[1]), int(s_line[3]))
    if "#E" in line:
        if "B" in s_line:
            return SET_EDGE_WEIGHT, (int(s_line[1]), int(s_line[2]), int(s_line[3]), int(''.join(filter(str.isdigit, s_line[0]))), float(s_line[5]))
        else:
            return SET_EDGE_WEIGHT, (
            int(s_line[1]), int(s_line[2]), int(s_line[3]), int(''.join(filter(str.isdigit, s_line[0]))), 0.)
    if "#Deadline" in line:
        return SET_DEADLINE, [int(s_line[1])]
    if "#Start" in line:
        return SET_START, [int(s_line[1])]
    if "#Shelter" in line:
        return SET_SHELTER, [int(s_line[1])]


def load_from_file(file_path=None, obj=Graph):
    if file_path is None:
        file_path = "input_graph.txt"
    graph = None
    with open(file_path) as f:
        for line in f:
            if line == '\n': continue
            op, args = parse_line(line)
            if op == SET_NUM_OF_VERTICES:
                num_of_vertices = args
                graph = obj(num_of_vertices)
            elif op == SET_EDGE_WEIGHT:
                graph.set_edge(args[0], args[1], args[2], args[3], args[4])
            elif op == SET_VERTEX_EVACUEES:
                graph.set_vertex_ev(args[0], args[1])
            elif op == SET_DEADLINE:
                graph.deadline = args[0]
            elif op == SET_START:
                graph.set_loc(args[0])
            elif op == SET_SHELTER:
                graph.set_vertex_is_shelter(args[0])

    return graph


if __name__ == '__main__':
    g = load_from_file()
    print str(g)

