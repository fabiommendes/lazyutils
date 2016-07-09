import pytest
from lazyutils import lazy, delegate_to, delegate_ro

#
# Lazy attribute
#
@pytest.fixture
def A():
    class A:
        L = []

        @lazy
        def b(self):
            self.L.append(1)
            return 2

    return A


def test_lazy_attribute_is_cached(A):
    a = A()
    assert a.b == 2
    assert A.L == [1]
    assert a.b == 2
    assert A.L == [1]


def test_lazy_attribute_is_writable(A):
    a = A()
    a.b = 1
    assert a.b == 1
    assert A.L == []


def test_lazy_works_with_lambdas():
    class A:
        x = lazy(lambda self: 42)

    a = A()
    assert a.x == 42


#
# Delegate to
#
@pytest.fixture
def B():
    class B:
        x = delegate_to('data')
        y = delegate_to('data', readonly=True)
        z = delegate_ro('data')

        def __init__(self, data):
            self.data = data

    return B


@pytest.fixture
def data_cls():
    class Data:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
    return Data


def test_delegate_to_reads_data(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    assert b.x == 1
    assert b.y == 2


def test_delegate_ro_reads_data(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    assert b.z == 3


def test_delegate_to_can_write(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    b.x = 42
    assert b.x == 42


def test_delegate_ro_cannot_write(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)

    with pytest.raises(AttributeError):
        b.y = 42

    with pytest.raises(AttributeError):
        b.z = 42

    assert b.y == 2
    assert b.z == 3
