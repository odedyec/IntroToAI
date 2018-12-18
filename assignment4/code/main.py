from my_parser import load_from_file

if __name__ == '__main__':
    ui = load_from_file()
    ui.print_vertices()
    ui.print_edges()
    ui.path_free_of_blockages([1,2,3,4])
    while ui.menu():
        pass
