from collections import Sequence
from errors import CircularList


class Atom(object):
    """An abstract class for every base type in Scheme."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Atom: %s (%s)>" % (str(self.value), self.__class__.__name__)

    def __eq__(self, other):
        if isinstance(other, self.__class__) and other.value == self.value:
            return True

        return False

    def get_python_equivalent(self):
        return self.value


"""Atom classes. Although most Scheme data types map neatly to Python
equivalents, there are some exceptions (such as symbols and exact
fractions). Therefore we wrap all atoms in a class so we can treat
them uniformly.

"""
class Symbol(Atom):
    def get_external_representation(self):
        return self.value

class Number(Atom):
    def __eq__(self, other):
        # we allow different types to be equal only for numbers
        if isinstance(other, Number) and self.value == other.value:
            return True

        return False

    def get_external_representation(self):
        return str(self.value)


class Integer(Number):
    pass

class FloatingPoint(Number):
    pass

class Boolean(Atom):
    def get_external_representation(self):
        if self.value:
            return "#t"
        else:
            return "#f"


class Character(Atom):
    def get_external_representation(self):
        return "#\%s" % self.value


class String(Atom):
    def get_external_representation(self):
        return "%r" % self.value


class Cons(Sequence):
    @staticmethod
    def from_list(python_list):
        if not python_list:
            return Nil()
        else:
            head = python_list[0]
            tail = Cons.from_list(python_list[1:])
            return Cons(head, tail)

    def __init__(self, head, tail=None):
        self.head = head

        if tail:
            self.tail = tail
        else:
            self.tail = Nil()
            
    def __len__(self):
        """Find the length of this linked list. We return an error if the list
        is circular, and handle dotted lists gracefully.

        Since Python doesn't have TCO, we are forced to use an
        iterative approach.

        """
        if self.is_circular():
            raise CircularList("Can't take the length of a circular list.")
        
        length = 1
        tail = self.tail

        while True:
            if isinstance(tail, Nil):
                # Reached the end of the list.
                return length
            elif isinstance(tail, Cons):
                # Not yet at the end of the list.
                length += 1
                tail = tail.tail
            else:
                # At the end of an improper list.
                return length + 1

    def is_circular(self):
        tail = self.tail
        seen_elements = set()

        while True:
            if id(tail) in seen_elements:
                return True
            else:
                # We can't hash our list items, but we're only
                # interested in checking if it's an item we've seen
                # before. Using id() is sufficient.
                seen_elements.add(id(tail))

            if isinstance(tail, Nil):
                # Reached the end of the list.
                return False
            elif isinstance(tail, Cons):
                # Not yet at the end of the list.
                tail = tail.tail
            else:
                # At the end of an improper list.
                return False

    def is_proper(self):
        """Does this list end with a Nil?"""
        if self.is_circular():
            return False

        tail = self.tail

        while True:
            if isinstance(tail, Nil):
                # Reached the end of the list.
                return True
            elif isinstance(tail, Cons):
                # Not yet at the end of the list.
                tail = tail.tail
            else:
                # At the end of an improper list.
                return False
                
    def __getitem__(self, index):
        if index == 0:
            return self.head
        else:
            return self.tail.__getitem__(index - 1)

    def __setitem__(self, index, value):
        if index == 0:
            self.head = value
        else:
            return self.tail.__setitem__(index - 1, value)

    def __repr__(self):
        return "<Cons: %s>" % str(self.get_external_representation())

    def __bool__(self):
        # a cons represents is a non-empty list, which we treat as true
        return True

    def __eq__(self, other):
        if not isinstance(other, Cons):
            return False

        element = self
        other_element = other

        while True:
            if element.head != other_element.head:
                return False
            else:
                # continue on the list
                element = element.tail
                other_element = other_element.tail

                if not isinstance(element, Cons) or not isinstance(other_element, Cons):
                    return element == other_element

    def get_python_equivalent(self):
        if hasattr(self.head, "get_python_equivalent"):
            python_list = [self.head.get_python_equivalent()]
        else:
            python_list = [self.head]

        if isinstance(self.tail, Atom):
            # an improper list has an atom as a tail rather than a list
            return python_list + ['.', self.tail.get_python_equivalent()]
        else:
            # normal list
            return python_list + self.tail.get_python_equivalent()

    def get_external_representation(self):
        if self.is_circular():
            # todo: find a better way of printing these.
            return "#<circular list>"

        contents = ""
        element = self

        while True:
            if isinstance(element, Nil):
                # Reached the end of the list.
                break
            elif isinstance(element, Cons):
                # Not yet at the end of the list.
                contents += " " + element.head.get_external_representation()
                element = element.tail
            else:
                # At the end of an improper list.
                contents += " . " + element.get_external_representation()
                break

        return "(%s)" % contents.strip()


class Nil(Sequence):
    def is_circular(self):
        return False

    def is_proper(self):
        return True
    
    # the empty list for our linked list structure
    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise IndexError

    def __setitem__(self, index, value):
        raise IndexError

    def __repr__(self):
        return "<Nil>"

    def __bool__(self):
        return False

    def __eq__(self, other):
        # a Nil is always equal to a Nil
        if isinstance(other, Nil):
            return True
        return False

    def get_python_equivalent(self):
        return []

    def get_external_representation(self):
        return "()"

class Vector(Sequence):
    def __init__(self, length):
        self.value = []
        for index in range(length):
            self.value.append(Nil())

    def __getitem__(self, index):
        return self.value[index]

    def __setitem__(self, index, new_value):
        self.value[index] = new_value

    def __len__(self):
        return len(self.value)

    def __eq__(self, other):
        if isinstance(other, Vector) and self.value == other.value:
            return True

        return False

    def get_external_representation(self):
        item_reprs = [item.get_external_representation()
                      for item in self.value]
        return "#(%s)" % (" ".join(item_reprs))

    @classmethod
    def from_list(cls, values):
        vector = Vector(len(values))
        vector.value = values

        return vector


"""Function classes. These are currently only used in order to add an
external representation.

"""

class Function(object):
    def __init__(self, func, name):
        self.function = func
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class BuiltInFunction(Function):
    def get_external_representation(self):
        return "#<built-in function %s>" % self.name


class PrimitiveFunction(Function):
    def get_external_representation(self):
        return "#<primitive function %s>" % self.name


class UserFunction(Function):
    def get_external_representation(self):
        return "#<user function %s>" % self.name
    

class LambdaFunction(Function):
    def __init__(self, func):
        self.function = func

    def get_external_representation(self):
        return "#<anonymous function>"
