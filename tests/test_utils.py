from operator import and_, not_, or_

from sentential.utils import (list_is_nested, resolve_left_innermost,
                             flatten_left_innermost, reduce_ast, ast_to_stack)

""" Test `list_is_nested` """

def test_flat_empty_list():
    assert list_is_nested([]) == False


def test_flat_list():
    assert list_is_nested([True, or_, False]) == False


def test_simple_nested_list():
    assert list_is_nested([True, or_, [True, and_, False]]) == True


""" Test `flatten_left_innermost` """

def test_flat_flatten_left_innermost():
    # If the given AST is a flat list, return the list
    test_ast = [True, and_, False]
    assert flatten_left_innermost(test_ast) == [True, and_, False]


def test_nested_flatten_left_innermost_return_value():
    """ Test that the correct sub-list is returned """
    test_ast = [True, and_, False, [True, or_, False], [1, 2, 3]]
    assert flatten_left_innermost(test_ast) == [True, or_, False]


def test_nested_flatten_left_innermost_list_is_updated():
    """
    Test that the list is altered appropriately.
    The returned sub-list should be represented in the original list
    by None.
    """
    test_ast = [True, and_, False, [True, or_, False], [1, 2, 3]]
    flatten_left_innermost(test_ast)
    assert test_ast == [True, and_, False, None, [1, 2, 3]]


""" Test `ast_to_stack` """

def test_empty_ast_to_stack():
    stack_representation = ast_to_stack([])
    assert len(stack_representation.contents) == 0


def test_flat_ast_to_stack():
    test_ast = [True, and_, False]
    stack_representation = ast_to_stack(test_ast)
    assert len(stack_representation.contents) == 1


def test_nested_ast_to_stack():
    test_ast = [True, and_, False, [True, or_, False], [1, 2, 3]]
    stack_representation = ast_to_stack(test_ast)
    assert len(stack_representation.contents) == 3
