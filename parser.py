import ply.yacc
from collections import Sequence

from lexer import tokens

"""Grammar for our minimal scheme:

# a program is a series of s-expressions
program : sexpression program
        |

# an s-expression is a list or an atom
sexpression : atom
            | list

list : ( listarguments )

listarguments : sexp listarguments
              |

atom : SYMBOL | NUMBER | BOOLEAN | CHARACTER

"""

# now, parse an expression and build a parse tree:

class Atom(object):
    def __init__(self, item_type, value):
        self.type = item_type # type is a reserved word
        self.value = value

    def __repr__(self):
        return "<Atom: %s (%s)>" % (str(self.value), self.type)

    def __eq__(self, other):
        if other.type == self.type and other.value == self.value:
            return True

        return False

    def get_python_equivalent(self):
        return self.value


class LinkedListNode(Sequence):
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

    def __len__(self):
        if self.tail is None:
            return 1

        return 1 + self.tail.__len__()

    def __getitem__(self, index):
        if index == 0:
            return self.head

        elif self.tail is None:
            # specified an index greater than the length
            raise IndexError()
        else:
            return self.tail.__getitem__(index - 1)

    def __setitem__(self, index, value):
        if index == 0:
            self.head = value

        elif self.tail is None:
            # specified an index greater than the length
            raise IndexError()
        else:
            return self.tail.__setitem__(index - 1, value)

    def __repr__(self):
        return "<LinkedList: %s>" % str(self.get_python_equivalent())

    def __bool__(self):
        # an empty LinkedList is just None, so we always return True here
        return True

    def index(self, value):
        """Find the first occurrence of value in the list, and return its index.

        """
        if self.head == value:
            return 0

        elif self.tail is None:
            raise ValueError

        else:
            return 1 + self.tail.index(value)


    def get_python_equivalent(self):
        if self.tail is None:
            return [self.head.get_python_equivalent()]
        else:
            python_list = [self.head.get_python_equivalent()]

            if hasattr(self.tail, 'type'):
                # is an improper list, so self.tail is an Atom
                return python_list + ['.', self.tail.get_python_equivalent()]
            else:
                # normal list
                return python_list + self.tail.get_python_equivalent()

def p_program(p):
    "program : sexpression program"
    p[0] = (p[1], p[2])

def p_program_empty(p):
    "program :"
    pass

def p_sexpression_atom(p):
    "sexpression : atom"
    p[0] = p[1]

def p_sexpression_list(p):
    "sexpression : list"
    p[0] = p[1]

def p_list(p):
    "list : LPAREN listarguments RPAREN"
    p[0] = p[2]

def p_listarguments_one(p):
    "listarguments : sexpression listarguments"
    # a list is therefore a nested tuple:
    p[0] = LinkedListNode(head=p[1], tail=p[2])

def p_listargument_empty(p):
    "listarguments :"
    pass

def p_atom_symbol(p):
    "atom : SYMBOL"
    p[0] = Atom('SYMBOL', p[1])

def p_atom_number(p):
    "atom : INTEGER"
    p[0] = Atom('INTEGER', int(p[1]))

def p_atom_floating_point(p):
    "atom : FLOATING_POINT"
    p[0] = Atom('FLOATING_POINT', float(p[1]))

def p_atom_boolean(p):
    "atom : BOOLEAN"
    if p[1] == '#t':
        p[0] = Atom('BOOLEAN', True)
    else:
        p[0] = Atom('BOOLEAN', False)

def p_atom_character(p):
    "atom : CHARACTER"
    p[0] = Atom('CHARACTER', p[1])


parser = ply.yacc.yacc()
