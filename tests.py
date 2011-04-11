#!/usr/bin/env python

import sys
import unittest
from evaluator import eval_program

assert sys.version.startswith('3.'), "Python 3 required"


class InterpreterTest(unittest.TestCase):
    def test_variable_evaluation(self):
        program = "(define x 28) x"

        self.assertEqual(eval_program(program), 28)



if __name__ == '__main__':
    unittest.main()
