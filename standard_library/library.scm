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
(define (null? x)
  (eqv? x '()))

(define (list . args)
  args)

(define (length x)
  (if (null? x)
      0
      (+ 1 (length (cdr x)))))

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

(define (for-each function list)
  (if (null? list)
      '()
      (begin
        (function (car list))
        (for-each function (cdr list)))))

; scoping macros
(defmacro let (assignments . body)
  `((lambda ,(map car assignments) ,@body)
    ,@(map cadr assignments)))

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

; vector functions
(define (vector . args)
  (let ((v (make-vector (length args)))
        (index 0))
    (for-each
     (lambda (arg)
       (vector-set! v index arg)
       (set! index (+ index 1)))
     args)
    v))

(define (vector->list vector)
  ;; vector-list-iter is a recursive helper function that moves
  ;; through the vector and builds a list.
  (let ((vector->list-iter
         (lambda (index)
           (if (>= index (vector-length vector))
               '()
               (cons
                (vector-ref vector index)
                (vector->list-iter (+ index 1)))))))
    (vector->list-iter 0)))

; I/O
(define (newline)
  (display "\n"))

; booleans
(define (not x)
  (eqv? x #f))

; note that R5RS requires 'and and 'or to take a variable number of arguments
(defmacro and (x y)
  `(if ,x (if ,y ,y #f) #f))

(defmacro or (x y)
  `(if ,x ,x ,y))

; characters
(define (char>? x y)
  (and (not (char=? x y))
       (not (char<? x y))))

(define (char<=? x y)
  (or (char=? x y)
      (char<? x y)))

(define (char>=? x y)
  (not (char<? x y)))
