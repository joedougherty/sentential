from operator import and_, not_, or_

from sentential.utils import (list_is_nested, resolve_left_innermost,
                             pop_left_innermost, reduce_ast, ast_to_stack)

""" Tests pertaining to sentential.utils """

def test_flat_empty_list():
    assert list_is_nested([]) == False


def test_flat_list():
    assert list_is_nested([True, or_, False]) == False


def test_simple_nested_list():
    assert list_is_nested([True, or_, [True, and_, False]]) == True
