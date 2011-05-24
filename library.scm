; maths predicates:
(define (zero? x)
  (if (= x 0)
      #t
      #f))

(define (positive? x)
  (if (>= x 0)
      #t
      #f))

(define (negative? x)
  (if (< x 0)
      #t
      #f))

(define (odd? x)
  (if (= (modulo x 2) 1)
      #t
      #f))

(define (even? x)
  (if (= (modulo x 2) 0)
      #t
      #f))

(define (abs x)
  (if (positive? x)
      x
      (- x)))

; list functions
(define (caar x)
  (car (car x)))

(define (cadr x)
  (car (cdr x)))

(define (cdar x)
  (cdr (car x)))

(define (cddr x)
  (cdr (cdr x)))

(define (map function list)
  (if (null? list)
      '()
      (cons (function (car list))
            (map function (cdr list)))))

; scoping macros
(defmacro let (assignments body)
  `((lambda ,(map car assignments) ,body)
    (unquote-splicing (map cadr assignments))))

(defmacro cond (clauses)
  (let ((first-clause (car clauses)))
    ; if we reach an else statment we evaluate it unconditionally
    (if (eqv? (car first-clause) 'else)
        (cadr first-clause)
        ; if this condition is true, evaluate the body of that condition
        `(if ,(car first-clause)
             ,(cadr first-clause)
             ; otherwise recurse on the rest of the clauses
             (cond ,(cdr clauses))))))
