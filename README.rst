Lazyutils provides a few simple utilities for lazy evaluation of code.


Lazy attribute
==============

The lazy decorator defines an attribute with deferred initialization::

    class Vec:
        def __init__(self, x, y):
            self.x, self.y = x, y

        @lazy
        def magnitude(self):
            print('computing...')
            return math.sqrt(x**2 + y**2)

Now the "magnitude" attribute is initialized and cached upon first use::

    >>> v = Vec(3, 4)
    >>> v.magnitude
    computing...
    5.0

The attribute is writable and apart from the deferred initialization, it behaves
just like any regular Python attribute.

    >>> v.magnitude = 42
    >>> v.magnitude
    42

Lazy attributes can be useful either to simplify the implementation of the
__init__ method of objects that initialize a great number or variables or as an
optimization that delays potentially expensive computations that may not be
necessary in the object's lifecycle.


Delegation
==========

The delegate_to() function delegates some attribute to an attribute during the
class definition::

    class Arrow:
        magnitude = delegate_to('vector')

        def __init__(self, vector, start=Vec(0, 0)):
            self.vector = radius
            self.start = start

Now, the `.magnitude` attribute of `Arrow` instances is delegated to
`.vector.magnitude`. Delegate fields are useful in class composition when one
wants to expose a few selected attributes from the inner objects. delegate_to()
handles attributes and methods with no distinction.


    >>> a = Arrow(Vec(6, 8))
    >>> a.magnitude
    magnitude...
    10.0
