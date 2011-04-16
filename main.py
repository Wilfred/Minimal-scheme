#!/usr/bin/env python

import sys
import os
import cmd

assert sys.version.startswith('3.'), "Python 3 required"

from lexer import lexer
from evaluator import eval_program, InterpreterException, load_standard_library
from utils import flatten_linked_list

class Repl(cmd.Cmd):
    intro = "Welcome to Minimal Scheme 0.1 alpha."
    prompt = "scheme> "

    def get_external_representation(self, internal_representation):
        if type(internal_representation) == tuple:
            # list
            external_representation = "("

            for element in flatten_linked_list(internal_representation):
                external_representation += self.get_external_representation(element) + ' '

            external_representation = external_representation.rstrip() + ')'

            return external_representation
        else:
            # atom
            return str(internal_representation)

    def onecmd(self, program):
        if program == 'EOF':
            print() # for tidyness' sake
            sys.exit(0)

        try:
            result = eval_program(program)

            if not result is None:
                print(self.get_external_representation(result))

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
