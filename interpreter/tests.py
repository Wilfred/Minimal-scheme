#!/usr/bin/env python3

import unittest
import sys
from io import StringIO

from evaluator import eval_program, load_standard_library, load_built_ins
from errors import (SchemeTypeError, SchemeStackOverflow, SchemeSyntaxError,
                    SchemeArityError)
from data_types import (Vector, Cons, Nil, Integer, Boolean, String,
                        Character, FloatingPoint)


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        self.environment = {}
        self.environment = load_built_ins(self.environment)
        self.environment = load_standard_library(self.environment)

    def evaluate(self, program):
        internal_result, final_environment = eval_program(program, self.environment)
        return internal_result

    def assertEvaluatesTo(self, program, expected_result):
        result = self.evaluate(program)
        self.assertEqual(result, expected_result)

    def assertEvaluatesAs(self, program, expected_result):
        internal_result = self.evaluate(program)

        if internal_result is None:
            result = Nil()
        else:
            result = internal_result
        
        self.assertEqual(result, expected_result)


class LexerTest(InterpreterTest):
    def test_integer(self):
        program = "3"
        self.assertEvaluatesTo(program, Integer(3))

    def test_floating_point(self):
        program = "2.0"
        self.assertEvaluatesTo(program, FloatingPoint(2.0))

    def test_boolean(self):
        program = "#t"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_character(self):
        program = "#\\a"
        self.assertEvaluatesTo(program, Character('a'))

        program = "#\\newline"
        self.assertEvaluatesTo(program, Character('\n'))

        program = "#\\space"
        self.assertEvaluatesTo(program, Character(' '))

    def test_string(self):
        program = '""'
        self.assertEvaluatesTo(program, String(""))

        program = '" "'
        self.assertEvaluatesTo(program, String(" "))

        program = '" \\" "'
        self.assertEvaluatesTo(program, String(' " '))

        program = '" \\n "'
        self.assertEvaluatesTo(program, String(' \n '))

    def test_invalid(self):
        program = '\\y'
        self.assertRaises(SchemeSyntaxError, eval_program, program, None)


class ParserTest(InterpreterTest):
    def test_mismatched_parens(self):
        program = "("
        self.assertRaises(SchemeSyntaxError, eval_program, program, None)


class EvaluatorTest(InterpreterTest):
    def test_empty_program(self):
        program = ""
        self.assertEvaluatesTo(program, None)

    def test_variable_evaluation(self):
        program = "(define x 28) x"
        self.assertEvaluatesTo(program, Integer(28))

    def test_procedure_call(self):
        program = "((if #f + *) 3 4)"
        self.assertEvaluatesTo(program, Integer(12))

    def test_if_two_arguments(self):
        program = "(if #t 1)"
        self.assertEvaluatesTo(program, Integer(1))

    def test_if_three_arguments(self):
        program = "(if #t 2 3)"
        self.assertEvaluatesTo(program, Integer(2))

    def test_variable_assignment(self):
        program = "(define x 1) (set! x 2) x"
        self.assertEvaluatesTo(program, Integer(2))

    def test_function_definition(self):
        program = "(define (x) 1) (x)"
        self.assertEvaluatesTo(program, Integer(1))

    def test_function_long_body(self):
        program = "(define (x) 1 2) (x)"
        self.assertEvaluatesTo(program, Integer(2))

    def test_variadic_function_long_body(self):
        program = "(define (foo . args) 1 2) (foo)"
        self.assertEvaluatesTo(program, Integer(2))

    def test_variadic_function_definition(self):
        # test that we can put nothing in the impure list parameter
        program = "(define (foo . args) 1) (foo)"
        self.assertEvaluatesTo(program, Integer(1))

        # test that we can put multiple things in the impure list parameter
        program = "(define (f . everything) everything) (f 1 2 3)"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2), Integer(3)]))

        # test that the improper list parameter is evaluated
        program = "(define (g . everything) everything) (g (+ 2 3))"
        self.assertEvaluatesTo(program, Cons(Integer(5)))

    def test_lambda(self):
        program = "((lambda (x) (+ x x)) 4)"
        self.assertEvaluatesTo(program, Integer(8))

        program = "((lambda () 1))"
        self.assertEvaluatesTo(program, Integer(1))

    def test_lambda_long_body(self):
        program = "((lambda () 1 2))"
        self.assertEvaluatesTo(program, Integer(2))

    def test_begin(self):
        program = "(begin)"
        self.assertEvaluatesTo(program, None)

        program = "(begin (define x 1) (+ x 3))"
        self.assertEvaluatesTo(program, Integer(4))

    def test_comment(self):
        program = "; 1"

        self.assertEvaluatesTo(program, None)

    def test_quote(self):
        program = "(quote (1 2 3))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2), Integer(3)]))

        program = "(quote ())"
        self.assertEvaluatesTo(program, Nil())

    def test_quote_sugar(self):
        program = "'(1 2 3)"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2), Integer(3)]))

    def test_type_error(self):
        program = "(2 2)"
        self.assertRaises(SchemeTypeError, eval_program, program, None)

    def test_stack_overflow(self):
        # FIXME: with TCO, this is actually just an infinite loop
        program = "(define (f) (f)) (f)"
        self.assertRaises(SchemeStackOverflow, eval_program, program, None)

    def test_call_empty_list(self):
        program = "()"
        self.assertRaises(SchemeSyntaxError, eval_program, program, None)

    def test_quasiquote(self):
        program = "(quasiquote (1 1))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(1)]))

        program = "(quasiquote (unquote 1))"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(quasiquote (1 (unquote (+ 2 2))))"
        self.assertEvaluatesTo(program, Cons(Integer(1), Cons(Integer(4))))

        program = "(quasiquote (1 (unquote-splicing '(2 2))))"
        self.assertEvaluatesTo(program, Cons(Integer(1), Cons(Integer(2), Cons(Integer(2)))))

    def test_quasiquote_sugar(self):
        program = "`,1"
        self.assertEvaluatesTo(program, Integer(1))

        program = "`(1 ,@'(2 2))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2), Integer(2)]))


class EquivalenceTest(InterpreterTest):
    def test_eqv(self):
        program = "(eqv? 1 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(eqv? (quote foo) (quote foo))"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(eqv? car car)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(eqv? (quote ()) (quote ()))"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(eqv? (cons 1 2) (cons 1 2))"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_eq(self):
        program = "(eq? (quote foo) (quote foo))"
        self.assertEvaluatesTo(program, Boolean(True))


class ListTest(InterpreterTest):
    def test_car(self):
        program = "(car (quote (1 2 3)))"
        self.assertEvaluatesTo(program, Integer(1))

    def test_cdr(self):
        program = "(cdr (quote (1 2 3)))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(2), Integer(3)]))

        program = "(cdr (quote (1 2 3)) 1)"
        with self.assertRaises(SchemeArityError):
            self.evaluate(program)

    def test_car_cdr_compositions(self):
        program = "(caar '((1 3) 2))"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(cadr '((1 3) 2))"
        self.assertEvaluatesTo(program, Integer(2))

        program = "(cdar '((1 3) 2))"
        self.assertEvaluatesTo(program, Cons(Integer(3)))

        program = "(cddr '((1 3) 2))"
        self.assertEvaluatesTo(program, Nil())

    def test_set_car(self):
        program = "(define x (list 4 5 6)) (set-car! x 1) x"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(5), Integer(6)]))

    def test_set_cdr(self):
        program = "(define x (list 4 5 6)) (set-cdr! x 1) x"
        result = self.evaluate(program)
        self.assertEqual(result, Cons(Integer(4), Integer(1)))

    def test_cons(self):
        program = "(cons 1 (quote (2 3)))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2), Integer(3)]))

        program = "(cons 1 2)"
        self.assertEvaluatesTo(program, Cons(Integer(1), Integer(2)))

    def test_null(self):
        program = "(null? 1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(null? '())"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(null? '(1 2))"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_is_list(self):
        program = "(list? '())"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(list? 1)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_list(self):
        program = "(list)"
        self.assertEvaluatesTo(program, Nil())

        program = "(list 1 (+ 2 3))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(5)]))

    def test_length(self):
        program = "(length '())"
        self.assertEvaluatesTo(program, Integer(0))

        program = "(length (cons 2 (cons 3 '())))"
        self.assertEvaluatesTo(program, Integer(2))

    def test_pair(self):
        program = "(pair? (quote (a b)))"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(pair? (quote ()))"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(pair? 1)"
        self.assertEvaluatesTo(program, Boolean(False))


class ControlTest(InterpreterTest):
    def test_is_procedure(self):
        program = "(procedure? car)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(procedure? 1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(procedure? (lambda (x) (+ x 1)))"
        self.assertEvaluatesTo(program, Boolean(True))
    
    def test_map(self):
        program = "(map (lambda (x) (+ x 1)) '(2 3))"
        self.assertEvaluatesTo(program, Cons(Integer(3), Cons(Integer(4))))

    def test_for_each(self):
        program = """(let ((total 0))
     (for-each
        (lambda (x) (set! total (+ total x)))
        '(1 2 3))
     total)"""
        self.assertEvaluatesTo(program, Integer(6))


class MathsTest(InterpreterTest):
    def test_addition(self):
        program = "(+ 1 2 3)"
        self.assertEvaluatesTo(program, Integer(6))

        program = "(+)"
        self.assertEvaluatesTo(program, Integer(0))

        program = "(+ 1 2.5)"
        self.assertEvaluatesTo(program, FloatingPoint(3.5))

    def test_subtraction(self):
        program = "(- 1 2 3)"
        self.assertEvaluatesTo(program, Integer(-4))

        program = "(- 2)"
        self.assertEvaluatesTo(program, Integer(-2))

        program = "(- 0.1)"
        self.assertEvaluatesTo(program, FloatingPoint(-0.1))

        program = "(- 10.0 0.5)"
        self.assertEvaluatesTo(program, FloatingPoint(9.5))

    def test_multiplication(self):
        program = "(* 2 2 3)"
        self.assertEvaluatesTo(program, Integer(12))

        program = "(*)"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(* 3 0.5)"
        self.assertEvaluatesTo(program, FloatingPoint(1.5))

    def test_division(self):
        program = "(/ 8)"
        self.assertEvaluatesTo(program, FloatingPoint(0.125))

        program = "(/ 12 3 2)"
        self.assertEvaluatesTo(program, Integer(2))

    def test_less_than(self):
        program = "(< 1 1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(< 1 2 4)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_less_or_equal(self):
        program = "(<= 1 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(<= 1 0)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_greater_than(self):
        program = "(> 1 1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(> 11 10 0)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_greater_or_equal(self):
        program = "(>= 1 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(>= 1 3 2)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_equality(self):
        program = "(=)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(= 0)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(= 0 0)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(= 0 1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(= 1.0 1)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_number(self):
        program = "(number? 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(number? 1.0)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(number? #\\a)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_complex(self):
        program = "(complex? 0)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_rational(self):
        program = "(rational? 1.1)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_real(self):
        program = "(real? 1.2)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_exact(self):
        program = "(exact? 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(exact? 1.0)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_inexact(self):
        program = "(inexact? 0)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(inexact? 0.0)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_quotient(self):
        program = "(quotient 3 2)"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(quotient 4 2)"
        self.assertEvaluatesTo(program, Integer(2))

        program = "(quotient -13 4)"
        self.assertEvaluatesTo(program, Integer(-3))

    def test_modulo(self):
        program = "(modulo 4 2)"
        self.assertEvaluatesTo(program, Integer(0))

        program = "(modulo 5 2)"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(modulo -13 4)"
        self.assertEvaluatesTo(program, Integer(3))

    def test_remainder(self):
        program = "(remainder 4 2)"
        self.assertEvaluatesTo(program, Integer(0))

        program = "(remainder 5 2)"
        self.assertEvaluatesTo(program, Integer(1))

        program = "(remainder -13 4)"
        self.assertEvaluatesTo(program, Integer(-1))

        program = "(remainder 13 -4)"
        self.assertEvaluatesTo(program, Integer(1))

    def test_exp(self):
        program = "(exp 0)"
        self.assertEvaluatesTo(program, FloatingPoint(1.0))

        program = "(exp 2)"
        self.assertEvaluatesTo(program, FloatingPoint(7.38905609893065))

    def test_log(self):
        program = "(log 1)"
        self.assertEvaluatesTo(program, FloatingPoint(0.0))

        program = "(log 7.38905609893065)"
        self.assertEvaluatesTo(program, FloatingPoint(2.0))

class LibraryMathsTest(InterpreterTest):
    def test_zero_predicate(self):
        program = "(zero? 0)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_positive_predicate(self):
        program = "(positive? 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(positive? -1)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(positive? 0)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_negative_predicate(self):
        program = "(negative? -1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(negative? 3)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_odd_predicate(self):
        program = "(odd? 1)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(odd? 0)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_even_predicate(self):
        program = "(even? 6)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(even? 7)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_abs(self):
        program = "(abs -5.1)"
        self.assertEvaluatesTo(program, FloatingPoint(5.1))

        program = "(abs 0.2)"
        self.assertEvaluatesTo(program, FloatingPoint(0.2))


class CharacterTest(InterpreterTest):
    def test_char_predicate(self):
        program = "(char? #\\a)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(char? 0)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(char? (quote (x)))"
        self.assertEvaluatesTo(program, Boolean(False))
    def test_equality(self):
        program = "(char=? #\\  #\\space)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_char_less_than(self):
        program = "(char<? #\\A #\\B)"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_char_greater_than(self):
        program = "(char>? #\\1 #\\0)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(char>? #\\0 #\\0)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(char>? #\\0 #\\1)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_char_less_or_equal(self):
        program = "(char<=? #\\y #\\z)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(char<=? #\\z #\\z)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(char<=? #\\z #\\y)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_char_greater_or_equal(self):
        program = "(char>=? #\\y #\\z)"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(char>=? #\\( #\\()"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(char>=? #\\z #\\y)"
        self.assertEvaluatesTo(program, Boolean(True))


class StringTest(InterpreterTest):
    def test_string_predicate(self):
        program = '(string? "foo")'
        self.assertEvaluatesTo(program, Boolean(True))

        program = '(string? (quote ("foo")))'
        self.assertEvaluatesTo(program, Boolean(False))

    def test_make_string(self):
        program = '(make-string 2)'
        self.assertEvaluatesTo(program, String("  "))

        program = '(make-string 2 #\\a)'
        self.assertEvaluatesTo(program, String("aa"))

        program = '(make-string 0 #\\a)'
        self.assertEvaluatesTo(program, String(""))

    def test_string_length(self):
        program = '(string-length "")'
        self.assertEvaluatesTo(program, Integer(0))

        program = '(string-length "abcdef")'
        self.assertEvaluatesTo(program, Integer(6))

    def test_string_ref(self):
        program = '(string-ref "abc" 2)'
        self.assertEvaluatesTo(program, Character('c'))

    def test_string_set(self):
        program = '(define s "abc") (string-set! s 0 #\z) s'
        self.assertEvaluatesTo(program, String('zbc'))


class BooleanTest(InterpreterTest):
    def test_not(self):
        program = '(not #f)'
        self.assertEvaluatesTo(program, Boolean(True))

        program = '(not \'())'
        self.assertEvaluatesTo(program, Boolean(False))

    def test_is_boolean(self):
        program = "(boolean? #t)"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(boolean? 1)"
        self.assertEvaluatesTo(program, Boolean(False))

    def test_and(self):
        program = "(and (= 2 2) (> 2 1))"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(and \"foo\" \"bar\")"
        self.assertEvaluatesTo(program, String("bar"))

    def test_or(self):
        program = "(or (= 2 3) (> 2 1))"
        self.assertEvaluatesTo(program, Boolean(True))

        program = "(or (= 2 3) (> 1 2))"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(or \"foo\" \"bar\")"
        self.assertEvaluatesTo(program, String("foo"))


class VectorTest(InterpreterTest):
    def test_make_vector(self):
        program = '(make-vector 0)'
        self.assertEvaluatesAs(program, Vector(0))

        program = '(make-vector 2)'
        self.assertEvaluatesAs(program, Vector(2))

    def test_make_vector_with_init(self):
        program = '(make-vector 1 3)'
        self.assertEvaluatesAs(program, Vector.from_list([Integer(3)]))

    def test_is_vector(self):
        program = "(vector? '())"
        self.assertEvaluatesTo(program, Boolean(False))

        program = "(vector? (make-vector 1))"
        self.assertEvaluatesTo(program, Boolean(True))

    def test_vector_set(self):
        program = "(let ((v (make-vector 1))) (vector-set! v 0 5) v)"
        self.assertEvaluatesAs(program, Vector.from_list([Integer(5)]))

    def test_vector_ref(self):
        program = "(let ((v (make-vector 1))) (vector-set! v 0 5) (vector-ref v 0))"
        self.assertEvaluatesTo(program, Integer(5))

    def test_vector_length(self):
        program = "(vector-length (make-vector 5))"
        self.assertEvaluatesTo(program, Integer(5))

    def test_vector(self):
        program = "(vector 1 2)"
        self.assertEvaluatesAs(
            program,
            Vector.from_list([Integer(1), Integer(2)]))

    def test_vector_to_list(self):
        program = "(vector->list (vector 1 2))"
        self.assertEvaluatesTo(program, Cons.from_list([Integer(1), Integer(2)]))

    def test_list_to_vector(self):
        program = "(list->vector (list 1 2))"
        self.assertEvaluatesAs(
            program,
            Vector.from_list([Integer(1), Integer(2)]))

    def test_vector_fill(self):
        program = "(let ((v (make-vector 1))) (vector-fill! v 5) v)"
        self.assertEvaluatesAs(
            program,
            Vector.from_list([Integer(5)]))


class IOTest(InterpreterTest):
    def setUp(self):
        super().setUp()
        self.saved_stdout = sys.stdout

        self.fake_stdout = StringIO()
        sys.stdout = self.fake_stdout

    def tearDown(self):
        sys.stdout = self.saved_stdout

    def test_display(self):
        program = '(display "hello")'
        eval_program(program, self.environment)

        self.assertEqual(sys.stdout.getvalue(), "hello")
        
    def test_newline(self):
        program = '(newline)'
        eval_program(program, self.environment)

        self.assertEqual(sys.stdout.getvalue(), "\n")
        

class MacroTest(InterpreterTest):
    """Test macro definition, but also test syntax defined in the
    standard library using macros.
    
    """
    def test_defmacro(self):
        program = '(defmacro inc (argument) `(+ 1 ,argument)) (inc 5)'
        self.assertEvaluatesTo(program, Integer(6))

    def test_let(self):
        program = "(let ((x 1)) x)"
        self.assertEvaluatesTo(program, Integer(1))

    def test_let_last_argument(self):
        program = "(let ((x 1)) 2 x)"
        self.assertEvaluatesTo(program, Integer(1))

    def test_cond(self):
        program = "(cond ((else 1)))"
        self.assertEvaluatesTo(program, Integer(1))
    
        program = "(define x 1) (cond (((> x 0) 3) (else 1)))"
        self.assertEvaluatesTo(program, Integer(3))
    
        program = "(define y 1) (cond (((< y 0) 3) (else 1)))"
        self.assertEvaluatesTo(program, Integer(1))
    

if __name__ == '__main__':
    unittest.main()
