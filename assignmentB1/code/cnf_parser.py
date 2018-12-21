from statements_axioms_variables import *


def get_predicates(line):
    return line.replace('V','').replace('v', '').split(' ')


def get_predicat_and_vars(name):
    is_not = False
    if '!' in name:
        is_not = True
        name = name.replace('!', '')
    res = name.replace(')', '').split('(')
    return is_not, res[0], res[1].split(',')


def create_variable(var=''):
    if var[0].islower():
        v = Variable(symbolic=var)
    else:
        v = Variable(symbolic=var, var=var)
    return v


def is_var_in_list(var, list_of_vars):
    for v in list_of_vars:
        if v.symbol == var:
            return True
    return False


def get_var_idx_in_list(var, list_of_vars):
    for i, v in enumerate(list_of_vars):
        if v.symbol == var:
            return i


def create_predicat_from_string(predicat, list_of_vars):
    is_not, pred_name, variables = get_predicat_and_vars(predicat)
    idx_list_for_predicat = []
    for v in variables:
        if not is_var_in_list(v, list_of_vars):
            list_of_vars.append(create_variable(v))
        idx = get_var_idx_in_list(v, list_of_vars)
        idx_list_for_predicat.append(idx)
    return Predicat(pred_name, [list_of_vars[i] for i in idx_list_for_predicat], is_not)

def parser(file_name):
    list_of_axioms = []
    with open(file_name) as f:
        list_of_vars = []
        for line in f:
            list_of_predicats = []
            for predicat in get_predicates(line.replace('\n', '')):
                if predicat == '': continue
                list_of_predicats.append(create_predicat_from_string(predicat, list_of_vars))
            list_of_axioms.append(Axiom(list_of_predicats))
    return list_of_axioms



if __name__ == '__main__':
    axioms = parser("cnf.txt")
    for a in axioms:
        print str(a)