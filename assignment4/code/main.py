from parser import load_from_file

if __name__ == '__main__':
    ui = load_from_file()
    ui.print_vertices()
    ui.print_edges()
    while ui.menu():
        pass
