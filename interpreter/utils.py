from errors import SchemeArityError

def identity(*args):
    return args

def check_argument_number(function_name, given_arguments,
                          min_arguments, max_arguments=None):
    assert max_arguments is None or min_arguments <= max_arguments

    right_argument_number = True

    if len(given_arguments) < min_arguments:
        right_argument_number = False

    if max_arguments and len(given_arguments) > max_arguments:
        right_argument_number = False

    if not right_argument_number:
        if min_arguments == max_arguments:
            raise SchemeArityError("%s requires exactly %d argument(s), but "
                                  "received %d." % (function_name,
                                                    min_arguments,
                                                    len(given_arguments)))
        else:
            if max_arguments:
                raise SchemeArityError("%s requires between %d and %d argument(s), but "
                                      "received %d." % (function_name,
                                                        min_arguments,
                                                        max_arguments,
                                                        len(given_arguments)))
            else:
                raise SchemeArityError("%s requires at least %d argument(s), but "
                                      "received %d." % (function_name,
                                                        min_arguments,
                                                        len(given_arguments)))
