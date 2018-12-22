def result(predicat):
    if predicat.name != 'Result':
        raise Exception("the result should only get a Result(a, s) predicat")
    state = predicat.vars[1].var
    num_s = state[1:]
    num_i = int(num_s)
    new_state = 'S'+str(num_i+1)
    return new_state


class Variable:
    def __init__(self, var=None, symbolic=''):
        self.var = var
        self.symbol = symbolic

    def __str__(self):
        if self.var is None:
            return self.symbol
        return str(self.var) if type(self.var) is int else self.var

    def __add__(self, other):
        if type(self.var) is int and type(other.var) is int:
            self.var += other.var
        else:
            raise Exception("Trying to add two non numeric vars")


class Predicat:
    def __init__(self, name, vars, is_not=True):
        self.name = name
        self.vars = vars
        self.is_not = is_not

    def __str__(self):
        s = '~' if self.is_not else ''
        s += self.name +'('
        for i, var in enumerate(self.vars):
            s += str(var)
            if i != len(self.vars)-1:
                s += ','
        return s + ')'

    def __neg__(self):
        self.is_not = not self.is_not

    def substitute(self, vars):
        vars_to_replace = []
        for i in range(len(self.vars)):
            if vars[i].var is None and self.vars[i].var is None:
                vars_to_replace.append((self.vars[i], vars[i]))  # (old_var, new_var)
            elif self.vars[i].var is None:
                self.vars[i].var = vars[i].var
            elif vars[i].var is None:
                    vars[i].var = self.vars[i].var
            elif vars[i].var == self.vars[i].var:
                continue
            else:
                return False
        return vars_to_replace if len(vars_to_replace) else True

    def is_complement(self, predicat):
        if self.name == predicat.name and predicat.is_not is not self.is_not:
            return True
        return False


class Axiom:
    def __init__(self, list_of_predicats):
        self.predicats = list_of_predicats

    def __str__(self):
        s = ''
        for i in range(len(self.predicats)):
            s += str(self.predicats[i])
            if i == len(self.predicats) - 1: continue
            s += ' V '
        return s

    def add_predicat(self, predicat):
        self.predicats.append(predicat)

    def is_complement_predicat_exist(self, predicat):
        for pred in self.predicats:
            if pred.is_complement(predicat):
                return True
        return False

    def unite(self, obj, obj_is_axiom=False):
        if obj_is_axiom:
            return self.unite_axiom(obj)
        return self.unite_predicat(obj)

    def unite_axiom(self, axiom):
        new_predicats = []
        res = True
        for predicat in axiom.predicats:
            if predicat.name == 'Plus':
                predicat.vars[2].var = predicat.vars[0].var + predicat.vars[1].var
            elif predicat.name == 'Result':
                predicat.vars[2].var = result(predicat)
            elif predicat.name == 'Greater':
                if predicat.vars[0].var > predicat.vars[1].var:
                    p = Predicat("Timeup", predicat.vars[2], is_not=False)
                else:
                    p = Predicat("Timeup", [predicat.vars[2]], is_not=True)
                res = self.unite_predicat(p)
            elif self.is_complement_predicat_exist(predicat):
                res = self.unite_predicat(predicat)
                if res is False: return res, None
            else:
                new_predicats.append(predicat)
        for pred in new_predicats:
            self.add_predicat(pred)
        return res

    def unite_predicat(self, predicat):
        new_list = []
        var = None
        for pred in self.predicats:
            if pred.is_complement(predicat):
                res = pred.substitute(predicat.vars)
                if res is False:
                    return False
                else:
                    var = res
            else:
                new_list.append(pred)
        if type(var) is list:
            for it in var:
                for p in new_list:
                    for i in range(len(p.vars)):
                        if p.vars[i] is it[0]:
                            p.vars[i] = it[1]
        self.predicats = Axiom(new_list).predicats
        return True

    def print_axiom(self):
        if len(self.predicats) == 0:
            print("\n==============\nQuery is False\n==============\n")
            return
        print(str(self))

