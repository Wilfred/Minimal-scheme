; maths predicates:
(define (zero? x)
  (if (= x 0)
      #t
      #f))

(define (positive? x)
  (if (> x 0)
      #t
      #f))

(define (negative? x)
  (if (< x 0)
      #t
      #f))
