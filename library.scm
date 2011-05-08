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