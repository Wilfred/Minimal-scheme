import ply.yacc

from lexer import tokens
from data_types import Cons, Nil, Atom

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
     | QUASIQUOTESUGAR sexpression
     | UNQUOTESUGAR sexpression
     | UNQUOTESPLICINGSUGAR sexpression

listarguments : sexpression listarguments
              |

atom : SYMBOL | NUMBER | BOOLEAN | CHARACTER | STRING

"""

# now, parse an expression and build a parse tree:

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

def p_list_quasiquotesugar(p):
    "list : QUASIQUOTESUGAR sexpression"
    # convert `foo to (quasiquote foo)
    p[0] = Cons(Atom('SYMBOL', "quasiquote"), Cons(p[2]))

def p_list_unquotesugar(p):
    "list : UNQUOTESUGAR sexpression"
    # convert ,foo to (unquote foo)
    p[0] = Cons(Atom('SYMBOL', "unquote"), Cons(p[2]))

def p_list_unquotesplicingsugar(p):
    "list : UNQUOTESPLICINGSUGAR sexpression"
    # convert ,foo to (unquote foo)
    p[0] = Cons(Atom('SYMBOL', "unquote-splicing"), Cons(p[2]))

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
