# -*- coding: utf-8 -*-

import pytest

from sentential.dpll import *

# Top level API sanity checks
def test_empty_collection_evaluates_to_true():
    assert dpll([]) == True


def test_single_empty_clause_evaluates_to_false():
    assert dpll([[]]] == False


# "Simplify" test cases
def test_contains_one_clause_with_a_positive_literal():
    assert simplify([['p']], 'p') == []


def test_contains_one_clause_with_a_negated_literal():
    assert simplify([['~p', 'q'], ['r']], 'p') == [['q'], ['r']]
