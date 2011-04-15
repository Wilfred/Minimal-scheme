#!/usr/bin/env python

import sys
import unittest
from evaluator import eval_program, variables

assert sys.version.startswith('3.'), "Python 3 required"


class InterpreterTest(unittest.TestCase):
    def test_variable_evaluation(self):
        program = "(define y 28) y"

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

    def test_variable_assignment(self):
        program = "(define x 1) (set! x 2) x"

        self.assertEqual(eval_program(program), 2)

    def test_function_definition(self):
        program = "(define (z) 1) (z)"

        self.assertEqual(eval_program(program), 1)

    def test_variadic_function_definition(self):
        program = "(define (foo . args) 1) (foo)"

        self.assertEqual(eval_program(program), 1)

    def test_lambda(self):
        program = "((lambda (x) (+ x x)) 4)"

        self.assertEqual(eval_program(program), 8)

class MathsTest(unittest.TestCase):
    def test_less_than(self):
        program = "(< 1 1)"
        self.assertEqual(eval_program(program), False)

        program = "(< 1 2 4)"
        self.assertEqual(eval_program(program), True)

    def test_greater_than(self):
        program = "(> 1 1)"
        self.assertEqual(eval_program(program), False)

        program = "(> 11 10 0)"
        self.assertEqual(eval_program(program), True)


if __name__ == '__main__':
    unittest.main()
