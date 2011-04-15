import ply.lex

tokens = ('LPAREN', 'RPAREN', 'SYMBOL', 'INTEGER', 'BOOLEAN', 'FLOATING_POINT')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SYMBOL = r'[a-zA-Z*+/!?=<>.-]+'
t_INTEGER = r'[0-9]+'
t_FLOATING_POINT = r"([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)"
t_BOOLEAN = r'\#t|\#f'

t_ignore = ' \t\n'

lexer = ply.lex.lex()

