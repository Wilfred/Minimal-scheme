from .base import define_built_in
from utils import check_argument_number

from data_types import (Boolean, Character, String, Integer)
from errors import SchemeTypeError, InvalidArgument


@define_built_in('string?')
def is_string(arguments):
    check_argument_number('string?', arguments, 1, 1)

    if isinstance(arguments[0], String):
        return Boolean(True)

    return Boolean(False)


@define_built_in('make-string')
def make_string(arguments):
    check_argument_number('make-string', arguments, 1, 2)

    string_length_atom = arguments[0]

    if not isinstance(string_length_atom, Integer):
        raise SchemeTypeError("String length must be an integer, "
                              "got %d." % string_length_atom.__class__)

    string_length = string_length_atom.value

    if string_length < 0:
        raise InvalidArgument("String length must be non-negative, "
                              "got %d." % string_length)

    if len(arguments) == 1:
        return String(' ' * string_length)

    else:
        repeated_character_atom = arguments[1]

        if not isinstance(repeated_character_atom, Character):
            raise SchemeTypeError("The second argument to make-string must be"
                                  " a character, got a %s." % repeated_character_atom.__class__)

        repeated_character = repeated_character_atom.value
        return String(repeated_character * string_length)


@define_built_in('string-length')
def string_length(arguments):
    check_argument_number('string-length', arguments, 1, 1)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-length takes a string as its argument, "
                              "not a %s." % string_atom.__class__)

    string_length = len(string_atom.value)
    return Integer(string_length)

@define_built_in('string-ref')
def string_ref(arguments):
    check_argument_number('string-ref', arguments, 2, 2)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-ref takes a string as its first argument, "
                              "not a %s." % string_atom.__class__)

    char_index_atom = arguments[1]
    if not isinstance(char_index_atom, Integer):
        raise SchemeTypeError("string-ref takes an integer as its second argument, "
                              "not a %s." % char_index_atom.__class__)

    string = string_atom.value
    char_index = char_index_atom.value

    if char_index >= len(string):
        # FIXME: this will say 0--1 if string is ""
        raise InvalidArgument("String index out of bounds: index must be in"
                              " the range 0-%d, got %d." % (len(string) - 1, char_index))

    return Character(string[char_index])


@define_built_in('string-set!')
def string_set(arguments):
    check_argument_number('string-set!', arguments, 3, 3)

    string_atom = arguments[0]
    if not isinstance(string_atom, String):
        raise SchemeTypeError("string-set! takes a string as its first argument, "
                              "not a %s." % string_atom.__class__)

    char_index_atom = arguments[1]
    if not isinstance(char_index_atom, Integer):
        raise SchemeTypeError("string-set! takes an integer as its second argument, "
                              "not a %s." % char_index_atom.__class__)

    replacement_char_atom = arguments[2]
    if not isinstance(replacement_char_atom, Character):
        raise SchemeTypeError("string-set! takes a character as its third argument, "
                              "not a %s." % replacement_char_atom.__class__)

    string = string_atom.value
    char_index = char_index_atom.value

    if char_index >= len(string):
        # FIXME: this will say 0--1 if string is ""
        raise InvalidArgument("String index out of bounds: index must be in"
                              " the range 0-%d, got %d." % (len(string) - 1, char_index))

    characters = list(string)
    characters[char_index] = replacement_char_atom.value
    new_string = "".join(characters)

    string_atom.value = new_string

    return None
