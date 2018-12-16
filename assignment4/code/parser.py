"""
Parser
"""
from graph import Graph
SET_NUM_OF_VERTICES = 0
SET_EDGE_WEIGHT = 1
SET_VERTIX_INFO = 2
SET_DEADLINE = 3


def parse_line(line):
    line = line.split(';')[0]
    s_line = line.split()
    if "#V" in line:
        if len(s_line) == 2:
            return SET_NUM_OF_VERTICES, (int(s_line[1]))
        else:
            return SET_VERTIX_INFO, (int(s_line[1]), s_line[2], float(s_line[3]))
    if "#E" in line:
        return SET_EDGE_WEIGHT, (int(s_line[1]), int(s_line[2]), float(s_line[3]), int(''.join(filter(str.isdigit, s_line[0]))))
    if "#D" in line:
        return SET_DEADLINE, (int(s_line[1]))


def load_from_file(file_path=None):
    if file_path is None:
        file_path = "input_graph.txt"
    graph = None
    with open(file_path) as f:
        for line in f:
            try:
                if line == '\n': continue
                op, args = parse_line(line)
                if op == SET_NUM_OF_VERTICES:
                    num_of_vertices = args
                    graph = Graph(num_of_vertices)
                elif op == SET_EDGE_WEIGHT:
                    graph.set_edge(args[0], args[1], args[2], args[3])
                elif op == SET_VERTIX_INFO:
                    if args[1] == "F":
                        graph.set_vertex_flood(args[0], args[2])
                    else:
                        raise Exception("Unknown input")
                elif op == SET_DEADLINE:
                    deadline = args
            except:
                print(line)
    return graph


if __name__ == '__main__':
    g = load_from_file()
    g.print_vertices()
    g.print_edges()

