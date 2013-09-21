from .base import define_built_in
from utils import check_argument_number
from data_types import Boolean


@define_built_in('procedure?')
def is_procedure(arguments):
    check_argument_number('procedure?', arguments, 1, 1)

    if callable(arguments[0]):
        return Boolean(True)

    return Boolean(False)
