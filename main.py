#!/usr/bin/env python3

import sys
import os
import cmd

from lexer import lexer
from evaluator import eval_program, load_standard_library, load_built_ins
from errors import InterpreterException

class Repl(cmd.Cmd):
    intro = "Welcome to Minimal Scheme 0.1 alpha."
    prompt = "scheme> "

    def __init__(self, initial_environment):
        self.environment = initial_environment
        super().__init__()

    def onecmd(self, program):
        if program == 'EOF':
            print() # for tidyness' sake
            sys.exit(0)

        try:
            result, self.environment = eval_program(program, self.environment)

            if not result is None:
                if hasattr(result, "get_python_equivalent"):
                    # is an atom or list
                    print(result.get_python_equivalent())
                else:
                    # function object
                    print(result)

        except InterpreterException as e:
            print("Error: %s" % e.message)


if __name__ == '__main__':
    environment = {}
    environment = load_built_ins(environment)
    environment = load_standard_library(environment)

    if len(sys.argv) > 1:
        # program file passed in
        path = os.path.abspath(sys.argv[1])
        program = open(path, 'r').read()

        try:
            eval_program(program, environment)
        except InterpreterException as e:
            print("Error: %s" % e.message)

    else:
        # interactive mode
        Repl(environment).cmdloop()
