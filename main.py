#!/usr/bin/env python

import sys
import os
import cmd

assert sys.version.startswith('3.'), "Python 3 required"

from lexer import lexer
from evaluator import eval_program, InterpreterException, load_standard_library

class Repl(cmd.Cmd):
    intro = "Welcome to Minimal Scheme 0.1 alpha."
    prompt = "scheme> "

    def onecmd(self, program):
        if program == 'EOF':
            print() # for tidyness' sake
            sys.exit(0)

        try:
            result = eval_program(program)

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
    load_standard_library()

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
        Repl().cmdloop()
