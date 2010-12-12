Hisp: HTML, Lisp Syntax. Works with Django.

Looks something like this:

    (~)
    (html
      (head
        meta (:charset "utf-8"))
        (title "Hisp is fun!"))
      (body
        (#container
          (.left {%django block})
          (.right {django variable})))
