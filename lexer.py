import ply.lex

tokens = ('LPAREN', 'RPAREN', 'SYMBOL', 'NUMBER', 'BOOLEAN')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SYMBOL = r'[a-zA-Z*+/!?=<>.-]+'
t_NUMBER = r'[0-9]+'
t_BOOLEAN = r'\#t|\#f'

t_ignore = ' \t\n'

lexer = ply.lex.lex()

