from scheme_parser import parser
from data_types import Atom, Symbol, BuiltInFunction
from errors import (UndefinedVariable, SchemeTypeError, SchemeStackOverflow,
                    SchemeSyntaxError)
from built_ins import built_ins
from copy import deepcopy

def load_built_ins(environment):

    # a built-in differs from primitives: it always has all its arguments evaluated
    # it also doesn't need the global scope, so we don't pass it for code brevity
    def arguments_evaluated(function):
        def decorated_function(arguments, _environment):
            arguments = deepcopy(arguments)
            # evaluate the arguments, then pass them to the function
            for i in range(len(arguments)):
                (arguments[i], _environment) = eval_s_expression(arguments[i], _environment)

            return (function(arguments), _environment)

        return decorated_function

    for (function_name, function) in built_ins.items():
        built_in_function = BuiltInFunction(arguments_evaluated(function),
                                            function_name)
        
        environment[function_name] = built_in_function

    return environment


def load_standard_library(environment):
    with open('standard_library/library.scm') as library_file:
        library_code = library_file.read()
        _, environment = eval_program(library_code, environment)

    return environment


def eval_program(program, initial_environment):
    if initial_environment:
        environment = initial_environment
    else:
        environment = {}

    # a program is a linked list of s-expressions
    s_expressions = parser.parse(program)

    if not s_expressions:
        return (None, environment)

    result = None

    for s_expression in s_expressions:
        result, environment = eval_s_expression(s_expression, environment)

    return (result, environment)


def eval_s_expression(s_expression, environment):
    if isinstance(s_expression, Atom):
        return eval_atom(s_expression, environment)
    else:
        try:
            return eval_list(s_expression, environment)
        except RuntimeError as e:
            if e.args[0].startswith("maximum recursion depth exceeded"):
                raise SchemeStackOverflow()
            else:
                raise e


def eval_list(linked_list, environment):
    if not linked_list:
        raise SchemeSyntaxError("() is not syntactically valid.")

    # find the function/primitive we are calling
    function, environment = eval_s_expression(linked_list[0], environment)

    if isinstance(function, Atom):
        raise SchemeTypeError("You can only call functions, but "
                              "you gave me a %s." % function.__class__)

    # call it (internally we require the function to decide whether or
    # not to evaluate the arguments)
    return function(linked_list.tail, environment)

def eval_atom(atom, environment):
    # with the exception of symbols, atoms evaluate to themselves
    if isinstance(atom, Symbol):
        return eval_symbol(atom.value, environment)
    else:
        return (atom, environment)

def eval_symbol(symbol_string, environment):

    if symbol_string in primitives:
        # We don't allow primitives to be overridden.
        return (primitives[symbol_string], environment)

    elif symbol_string in environment:
        return (environment[symbol_string], environment)

    elif symbol_string in built_ins:
        return (built_ins[symbol_string], environment)

    else:
        raise UndefinedVariable('%s has not been defined (environment: %s).' % (symbol_string, sorted(environment.keys())))

# this import has to be after eval_s_expression to avoid circular import issues
from primitives import primitives
