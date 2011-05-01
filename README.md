Minimal scheme: a toy scheme interpreter written in Python

Targetting R5RS ([HTML copy of spec](http://people.csail.mit.edu/jaffer/r5rs_toc.html)), or at least an
interesting subset of it.

All functionality is implemented with corresponding tests. Functions are generally thorough with their error messages, and we strive to give informative error messages.

### Terminology

The terms `primitive`, `built-in` and `standard function` are used to refer to different things in minimal scheme.

A `primitive` is written in Python and controls whether or not it evaluates its arguments.

A `built-in` is written in Python but has all its arguments evaluated automatically.

A `standard function` is written in Scheme.

## Functionality implemented

### Primitives

`define`, `lambda`, `if`, `begin`, `quote`, `eqv?`, `eq?`

No support for `'` acting as `quote` yet though.

### Integers and floats

`number?`, `complex?`, `rational?`, `real?`, `exact?`, `inexact?`,
`+`, `-`, `*`, `/`, `<`, `>`, `=`, `zero?`, `positive?`, `negative?`,
`abs`

No support for exact fractions or complex numbers.

### Characters

`char?`, `char=?`, `char<?`, `char>?`, `char<=?`, `char>=?`

### Lists

`car`, `cdr`, `cons`, `pair?`

### Strings

`string?`, `make-string`, `string-length`

### Other

Comments work too!

## Known bugs

* Cannot nest defines
* No variadic lambdas
* No 'hello world' yet
* positive? returns false for 0

## Cleanup tasks

* Using None as the empty list means that we cannot call len() on any list -- create a Nil object
* Add slice support for our linked list, then clean up variadic function stuff
* Write an immutable dict for environments -- clarity
* Remove eval_program -- it's just map(eval_s_expression, s_expressions)
* Rename internal_result to actual_result in tests.py
* Indent this file properly
* Fix width of evaluator.py
* Put blank lines in consistenly in tests.py
* Distinguish between incorrect type errors and incorrect arity errors, printing accordingly
* Since built-ins don't need access to global variables, don't pass them

## Future ideas

* Compare with other Scheme interpreters written in Python for
  elegance of approach, error friendliness, performance, test coverage
* Stack traces on error with line numbers
  
