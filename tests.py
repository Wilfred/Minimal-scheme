#!/usr/bin/env python

import sys
import unittest
from evaluator import eval_program, variables, load_standard_library, load_built_ins

assert sys.version.startswith('3.'), "Python 3 required"


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        load_built_ins()
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

    def test_character(self):
        program = "#\\a"
        self.assertEvaluatesTo(program, 'a')

        program = "#\\newline"
        self.assertEvaluatesTo(program, '\n')


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

        program = "((lambda () 1))"
        self.assertEvaluatesTo(program, 1)

    def test_begin(self):
        program = "(begin (define n 1) (+ n 3))"

        self.assertEvaluatesTo(program, 4)

    def test_comment(self):
        program = "; 1"

        self.assertEvaluatesTo(program, None)


class EquivalenceTest(InterpreterTest):
    def test_eqv(self):
        program = "(eqv? 1 1)"
        self.assertEvaluatesTo(program, True)

        program = "(eqv? (quote foo) (quote foo))"
        self.assertEvaluatesTo(program, True)

        program = "(eqv? car car)"
        self.assertEvaluatesTo(program, True)

        program = "(eqv? (quote ()) (quote ()))"
        self.assertEvaluatesTo(program, True)

        program = "(eqv? (cons 1 2) (cons 1 2))"
        self.assertEvaluatesTo(program, False)

    def test_eq(self):
        program = "(eq? (quote foo) (quote foo))"
        self.assertEvaluatesTo(program, True)

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

    def test_pair(self):
        program = "(pair? (quote (a b)))"
        self.assertEvaluatesTo(program, True)

        program = "(pair? (quote ()))"
        self.assertEvaluatesTo(program, False)

class MathsTest(InterpreterTest):
    def test_addition(self):
        program = "(+ 1 2 3)"
        self.assertEvaluatesTo(program, 6)

        program = "(+)"
        self.assertEvaluatesTo(program, 0)

    def test_subtraction(self):
        program = "(- 1 2 3)"
        self.assertEvaluatesTo(program, -4)

        program = "(- 2)"
        self.assertEvaluatesTo(program, -2)

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

    def test_equality(self):
        program = "(= 0 0)"

        self.assertEvaluatesTo(program, True)

    # remaining tests in this class are library code:
    def test_zero_predicate(self):
        program = "(zero? 0)"

        self.assertEvaluatesTo(program, True)

    def test_positive_predicate(self):
        program = "(positive? 1)"
        self.assertEvaluatesTo(program, True)

    def test_negative_predicate(self):
        program = "(negative? (- 1))"
        self.assertEvaluatesTo(program, True)

class CharacterTest(InterpreterTest):
    def test_char_predicate(self):
        program = "(char? #\\a)"
        self.assertEvaluatesTo(program, True)

        program = "(char? 0)"
        self.assertEvaluatesTo(program, False)

    def test_equality(self):
        program = "(char=? #\\  #\\space)"
        self.assertEvaluatesTo(program, True)

    def test_char_less_than(self):
        program = "(char<? #\\A #\\B)"
        self.assertEvaluatesTo(program, True)

    def test_char_greater_than(self):
        program = "(char>? #\\1 #\\0)"
        self.assertEvaluatesTo(program, True)

    def test_char_less_or_equal(self):
        program = "(char<=? #\\z #\\z)"
        self.assertEvaluatesTo(program, True)

    def test_char_greater_or_equal(self):
        program = "(char>=? #\\( #\\()"
        self.assertEvaluatesTo(program, True)

if __name__ == '__main__':
    unittest.main()
