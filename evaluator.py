from parser import parser, Atom, LinkedListNode
from errors import (InterpreterException, UndefinedVariable, RedefinedVariable,
                    SchemeTypeError, SchemeSyntaxError)
from built_ins import built_ins
from utils import safe_len, safe_iter
from copy import deepcopy

def load_built_ins(environment):

    # a built in differs from primitives: it always has all its arguments evaluated
    def arguments_evaluated(function):
        def decorated_function(arguments, _environment):
            arguments = deepcopy(arguments)
            # evaluate the arguments, then pass them to the function
            for i in range(safe_len(arguments)):
                (arguments[i], _environment) = eval_s_expression(arguments[i], _environment)

            return function(arguments, _environment)

        return decorated_function

    for (function_name, function) in built_ins.items():
        environment[function_name] = arguments_evaluated(function)

    return environment


def load_standard_library(environment):
    with open('library.scm') as library_file:
        library_code = library_file.read()
        eval_program(library_code, environment)

    return environment


def eval_program(program, initial_environment=None):
    if initial_environment:
        environment = initial_environment
    else:
        environment = {}

    # a program is a linked list of s-expressions
    s_expressions = parser.parse(program)

    if not s_expressions:
        return (None, environment)

    result = None

    for s_expression in safe_iter(s_expressions):
        result, environment = eval_s_expression(s_expression, environment)

    return (result, environment)


def eval_s_expression(s_expression, environment):
    if isinstance(s_expression, LinkedListNode):
        return eval_list(s_expression, environment)
    else:
        return eval_atom(s_expression, environment)


def eval_list(linked_list, environment):
    # find the function/primitive we are calling
    function, environment = eval_s_expression(linked_list.head, environment)

    # call it (internally we require the function to decide whether or
    # not to evalue the arguments)
    return function(linked_list.tail, environment)

def eval_atom(atom, environment):
    # with the exception of symbols, atoms evaluate to themselves
    if atom.type == 'SYMBOL':
        return eval_symbol(atom.value, environment)
    else:
        return (atom, environment)

def eval_symbol(symbol_string, environment):
    if symbol_string == 'define':

        def define(arguments, _environment):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to "
                                      "`define` (you passed %d)." % safe_len(arguments))

            if isinstance(arguments.head, Atom):
                # variable assignment
                if arguments.head.type != 'SYMBOL':
                    raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % arguments.head.type)

                if arguments.head.value in environment:
                    raise RedefinedVariable("Cannot define %s, as it has already been defined." % arguments.head.value)

                variable_name = arguments.head.value
                variable_value_expression = arguments.tail.head

                result, _environment = eval_s_expression(variable_value_expression, _environment)
                _environment[variable_name] = result

                return (None, _environment)

            else:
                # function definition
                function_name_with_parameters = arguments.head
                function_name = function_name_with_parameters.head

                if function_name.type != "SYMBOL":
                    raise SchemeTypeError("Function names must be symbols, not a %s." % function_name.type)

                # check that all our arguments are symbols:
                function_parameters = function_name_with_parameters.tail

                for parameter in safe_iter(function_parameters):
                    if parameter.type != "SYMBOL":
                        raise SchemeTypeError("Function arguments must be symbols, not a %s." % parameter.type)

                function_body = arguments.tail.head

                # check if this function can take a variable number of arguments
                is_variadic = False

                for parameter in safe_iter(function_parameters):
                    if parameter.value == '.':
                        if is_variadic:
                            raise SchemeSyntaxError("May not have . more than once in a parameter list.")
                        else:
                            is_variadic = True

                if is_variadic:
                    dot_position = function_parameters.index(Atom('SYMBOL', '.'))

                    if dot_position < len(function_parameters) - 2:
                        raise SchemeSyntaxError("You can only have one improper list "
                                                "(you have %d parameters after the '.')." % (len(function_parameters) - 1 - dot_position))
                    if dot_position == len(function_parameters) - 1:
                        raise SchemeSyntaxError("Must name an improper list parameter after '.'.")

                def named_variadic_function(arguments, _environment):
                    # a function that takes a variable number of arguments
                    if dot_position == 0:
                        explicit_parameters = None
                    else:
                        explicit_parameters = deepcopy(function_parameters)

                        # create a linked list holding all the parameters before the dot
                        current_head = explicit_parameters

                        # find the position in the list just before the dot
                        for i in range(dot_position - 2):
                            current_head = current_head.tail

                        # then remove the rest of the list
                        current_head.tail = None

                    improper_list_parameter = function_parameters[dot_position + 1]

                    # check we have been given sufficient arguments for our explicit parameters
                    if safe_len(arguments) < safe_len(explicit_parameters):
                        raise SchemeTypeError("%s takes at least %d arguments, you only provided %d." % \
                                                  (function_name.value, safe_len(explicit_parameters),
                                                   safe_len(arguments)))

                    local_environment = {}

                    for (parameter, parameter_expression) in zip(safe_iter(explicit_parameters),
                                                                 safe_iter(arguments)):
                        local_environment[parameter.value], _environment = eval_s_expression(parameter_expression, _environment)

                    # put the remaining arguments in our improper parameter
                    if arguments:
                        local_environment[improper_list_parameter.value] = arguments[safe_len(explicit_parameters)]

                    new_environment = dict(_environment, **local_environment)

                    # evaluate our function_body in this environment
                    (result, final_environment) = eval_s_expression(function_body, new_environment)

                    # update global variables that weren't masked by locals
                    for variable_name in _environment:
                        if variable_name not in local_environment:
                            _environment[variable_name] = final_environment[variable_name]

                    return (result, _environment)

                def named_function(arguments, _environment):
                    if safe_len(arguments) != safe_len(function_parameters):
                        raise SchemeTypeError("%s takes %d arguments, %d given." % \
                                                  (function_name, safe_len(function_parameters), safe_len(arguments)))

                    local_environment = {}

                    # evaluate arguments in current environment
                    for (parameter_name, parameter_expression) in zip(safe_iter(function_parameters),
                                                                      safe_iter(arguments)):
                        local_environment[parameter_name.value], _environment = eval_s_expression(parameter_expression, _environment)

                    # create new environment, where local variables mask globals
                    new_environment = dict(_environment, **local_environment)

                    # evaluate the function block
                    result, final_environment = eval_s_expression(function_body, new_environment)

                    # update any global variables that weren't masked
                    for variable_name in _environment:
                        if variable_name not in local_environment:
                            _environment[variable_name] = final_environment[variable_name]

                    return (result, _environment)

                # assign this function to this name
                if is_variadic:
                    _environment[function_name.value] = named_variadic_function
                else:
                    _environment[function_name.value] = named_function

                return (None, _environment)

        return (define, environment)

    elif symbol_string == 'set!':

        def set_variable(arguments, _environment):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `set!`.")

            variable_name = arguments.head

            if variable_name.type != 'SYMBOL':
                raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % variable_name.type)

            if variable_name.value not in environment:
                raise UndefinedVariable("Can't assign to undefined variable %s." % variable_name.value)

            variable_value_expression = arguments.tail.head
            result, _environment = eval_s_expression(variable_value_expression, _environment)
            _environment[variable_name.value] = result

            return (None, _environment)

        return (set_variable, environment)

    elif symbol_string == 'if':

        def if_function(arguments, _environment):
            if safe_len(arguments) not in [2,3]:
                raise SchemeTypeError("Need to pass either two or three arguments to `if`.")

            condition, _environment = eval_s_expression(arguments.head, _environment)

            # everything except an explicit false boolean is true
            if not (condition.type == 'BOOLEAN' and condition.value == False):
                then_expression = arguments[1]
                return eval_s_expression(then_expression, _environment)
            else:
                if safe_len(arguments) == 3:
                    else_expression = arguments[2]
                    return eval_s_expression(else_expression, _environment)

        return (if_function, environment)

    elif symbol_string == 'lambda':

        def make_lambda_function(arguments, _environment):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `lambda`.")

            parameter_list = arguments.head
            function_body = arguments.tail.head

            if isinstance(parameter_list, Atom):
                raise SchemeTypeError("The first argument to `lambda` must be a list of variables.")

            for parameter in safe_iter(parameter_list):
                if parameter.type != "SYMBOL":
                    raise SchemeTypeError("Parameters of lambda functions must be symbols, not %s." % parameter.type)

            def lambda_function(_arguments, __environment):
                if safe_len(_arguments) != safe_len(parameter_list):
                    raise SchemeTypeError("Wrong number of arguments for this "
                                          "lambda function, was expecting %d, received %d" % (safe_len(parameter_list), safe_len(_arguments)))

                local_environment = {}

                for (parameter_name, parameter_expression) in zip(safe_iter(parameter_list),
                                                                  safe_iter(_arguments)):
                    local_environment[parameter_name.value], __environment = eval_s_expression(parameter_expression, __environment)

                new_environment = dict(__environment, **local_environment)

                # now we have set up the correct scope, evaluate our function block
                (result, final_environment) = eval_s_expression(function_body, new_environment)

                # update any global variables that weren't masked
                for variable_name in __environment:
                    if variable_name not in local_environment:
                        __environment[variable_name] = final_environment[variable_name]

                return (result, __environment)

            return (lambda_function, _environment)

        return (make_lambda_function, environment)

    elif symbol_string == 'quote':

        def return_argument_unevaluated(arguments, _environment):
            if safe_len(arguments) != 1:
                raise SchemeTypeError("Quote takes exactly one argument, received %d" % safe_len(arguments))

            return (arguments.head, _environment)

        return (return_argument_unevaluated, environment)

    elif symbol_string == 'begin':

        def evaluate_sequence(arguments, _environment):
            result = None

            for argument in arguments:
                result, _environment = eval_s_expression(argument, _environment)

            return (result, _environment)

        return (evaluate_sequence, environment)

    elif symbol_string in environment:

        return (environment[symbol_string], environment)

    else:

        raise UndefinedVariable('%s has not been defined (environment: %s).' % (symbol_string, sorted(environment.keys())))
