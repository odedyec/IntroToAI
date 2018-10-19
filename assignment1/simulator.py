
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
        return SET_EDGE_WEIGHT, (int(s_line[1])-1, int(s_line[2])-1, int(s_line[3]))
    if "#D" in line:
        return SET_DEADLINE, (int(s_line[1]))


def print_as_matrix(mat, title):
    print("")
    print(title)
    print("------------------------")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in mat]))


class Edge:
    def __init__(self):
        self.weight = 0
        self.is_safe = False
        self.num_of_people = 0


class HurricaneSimulator:
    def __init__(self, init_state, config_file=None):
        self.graph = []
        self.num_of_vertices = 0
        self.deadline = 0
        self.time = 0
        self.state = init_state
        self.people_in_vehicle = 0
        self.load_from_file(config_file)
        self.add_people_to_vehicle()
        self.num_of_actions = 0

    def no_op(self):
        self.num_of_actions += 1
        self.time += 1

    def add_people_to_vehicle(self):
        self.people_in_vehicle += self.graph[self.state][self.state].num_of_people
        self.graph[self.state][self.state].num_of_people = 0

    def time_cost(self, new_state, K):
        return self.graph[self.state][new_state].weight * (1 + K * self.people_in_vehicle)

    def traverse(self, new_state, K):
        self.num_of_actions += 1
        self.time += self.time_cost(new_state, K)
        self.state = new_state
        if self.graph[new_state][new_state].is_safe:
            self.people_in_vehicle = 0
        else:
            self.add_people_to_vehicle()

    def load_from_file(self, file_path=None):
        if file_path is None:
            file_path = "input_graph.txt"
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
                        self.graph[args[0]][args[1]].weight = args[2]  # undirected graph
                        self.graph[args[1]][args[0]].weight = args[2]
                    elif op == SET_VERTIX_INFO:
                        if args[1][0] == "P":
                            self.graph[args[0]][args[0]].num_of_people = int(args[1][1])
                        else:
                            self.graph[args[0]][args[0]].is_safe = True
                    elif op == SET_DEADLINE:
                        self.deadline = args
                except:
                    print(line)

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

    def get_state(self):
        return self.state

    def get_deadline(self):
        return self.deadline

    def get_time(self):
        return self.time

    def print_people(self):
        print_as_matrix(self.get_people(), "people")

    def print_shelter(self):
        print_as_matrix(self.get_shelter(), "shelter")

    def print_weights(self):
        print_as_matrix(self.get_weights(), "weights")

    def print_all(self):
        self.print_people()
        self.print_shelter()
        self.print_weights()
        print("\nDeadline in: ", self.deadline)


if __name__ == '__main__':
    hs = HurricaneSimulator(0)
