
def find_closest(list_of_vertices):
    """ This auxiliary function helps finding the closest result from the search grid list"""
    closest = None
    for vertex in list_of_vertices:
        if closest is None:
            closest = vertex
        else:
            if closest[1] > vertex[1]:
                closest = vertex
    return closest


def sum_of_people(list_of_people):
    sum_val = 0
    for row in list_of_people:
        for i in row:
            sum_val += i
    return sum_val