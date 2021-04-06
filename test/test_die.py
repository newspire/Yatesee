import pytest
from yatesee import Die

def test_die_equals():
    assert Die(1) == 1
    assert Die(2) == 2
    assert Die(3) == 3
    assert Die(4) == 4
    assert Die(5) == 5
    assert Die(6) == 6

    assert Die(1) != 3

    assert Die(1) == Die(1)
    assert Die(2) == Die(2)
    assert Die(3) == Die(3)
    assert Die(4) == Die(4)
    assert Die(5) == Die(5)
    assert Die(6) == Die(6)

    assert Die(1) != Die(2)

    assert Die(1).currentValue() == 1
    assert Die(2).currentValue() == 2
    assert Die(3).currentValue() == 3
    assert Die(4).currentValue() == 4
    assert Die(5).currentValue() == 5
    assert Die(6).currentValue() == 6

def test_die_roll():
    d = Die()
    d.roll()
    assert True

def test_die_hash():
    assert Die(1).__hash__() == Die(1).__hash__()
    assert Die(1).__hash__() != Die(2).__hash__()

def test_die_lt():
    assert Die(1) < Die(2)
    assert Die(1) < 2

    assert not (Die(2) < 2)
    assert not (Die(2) < Die(2))

def test_die_lte():
    assert Die(2) <= Die(2)
    assert Die(2) <= 2
    assert Die(1) <= Die(2)
    assert Die(1) <= 2

    assert not (Die(2) <= Die(1))
    assert not (Die(2) <= 1)

def test_die_ne():
    assert Die(2) != Die(1)
    assert Die(1) != 2

    assert not (Die(2) != Die(2))
    assert not (Die(2) != 2)

def test_die_gt():
    assert Die(2) > Die(1)
    assert Die(2) > 1

    assert not (Die(2) > 2)
    assert not (Die(2) > Die(2))

def test_die_gte():
    assert Die(2) >= Die(2)
    assert Die(2) >= 2
    assert Die(2) >= Die(1)
    assert Die(2) >= 1

    assert not (Die(1) >= Die(2))
    assert not (Die(1) >= 2)

def test_die_add():
    assert Die(2) + Die(2) == 4
    assert Die(2) + 2 == 4

    assert not (Die(2) + Die(1) == 4)
    assert not (Die(2) + 1 == 4)
