
def find_min_in_queue(queue):
    best = queue[0]
    idx = 0
    for i in range(1, len(queue)):
        if queue[i][1] < best[1]:
            best = queue[i]
            idx = i
    return idx


def dijkstra_shortest_path(grid, start, goal):
    """
    Based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

    :param grid: a 2D array of weights
    :param start: the starting index
    :param goal:  the goal index
    :return: the shortest path from  the starting index to the goal. [-1] if does not exist
    """
    q = []
    closed_q = []
    q.append((start, 0))
    path = []
    while len(q):
        i = find_min_in_queue(q)
        v = q.pop(i)
        path.append(v)
        if v[0] == goal:
            return path
        closed_q.append(v[0])
        for i, edge in enumerate(grid[v[0]]):
            if i in closed_q:
                continue
            if edge != -1:
                q.append((i, edge + v[1]))
    return [-1]





if __name__ == '__main__':
    grid = [[0, 1, -1, -1], [1, 0, 4, 8], [-1, 4, 0, 3], [-1, 8, 3, 0]]
    s = 0
    goal = 3
    for row in grid:
        print(row)

    path = dijkstra_shortest_path(grid, s, goal)
    print(path)