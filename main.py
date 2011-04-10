#!/usr/bin/env python

# Python 3 assumed

from lexer import lexer
from parser import parser
from evaluator import eval_program, InterpreterException

while True:
    try:
        program_text = input('scheme> ')
        parse_tree = parser.parse(program_text)

        # print(parse_tree)

        result = eval_program(parse_tree)

        if not result is None:
            print(result)
        
    except EOFError:
        break
    except InterpreterException as e:
        print("Error: %s" % e.message)
        continue

