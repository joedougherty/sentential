from operator import and_, or_, not_
import pytest

from sentential.subexpression import (negated_term_collector, classify_sub_expr_terms,
                                      sub_expr_is_sane, ast_is_sane)

""" Test `negated_term_collector` """

def test_negation_collector_with_single_negation():
    partial_ast = ['~', 'p']
    assert negated_term_collector(partial_ast) == ['~', 'p']


def test_negation_collector_with_single_negation_side_effect():
    """ This should also remove the found items from partial_ast. """
    partial_ast = ['~', 'p']
    negated_term_collector(partial_ast)
    assert partial_ast == []


def test_negation_collector_with_multiple_negations():
    partial_ast = ['!', 'not', '~', 'p']
    assert negated_term_collector(partial_ast) == ['!', 'not', '~', 'p']


def test_negation_collector_with_mutliple_negations_side_effect():
    partial_ast = ['!', 'not', '~', 'p']
    negated_term_collector(partial_ast)
    assert partial_ast == []


""" Test `classify_sub_expr_terms` """

def test_classify_sub_expr_terms_single_term_no_binary_op():
    sub_expr = ['!', 'not', '~', 'p']
    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    assert len(terms) == 1
    assert len(binary_ops) == 0
    assert orig_sub_expr == ['!', 'not', '~', 'p']


def test_classify_sub_expr_terms_two_terms_one_binary_op():
    sub_expr = ['!', 'q', 'and', 'r']
    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    assert len(terms) == 2
    assert len(binary_ops) == 1
    assert orig_sub_expr == ['!', 'q', 'and', 'r']


def test_classify_sub_expr_terms_three_terms_one_binary_op():
    sub_expr = ['!', 'q', 'and', 'r', 'z']
    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    assert len(terms) == 3
    assert len(binary_ops) == 1
    assert orig_sub_expr == ['!', 'q', 'and', 'r', 'z']


def test_classify_sub_expr_terms_zero_terms_two_binary_ops():
    sub_expr = ['and', 'v']
    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    assert len(terms) == 0
    assert len(binary_ops) == 2
    assert orig_sub_expr == ['and', 'v']

""" Test `ast_is_sane` """


def test_ast_is_sane_flat_ast():
    test_ast = ['!', 'p', 'or', '~', 'q']
    assert ast_is_sane(test_ast) == True


def test_ast_is_sane_flat_ast_has_too_many_terms():
    test_ast = ['p', 'q', 'r']
    with pytest.raises(ValueError):
        ast_is_sane(test_ast)


def test_ast_is_sane_flat_ast_has_too_many_binary_ops():
    test_ast = ['p', 'and', 'q', 'v', 'r']
    with pytest.raises(ValueError):
        ast_is_sane(test_ast)

