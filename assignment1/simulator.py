
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
            return SET_VERTIX_INFO, (int(s_line[1])-1, s_line[2:])
    if "#E" in line:
        return SET_EDGE_WEIGHT, (int(s_line[1])-1, int(s_line[2])-1, s_line[3])
    if "#D" in line:
        return SET_DEADLINE, (int(s_line[1]))


def print_as_matrix(mat):
    print("")
    for row in mat:
        print (row)
    print("")

class Edge:
    def __init__(self):
        self.weight = 0
        self.is_safe = False
        self.num_of_people = 0


class HurricaneSimulator:
    def __init__(self):
        self.graph = []
        self.num_of_vertices = 0
        self.deadline = 0

    def load_from_file(self, file_path="input_graph.txt"):
        with open(file_path) as f:
            for line in f:
                try:
                    if line == '\n': continue
                    op, args = parse_line(line)
                    if op == SET_NUM_OF_VERTICES:
                        for i in range(args):
                            r = list()
                            for j in range(args):
                                r.append(Edge())
                            self.graph.append(r)
                        self.num_of_vertices = args
                    elif op == SET_EDGE_WEIGHT:
                        self.graph[args[0]][args[1]].weight = args[2]
                    elif op == SET_VERTIX_INFO:
                        if args[1][0] == "P":
                            self.graph[args[0]][args[0]].num_of_people = args[1][1]
                        else:
                            self.graph[args[0]][args[0]].is_safe = True
                    elif op == SET_DEADLINE:
                        self.deadline = args
                except:
                    print(line)
        print_as_matrix(self.get_people())
        print_as_matrix(self.get_shelter())
        print_as_matrix(self.get_weights())
        print(self.deadline)

    def get_people(self):
        l = [[0 for i in range(self.num_of_vertices)] for j in range(self.num_of_vertices)]
        for i in range(self.num_of_vertices):
            for j in range(self.num_of_vertices):
                l[i][j] = self.graph[i][j].num_of_people
        return l

    def get_shelter(self):
        l = [[0 for i in range(self.num_of_vertices)] for j in range(self.num_of_vertices)]
        for i in range(self.num_of_vertices):
            for j in range(self.num_of_vertices):
                if self.graph[i][j].is_safe:
                    l[i][j] = 1
        return l

    def get_weights(self):
        l = [[0 for i in range(self.num_of_vertices)] for j in range(self.num_of_vertices)]
        for i in range(self.num_of_vertices):
            for j in range(self.num_of_vertices):
                l[i][j] = self.graph[i][j].weight
        return l

if __name__ == '__main__':
    hs = HurricaneSimulator()
    hs.load_from_file()
