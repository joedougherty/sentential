# -*- coding: utf-8 -*-

from operator import and_, or_, not_

from sentential.evaluator import resolve_term_negation, eval_cell  

""" Test `resolve_term_negation` """


def test_resolve_term_negation_double_negation():
    test_ast = [not_, not_, True]
    assert resolve_term_negation(test_ast) == True


def test_resolve_term_negation_double_negation_side_effect():
    test_ast = [not_, not_, True]
    resolve_term_negation(test_ast)
    assert test_ast == []


""" Test `eval_cell` """

def test_eval_cell_binary_operator():
    test_cell = [True, and_, not_, False]
    assert eval_cell(test_cell) == True


def test_eval_cell_single_negation_operator():
    test_cell = [not_, False]
    assert eval_cell(test_cell) == True
