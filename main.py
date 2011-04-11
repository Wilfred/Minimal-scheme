#!/usr/bin/env python

import sys
import os

assert sys.version.startswith('3.'), "Python 3 required"

from lexer import lexer
from parser import parser
from evaluator import eval_program, InterpreterException

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # program file passed in
        path = os.path.abspath(sys.argv[1])
        program = open(path, 'r').read()

        try:
            eval_program(program)
        except InterpreterException as e:
            print("Error: %s" % e.message)

    else:
        # interactive mode
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
