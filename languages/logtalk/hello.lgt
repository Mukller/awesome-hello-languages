:- object(hello).

    :- public(say/0).
    say :- write('Hello, World!'), nl.

:- end_object.
