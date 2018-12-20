from statements_axioms_variables import *
from kb_handler import KnoledgeBase


if __name__ == '__main__':
    """ A1 """
    x = Variable(symbolic='x')
    y = Variable(symbolic='y')
    z = Variable(symbolic='z')
    ax1 = Axiom(
        [Predicat('American', [x]), Predicat('Weapon', [y]), Predicat('Sells', [x, y, z]), Predicat('Hostile', [z]),
         Predicat('Criminal', [x], is_not=False)])

    """ A2 """
    x2 = Variable(symbolic='x2')
    ax2 = Axiom([Predicat('Missile', [x2]), Predicat('Weapon', [x2], is_not=False)])

    """ A3 """
    x3 = Variable(symbolic='x3')
    west = Variable(symbolic='West', var="West")
    missile = Variable(symbolic='y', var='M1')
    nono = Variable(symbolic='Nono', var='Nono')
    ax3 = Axiom([Predicat('Missile', [x3]), Predicat('Owns', [nono, x3]), Predicat('Sells', [west, x3, nono], is_not=False)])

    """ A4 """
    x4 = Variable(symbolic='x4')
    america = Variable(symbolic='America', var='America')
    ax4 = Axiom([Predicat('Enemy', [x4, america]), Predicat('Hostile', [x4], is_not=False)])

    """ KB """
    query = [Predicat('Criminal', [west], is_not=True)]
    KB = KnoledgeBase(query)
    """ Start solving """
    KB.resolve(ax1, obj_is_axiom=True)
    KB.print_status()

    KB.resolve(Predicat('American', [west], is_not=False))
    KB.print_status()

    KB.resolve(ax2, obj_is_axiom=True)
    KB.print_status()

    KB.resolve(Predicat('Missile', [missile], is_not=False))
    KB.print_status()

    KB.resolve(ax3, obj_is_axiom=True)
    KB.print_status()

    KB.resolve(Predicat('Missile', [missile], is_not=False))
    KB.print_status()

    owns = Predicat('Owns', [nono, missile], is_not=False)
    KB.resolve(owns)
    KB.print_status()

    KB.resolve(ax4, obj_is_axiom=True)
    KB.print_status()

    enemy = Predicat('Enemy', [nono, america], is_not=False)
    KB.resolve(enemy)
    KB.print_status()

