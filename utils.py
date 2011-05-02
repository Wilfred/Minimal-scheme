from errors import SchemeTypeError

def get_type(internal_object):
    if hasattr(internal_object, "type"):
        return internal_object.type
    else:
        return "LIST"

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
            raise SchemeTypeError("%s requires exactly %d argument(s), but "
                                  "received %d." % (function_name,
                                                    min_arguments,
                                                    len(given_arguments)))
        else:
            if max_arguments:
                raise SchemeTypeError("%s requires between %d and %d argument(s), but "
                                      "received %d." % (function_name,
                                                        min_arguments,
                                                        max_arguments,
                                                        len(given_arguments)))
            else:
                raise SchemeTypeError("%s requires at least %d argument(s), but "
                                      "received %d." % (function_name,
                                                        min_arguments,
                                                        len(given_arguments)))
