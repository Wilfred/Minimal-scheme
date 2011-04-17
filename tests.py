#!/usr/bin/env python

import sys
import unittest
from evaluator import eval_program, variables, load_standard_library

assert sys.version.startswith('3.'), "Python 3 required"


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        load_standard_library()

    def assertEvaluatesTo(self, program, expected_result):
        internal_result = eval_program(program)

        if internal_result:
            result = internal_result.get_python_equivalent()
        else:
            result = None
        
        self.assertEqual(result, expected_result)

class LexerText(InterpreterTest):
    def test_integer(self):
        program = "3"
        result = eval_program(program).get_python_equivalent()

        self.assertEqual(result, 3)
        self.assertEqual(type(result), int)

    def test_floating_point(self):
        program = "2.0"
        result = eval_program(program).get_python_equivalent()

        self.assertEqual(result, 2.0)
        self.assertEqual(type(result), float)

    def test_boolean(self):
        program = "#t"
        result = eval_program(program).get_python_equivalent()

        self.assertEqual(result, True)
        self.assertEqual(type(result), bool)


class EvaluatorTest(InterpreterTest):
    def test_variable_evaluation(self):
        program = "(define y 28) y"

        self.assertEvaluatesTo(program, 28)

    def test_procedure_call(self):
        program = "((if #f + *) 3 4)"

        self.assertEvaluatesTo(program, 12)

    def test_if_two_arguments(self):
        program = "(if #t 1)"

        self.assertEvaluatesTo(program, 1)

    def test_if_three_arguments(self):
        program = "(if #t 2 3)"

        self.assertEvaluatesTo(program, 2)

    def test_variable_assignment(self):
        program = "(define x 1) (set! x 2) x"

        self.assertEvaluatesTo(program, 2)

    def test_function_definition(self):
        program = "(define (z) 1) (z)"

        self.assertEvaluatesTo(program, 1)

    def test_variadic_function_definition(self):
        program = "(define (foo . args) 1) (foo)"

        self.assertEvaluatesTo(program, 1)

    def test_lambda(self):
        program = "((lambda (x) (+ x x)) 4)"

        self.assertEvaluatesTo(program, 8)

    def test_comment(self):
        program = "; 1"

        self.assertEvaluatesTo(program, None)

class ListTest(InterpreterTest):
    def test_car(self):
        program = "(car (quote (1 2 3)))"
        self.assertEvaluatesTo(program, 1)

    def test_cdr(self):
        program = "(cdr (quote (1 2 3)))"
        self.assertEvaluatesTo(program, [2, 3])

    def test_cons(self):
        program = "(cons 1 (quote (2 3)))"
        self.assertEvaluatesTo(program, [1, 2, 3])

        program = "(cons 1 2)"
        self.assertEvaluatesTo(program, [1, '.', 2])

class MathsTest(InterpreterTest):
    def test_addition(self):
        program = "(+ 1 2 3)"
        self.assertEvaluatesTo(program, 6)

        program = "(+)"
        self.assertEvaluatesTo(program, 0)

    def test_multiplication(self):
        program = "(* 2 2 3)"
        self.assertEvaluatesTo(program, 12)

        program = "(*)"
        self.assertEvaluatesTo(program, 1)

    def test_division(self):
        program = "(/ 8)"
        self.assertEvaluatesTo(program, 0.125)

        program = "(/ 12 3 2)"
        self.assertEvaluatesTo(program, 2)

    def test_less_than(self):
        program = "(< 1 1)"
        self.assertEvaluatesTo(program, False)

        program = "(< 1 2 4)"
        self.assertEvaluatesTo(program, True)

    def test_greater_than(self):
        program = "(> 1 1)"
        self.assertEvaluatesTo(program, False)

        program = "(> 11 10 0)"
        self.assertEvaluatesTo(program, True)

    def test_zero_predicate(self):
        program = "(zero? 0)"

        self.assertEvaluatesTo(program, True)

    def test_equality(self):
        program = "(= 0 0)"

        self.assertEvaluatesTo(program, True)

if __name__ == '__main__':
    unittest.main()
