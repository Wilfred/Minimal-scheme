#!/usr/bin/env python

import sys
import unittest
from evaluator import eval_program

assert sys.version.startswith('3.'), "Python 3 required"


class InterpreterTest(unittest.TestCase):
    def test_variable_evaluation(self):
        program = "(define x 28) x"

        self.assertEqual(eval_program(program), 28)

    def test_procedure_call(self):
        program = "((if #f + *) 3 4)"

        self.assertEqual(eval_program(program), 12)

    def test_if_two_arguments(self):
        program = "(if #t 1)"

        self.assertEqual(eval_program(program), 1)

    def test_if_three_arguments(self):
        program = "(if #t 2 3)"

        self.assertEqual(eval_program(program), 2)


if __name__ == '__main__':
    unittest.main()
