from .base import built_ins

# Although we don't do anything after importing, we need to execute
# these scripts to ensure their built-ins are loaded into the
# built_ins dict.
from . import lists
from . import numbers
from . import equivalence
from . import chars
from . import strings
from . import vectors
from . import io
from . import control
