Minimal scheme: a toy scheme interpreter written in Python

Targetting R5RS ([HTML copy of spec](http://people.csail.mit.edu/jaffer/r5rs_toc.html)), or at least an
interesting subset of it.

All functionality is implemented with corresponding tests. Functions are generally thorough with their error messages, and we strive to give informative error messages.

## Functionality implemented

### Primitives

`define`, `lambda`, `if`, `begin`, `quote`, `eqv?`, `eq?`

No support for `'` acting as `quote` yet though.

### Integers and floats

`+`, `-`, `*`, `/`, `<`, `>`, `=`, `zero?`, `positive?`, `negative?`

No support for exact fractions or complex numbers.

### Characters

`char?`, `char=?`, `char<?`, `char>?`, `char<=?`, `char>=?`

### Lists

`car`, `cdr`, `cons`, `pair?`

### Other

Comments work too!

## Known bugs

* Type checking doesn't handle lists yet (so `(+ (quote x) (quote x))`
  and `(number? (quote x))` crash)
* The environment isn't wiped after each test
