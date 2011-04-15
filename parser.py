import ply.yacc

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

atom : SYMBOL | NUMBER | BOOLEAN

"""

# now, parse an expression and build a parse tree:

class Atom(object):
    def __init__(self, item_type, value):
        self.type = item_type # type is a reserved word
        self.value = value

    def __repr__(self):
        return str(self.value)

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
    p[0] = (p[1], p[2])

def p_listargument_empty(p):
    "listarguments :"
    pass

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

parser = ply.yacc.yacc()
