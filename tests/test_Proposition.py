import pytest

from sentential import Proposition

""" Top-level API testing """

def test_nested_prop_has_too_many_binary_ops():
    with pytest.raises(SyntaxError):
        p = Proposition(''''p -> q = ~p v q''')
