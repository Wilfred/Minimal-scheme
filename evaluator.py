from parser import parser, Atom, LinkedListNode
from errors import (InterpreterException, UndefinedVariable, RedefinedVariable,
                    SchemeTypeError, SchemeSyntaxError)
from built_ins import built_ins
from utils import safe_len, safe_iter
from copy import deepcopy

variables = {}

def load_built_ins():
    # a built in differs from primitives: it always has all its arguments evaluated
    def arguments_evaluated(function):
        def decorated_function(arguments):
            for i in range(safe_len(arguments)):
                arguments[i] = eval_s_expression(arguments[i])

            return function(arguments)

        return decorated_function

    for (function_name, function) in built_ins.items():
        variables[function_name] = arguments_evaluated(function)

def load_standard_library():
    with open('library.scm') as library_file:
        library_code = library_file.read()
        eval_program(library_code)


def eval_program(program):
    # a program is a linked list of s-expressions
    s_expressions = parser.parse(program)

    if not s_expressions:
        return

    result = None
    for s_expression in safe_iter(s_expressions):
        result = eval_s_expression(s_expression)

    return result


def eval_s_expression(s_expression):
    if isinstance(s_expression, LinkedListNode):
        return eval_list(s_expression)
    else:
        return eval_atom(s_expression)


def eval_list(linked_list):
    # find the function we are calling
    function = eval_s_expression(linked_list.head)

    # call it (we require the function to decide whether or not to
    # evalue the arguments)
    return function(linked_list.tail)

def eval_atom(atom):
    # with the exception of symbols, atoms evaluate to themselves
    if atom.type == 'SYMBOL':
        return eval_symbol(atom.value)
    else:
        return atom

def eval_symbol(symbol_string):
    if symbol_string == 'define':

        def define(arguments):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to "
                                      "`define` (you passed %d)." % safe_len(arguments))

            if isinstance(arguments.head, Atom):
                # variable assignment
                if arguments.head.type != 'SYMBOL':
                    raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % arguments.head.type)

                if arguments.head.value in variables:
                    raise RedefinedVariable("Cannot define %s, as it has already been defined." % arguments.head.value)

                variable_value_expression = arguments.tail.head
                variables[arguments.head.value] = eval_s_expression(variable_value_expression)

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

                def named_variadic_function(arguments):
                    if dot_position == 0:
                        explicit_parameters = None
                    else:
                        explicit_parameters = deepcopy(function_parameters)

                        # create a linked list holding all the parameters before the dot
                        current_head = explicit_parameters
                        for i in range(dot_position - 2):
                            current_head = current_head.tail

                        current_head.tail = None

                    improper_list_parameter = function_parameters[dot_position + 1]

                    # check we have been given sufficient arguments for our explicit parameters
                    if safe_len(arguments) < safe_len(explicit_parameters):
                        raise SchemeTypeError("%s takes at least %d arguments, you only provided %d." % \
                                                  (function_name.value, safe_len(explicit_parameters),
                                                   safe_len(arguments)))

                    # assign to all our parameters
                    global variables
                    global_variables = variables.copy()

                    for (parameter, parameter_expression) in zip(safe_iter(explicit_parameters),
                                                                 safe_iter(arguments)):
                        variables[parameter.value] = eval_s_expression(parameter_expression)

                    # put the remaining arguments in our improper parameter
                    if arguments:
                        variables[improper_list_parameter.value] = arguments[safe_len(explicit_parameters)]

                    # evaluate our function_body in this environment
                    result = eval_s_expression(function_body)

                    # reset the environment
                    variables = global_variables

                    return result

                def named_function(arguments):
                    if safe_len(arguments) != safe_len(function_parameters):
                        raise SchemeTypeError("%s takes %d arguments, %d given." % \
                                                  (function_name, safe_len(function_parameters), safe_len(arguments)))

                    # create function scope by saving old environment
                    global variables
                    global_variables = variables.copy()

                    # evaluate arguments
                    for (parameter_name, parameter_expression) in zip(safe_iter(function_parameters),
                                                                      safe_iter(arguments)):
                            variables[parameter_name.value] = eval_s_expression(parameter_expression)

                    # evaluate the function block
                    result = eval_s_expression(function_body)

                    # restore old environment
                    variables = global_variables

                    return result

                # assign this function to this name
                if is_variadic:
                    variables[function_name.value] = named_variadic_function
                else:
                    variables[function_name.value] = named_function

        return define

    elif symbol_string == 'set!':

        def set_variable(arguments):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `set!`.")

            variable_name = arguments.head

            if variable_name.type != 'SYMBOL':
                raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % variable_name.type)

            if variable_name.value not in variables:
                raise UndefinedVariable("Can't assign to undefined variable %s." % variable_name.value)

            variable_value_expression = arguments.tail.head
            variables[variable_name.value] = eval_s_expression(variable_value_expression)

        return set_variable

    elif symbol_string == 'if':

        def if_function(arguments):
            if safe_len(arguments) not in [2,3]:
                raise SchemeTypeError("Need to pass either two or three arguments to `if`.")

            condition = eval_s_expression(arguments.head)

            # everything except an explicit false boolean is true
            if not (condition.type == 'BOOLEAN' and condition.value == False):
                then_expression = arguments[1]
                return eval_s_expression(then_expression)
            else:
                if safe_len(arguments) == 3:
                    else_expression = arguments[2]
                    return eval_s_expression(else_expression)

        return if_function

    elif symbol_string == 'lambda':

        def make_lambda_function(arguments):
            if safe_len(arguments) != 2:
                raise SchemeTypeError("Need to pass exactly two arguments to `lambda`.")

            parameter_list = arguments.head
            function_body = arguments.tail.head

            if isinstance(parameter_list, Atom):
                raise SchemeTypeError("The first argument to `lambda` must be a list of variables.")

            for parameter in safe_iter(parameter_list):
                if parameter.type != "SYMBOL":
                    raise SchemeTypeError("Parameters of lambda functions must be symbols, not %s." % parameter.type)

            def lambda_function(_arguments):
                if safe_len(_arguments) != safe_len(parameter_list):
                    raise SchemeTypeError("Wrong number of arguments for this "
                                          "lambda function, was expecting %d, received %d" % (safe_len(parameter_list), safe_len(_arguments)))

                # save the global scope variables elsewhere so we can restore them
                global variables
                global_variables = variables.copy()

                for (parameter_name, parameter_expression) in zip(safe_iter(parameter_list),
                                                                  safe_iter(_arguments)):
                    variables[parameter_name.value] = eval_s_expression(parameter_expression)

                # now we have set up the correct scope, evaluate our function block
                result = eval_s_expression(function_body)

                # now restore the original environment
                variables = global_variables

                return result

            return lambda_function

        return make_lambda_function

    elif symbol_string == 'quote':

        def return_argument_unevaluated(arguments):
            if safe_len(arguments) != 1:
                raise SchemeTypeError("Quote takes exactly one argument, received %d" % safe_len(arguments))

            return arguments.head

        return return_argument_unevaluated

    elif symbol_string == 'begin':

        def evaluate_sequence(arguments):
            result = None

            for argument in arguments:
                result = eval_s_expression(argument)

            return result

        return evaluate_sequence

    elif symbol_string in variables:

        return variables[symbol_string]

    else:

        raise UndefinedVariable('%s has not been defined (environment: %s).' % (symbol_string, variables))
