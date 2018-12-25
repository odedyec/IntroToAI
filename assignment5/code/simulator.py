"""
Simulator class
"""
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
            return SET_VERTIX_INFO, (int(s_line[1]), s_line[2:])
    if "#E" in line:
        return SET_EDGE_WEIGHT, (int(s_line[1]), int(s_line[2]), int(s_line[3]))
    if "#D" in line:
        return SET_DEADLINE, (int(s_line[1]))


def load_from_file(file_path=None):
    if file_path is None:
        file_path = "input_graph.txt"
    graph = []
    with open(file_path) as f:
        for line in f:
            try:
                if line == '\n': continue
                op, args = parse_line(line)
                if op == SET_NUM_OF_VERTICES:
                    for i in range(args):
                        r = list()
                        for j in range(args):
                            r.append(Vertex())
                        graph.append(r)
                    num_of_vertices = args
                elif op == SET_EDGE_WEIGHT:
                    graph[args[0]][args[1]].weight = args[2]  # undirected graph
                    graph[args[1]][args[0]].weight = args[2]
                elif op == SET_VERTIX_INFO:
                    if args[1][0] == "P":
                        graph[args[0]][args[0]].num_of_people = int(args[1][1])
                    else:
                        graph[args[0]][args[0]].is_safe = True
                elif op == SET_DEADLINE:
                    deadline = args
            except:
                print(line)

class Simulator:
    def __init__(self):
        self.test = 'hello'

    def __str__(self):
        return self.test