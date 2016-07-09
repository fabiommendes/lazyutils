class delegate_to:
    """
    Property that delegates attribute access to a inner variable.

    Args:
        attribute:
            Name of the inner variable that receives delegation.
        readonly:
            If true, makes the the delegate readonly.
    """

    def __init__(self, attribute, readonly=False):
        self.attribute = attribute
        self.readonly = readonly

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        owner = getattr(obj, self.attribute)
        try:
            attr = self._name
        except AttributeError:
            attr = self._name = self._get_name(cls)
        return getattr(owner, attr)

    def __set__(self, obj, value):
        if self.readonly:
            raise AttributeError
        owner = getattr(obj, self.attribute)
        try:
            attr = self._name
        except AttributeError:
            attr = self._name = self._get_name(type(obj))
        setattr(owner, attr, value)

    def _get_name(self, cls):
        for attr in dir(cls):
            value = getattr(cls, attr, None)
            if value is self:
                return attr
        raise RuntimeError('not a member of class')


class delegate_ro(delegate_to):
    """
    A read-only version of delegate_to()
    """

    def __init__(self, attribute):
        super().__init__(attribute, readonly=True)


class lazy:
    """
    Decorator that defines an attribute that is initialized as first usage
    rather than at instance creation.

    Usage is similar to the ``@property`` decorator, although lazy attributes do
    not override the *setter* and *deleter* methods.
    """

    def __init__(self, method):
        self.method = method
        self.__name__ = getattr(method, '__name__', None)

    def __get__(self, obj, cls):
        if obj is None:
            return self

        result = self.method(obj)
        try:
            attr_name = self._attr
        except AttributeError:
            attr_name = self._get_attribute_name(cls)

        setattr(obj, attr_name, result)
        return result

    def _get_attribute_name(self, cls):
        """Inspect live object for some attributes."""

        try:
            if getattr(cls, self.__name__) is self:
                return self.__name__
        except AttributeError:
            pass

        for attr in dir(cls):
            method = getattr(cls, attr, None)
            if method is self:
                self._attr = attr
                return attr

        raise TypeError('lazy accessor not found in %s' % cls.__name__)
