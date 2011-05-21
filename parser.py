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

# unlike a normal list, using ' only permits one argument
list : ( listarguments )
     | QUOTESUGAR sexpression

listarguments : sexpression listarguments
              |

atom : SYMBOL | NUMBER | BOOLEAN | CHARACTER | STRING

"""

# now, parse an expression and build a parse tree:

class Atom(object):
    def __init__(self, item_type, value):
        self.type = item_type # type is a reserved word
        self.value = value

    def __repr__(self):
        return "<Atom: %s (%s)>" % (str(self.value), self.type)

    def __eq__(self, other):
        if isinstance(other, Atom):
            if other.type == self.type and other.value == self.value:
                return True

        return False

    def get_python_equivalent(self):
        return self.value


class Cons(Sequence):
    @staticmethod
    def from_list(python_list):
        if not python_list:
            return Nil()
        else:
            head = python_list[0]
            tail = Cons.from_list(python_list[1:])
            return Cons(head, tail)

    def __init__(self, head, tail=None):
        self.head = head

        if tail:
            self.tail = tail
        else:
            self.tail = Nil()
            

    def __len__(self):
        return 1 + self.tail.__len__()

    def __getitem__(self, index):
        if index == 0:
            return self.head
        else:
            return self.tail.__getitem__(index - 1)

    def __setitem__(self, index, value):
        if index == 0:
            self.head = value
        else:
            return self.tail.__setitem__(index - 1, value)

    def __repr__(self):
        return "<Cons: %s>" % str(self.get_python_equivalent())

    def __bool__(self):
        # a cons represents is a non-empty list, which we treat as true
        return True

    def get_python_equivalent(self):
        if hasattr(self.head, "get_python_equivalent"):
            python_list = [self.head.get_python_equivalent()]
        else:
            python_list = [self.head]

        if hasattr(self.tail, 'type'):
            # is an improper list, so self.tail is an Atom
            return python_list + ['.', self.tail.get_python_equivalent()]
        else:
            # normal list
            return python_list + self.tail.get_python_equivalent()


class Nil(Sequence):
    # the empty list for our linked list structure
    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise IndexError

    def __setitem__(self, index, value):
        raise IndexError

    def __repr__(self):
        return "<Nil>"

    def __bool__(self):
        return False

    def __eq__(self, other):
        # a Nil is always equal to a Nil
        if isinstance(other, Nil):
            return True
        return False

    def get_python_equivalent(self):
        return []


def p_program(p):
    "program : sexpression program"
    p[0] = Cons(p[1], p[2])

def p_program_empty(p):
    "program :"
    p[0] = Nil()

def p_sexpression_atom(p):
    "sexpression : atom"
    p[0] = p[1]

def p_sexpression_list(p):
    "sexpression : list"
    p[0] = p[1]

def p_list(p):
    "list : LPAREN listarguments RPAREN"
    p[0] = p[2]

def p_list_quotesugar(p):
    "list : QUOTESUGAR sexpression"
    # convert 'foo to (quote foo)
    p[0] = Cons(Atom('SYMBOL', "quote"), Cons(p[2]))

def p_listarguments_one(p):
    "listarguments : sexpression listarguments"
    # a list is therefore a nested tuple:
    p[0] = Cons(p[1], p[2])

def p_listargument_empty(p):
    "listarguments :"
    p[0] = Nil()

def p_atom_symbol(p):
    "atom : SYMBOL"
    p[0] = Atom('SYMBOL', p[1])

def p_atom_number(p):
    "atom : INTEGER"
    p[0] = Atom('INTEGER', p[1])

def p_atom_floating_point(p):
    "atom : FLOATING_POINT"
    p[0] = Atom('FLOATING_POINT', p[1])

def p_atom_boolean(p):
    "atom : BOOLEAN"
    p[0] = Atom('BOOLEAN', p[1])

def p_atom_character(p):
    "atom : CHARACTER"
    p[0] = Atom('CHARACTER', p[1])

def p_atom_string(p):
    "atom : STRING"
    p[0] = Atom('STRING', p[1])


parser = ply.yacc.yacc()
