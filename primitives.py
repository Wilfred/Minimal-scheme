from evaluator import eval_s_expression
from errors import SchemeTypeError, RedefinedVariable, SchemeSyntaxError, UndefinedVariable
from parser import Atom, Nil, Cons
from copy import deepcopy
from utils import check_argument_number

primitives = {}

# a decorator for giving a name to built-in
def name_function(function_name):
    def name_function_decorator(function):
        primitives[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return name_function_decorator


@name_function('define')
def define(arguments, environment):
    check_argument_number('define', arguments, 2, 2)

    if isinstance(arguments[0], Atom):
        return define_variable(arguments, environment)
    else:
        return define_function(arguments, environment)


def define_variable(arguments, environment):
    if arguments[0].type != 'SYMBOL':
        raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % arguments[0].type)

    if arguments[0].value in environment:
        raise RedefinedVariable("Cannot define %s, as it has already been defined." % arguments[0].value)

    variable_name = arguments[0].value
    variable_value_expression = arguments[1]

    result, environment = eval_s_expression(variable_value_expression, environment)
    environment[variable_name] = result

    return (None, environment)


def define_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = function_name_with_parameters[0]

    if function_name.type != "SYMBOL":
        raise SchemeTypeError("Function names must be symbols, not a %s." % function_name.type)

    # check that all our arguments are symbols:
    function_parameters = function_name_with_parameters.tail

    for parameter in function_parameters:
        if parameter.type != "SYMBOL":
            raise SchemeTypeError("Function arguments must be symbols, not a %s." % parameter.type)

    # check if this function can take a variable number of arguments
    is_variadic = False

    for parameter in function_parameters:
        if parameter.value == '.':
            if is_variadic:
                raise SchemeSyntaxError("May not have . more than once in a parameter list.")
            else:
                is_variadic = True

    if is_variadic:
        return define_variadic_function(arguments, environment)
    else:
        return define_normal_function(arguments, environment)


def define_normal_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = function_name_with_parameters[0]
    function_parameters = function_name_with_parameters.tail

    function_body = arguments[1]
    
    # a function with a fixed number of arguments
    def named_function(_arguments, _environment):
        check_argument_number(function_name.value, _arguments,
                              len(function_parameters), len(function_parameters))

        local_environment = {}

        # evaluate arguments
        _arguments = deepcopy(_arguments)
        for i in range(len(_arguments)):
            (_arguments[i], _environment) = eval_s_expression(_arguments[i], _environment)

        # assign to parameters
        for (parameter_name, parameter_value) in zip(function_parameters,
                                                     _arguments):
            local_environment[parameter_name.value] = parameter_value

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
    environment[function_name.value] = named_function

    return (None, environment)


def define_variadic_function(arguments, environment):
    function_name_with_parameters = arguments[0]
    function_name = arguments[0][0]
    function_parameters = function_name_with_parameters.tail

    function_body = arguments.tail[0]
    
    dot_position = function_parameters.index(Atom('SYMBOL', '.'))

    if dot_position < len(function_parameters) - 2:
        raise SchemeSyntaxError("You can only have one improper list "
                                "(you have %d parameters after the '.')." % (len(function_parameters) - 1 - dot_position))
    if dot_position == len(function_parameters) - 1:
        raise SchemeSyntaxError("Must name an improper list parameter after '.'.")

    def named_variadic_function(_arguments, _environment):
        # a function that takes a variable number of arguments
        if dot_position == 0:
            explicit_parameters = Nil()
        else:
            explicit_parameters = deepcopy(function_parameters)

            # create a linked list holding all the parameters before the dot
            current_head = explicit_parameters

            # find the position in the list just before the dot
            for i in range(dot_position - 2):
                current_head = current_head.tail

            # then remove the rest of the list
            current_head.tail = Nil()

        improper_list_parameter = function_parameters[dot_position + 1]

        # check we have been given sufficient arguments for our explicit parameters
        check_argument_number(function_name.value, _arguments,
                              len(explicit_parameters))

        local_environment = {}

        # evaluate arguments
        _arguments = deepcopy(_arguments)
        for i in range(len(_arguments)):
            (_arguments[i], _environment) = eval_s_expression(_arguments[i], _environment)

        # assign parameters
        for (parameter, parameter_value) in zip(explicit_parameters,
                                                _arguments):
            local_environment[parameter] = parameter_value

        # put the remaining arguments in our improper parameter
        remaining_arguments = _arguments
        for i in range(len(explicit_parameters)):
            remaining_arguments = remaining_arguments.tail

        local_environment[improper_list_parameter.value] = remaining_arguments

        new_environment = dict(_environment, **local_environment)

        # evaluate our function_body in this environment
        (result, final_environment) = eval_s_expression(function_body, new_environment)

        # update global variables that weren't masked by locals
        for variable_name in _environment:
            if variable_name not in local_environment:
                _environment[variable_name] = final_environment[variable_name]

        return (result, _environment)

    # assign this function to this name
    environment[function_name.value] = named_variadic_function

    return (None, environment)


@name_function('set!')
def set_variable(arguments, environment):
    check_argument_number('set!', arguments, 2, 2)

    variable_name = arguments[0]

    if variable_name.type != 'SYMBOL':
        raise SchemeTypeError("Tried to assign to a %s, which isn't a symbol." % variable_name.type)

    if variable_name.value not in environment:
        raise UndefinedVariable("Can't assign to undefined variable %s." % variable_name.value)

    variable_value_expression = arguments[1]
    result, environment = eval_s_expression(variable_value_expression, environment)
    environment[variable_name.value] = result

    return (None, environment)

@name_function('if')
def if_function(arguments, environment):
    check_argument_number('if', arguments, 2, 3)

    condition, environment = eval_s_expression(arguments[0], environment)

    # everything except an explicit false boolean is true
    if not (condition.type == 'BOOLEAN' and condition.value == False):
        then_expression = arguments[1]
        return eval_s_expression(then_expression, environment)
    else:
        if len(arguments) == 3:
            else_expression = arguments[2]
            return eval_s_expression(else_expression, environment)


@name_function('lambda')
def make_lambda_function(arguments, environment):
    check_argument_number('lambda', arguments, 2, 2)

    parameter_list = arguments[0]
    function_body = arguments[1]

    if isinstance(parameter_list, Atom):
        raise SchemeTypeError("The first argument to `lambda` must be a list of variables.")

    for parameter in parameter_list:
        if parameter.type != "SYMBOL":
            raise SchemeTypeError("Parameters of lambda functions must be symbols, not %s." % parameter.type)

    def lambda_function(_arguments, _environment):
        check_argument_number('(anonymous function)', _arguments,
                              len(parameter_list), len(parameter_list))

        local_environment = {}

        for (parameter_name, parameter_expression) in zip(parameter_list,
                                                          _arguments):
            local_environment[parameter_name.value], _environment = eval_s_expression(parameter_expression, _environment)

        new_environment = dict(_environment, **local_environment)

        # now we have set up the correct scope, evaluate our function block
        (result, final_environment) = eval_s_expression(function_body, new_environment)

        # update any global variables that weren't masked
        for variable_name in _environment:
            if variable_name not in local_environment:
                _environment[variable_name] = final_environment[variable_name]

        return (result, _environment)

    return (lambda_function, environment)


@name_function('quote')
def return_argument_unevaluated(arguments, environment):
    check_argument_number('quote', arguments, 1, 1)

    return (arguments[0], environment)


@name_function('begin')
def evaluate_sequence(arguments, environment):
    result = None

    for argument in arguments:
        result, environment = eval_s_expression(argument, environment)

    return (result, environment)


@name_function('quasiquote')
def quasiquote(arguments, environment):
    """Returns the arguments unevaluated, except for any occurrences
    of unquote.

    """
    def recursive_eval_unquote(s_expression, _environment):
        """Return a copy of s_expression, with all occurrences of
        unquoted s-expressions replaced by their evaluated values.

        """
        if isinstance(s_expression, Atom):
            return (s_expression, _environment)

        elif isinstance(s_expression, Nil):
            return (s_expression, _environment)

        elif s_expression[0] == Atom("SYMBOL", "unquote"):
            check_argument_number('unquote', arguments, 1, 1)
            return eval_s_expression(s_expression[1], _environment)

        else:
            # return a list of s_expressions that have been
            # recursively checked for unquote
            list_elements = []

            for element in s_expression:
                (result, _environment) = recursive_eval_unquote(element, _environment)
                list_elements.append(result)

            return (Cons.from_list(list_elements), _environment)

    check_argument_number('quasiquote', arguments, 1, 1)

    return recursive_eval_unquote(arguments[0], environment)
