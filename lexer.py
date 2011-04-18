import ply.lex

tokens = ('LPAREN', 'RPAREN', 'SYMBOL', 'INTEGER', 'BOOLEAN', 'FLOATING_POINT', 'COMMENT', 'CHARACTER')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SYMBOL = r'[a-zA-Z*+/!?=<>.-]+'

def t_FLOATING_POINT(t):
    r"([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)"
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'\#t|\#f'
    if t.value == "#t":
        t.value = True
    else:
        t.value = False

    return t

def t_CHARACTER(t):
    r'\#\\(space|newline|.)'
    # throw away leading #\
    t.value = t.value[2:]

    if t.value == 'space':
        t.value = ' '
    elif t.value == 'newline':
        t.value = '\n'

    return t

def t_COMMENT(t):
    r";[^\n]*"
    # throw away all comments during lexing
    pass

t_ignore = ' \t\n'

lexer = ply.lex.lex()

