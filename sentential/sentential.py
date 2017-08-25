# -*- coding: utf-8 -*-

from collections import OrderedDict
from copy import copy, deepcopy
from itertools import product

from .environment import ENV
from .evaluator import eval_cell
from .grammar import expression_is_grammatical
from .parser import tokenize, balanced_parens, read_from_tokens_gen
from .subexpression import ast_is_sane
from .utils import parenthesize, extract_variables, reduce_ast


def derive_truth_value(expression, var_truth_values):
    """
    Return the truth value of an expression in sentential logic.

        expression [str]:
            An expression in sentential logic.
            Ex: '''(p & ~q)'''

        var_truth_values [dict]:
            key: the variable (ex: 'p', 'q', etc.)
            value: its boolean value (True, False)

    Usage::
    >>> derive_truth_value('''(p & ~q)''', {'p': True, 'q': False})
    True
    """
    balanced_parens(parenthesize(expression))
    tokens = tokenize(parenthesize(expression))
    expression_is_grammatical(tokens)
    ast_is_sane(read_from_tokens_gen((t for t in tokens), evaluate_tokens=False))
    # CNF Conversion goes here eventually ...
    env = deepcopy(ENV)
    env.update(var_truth_values)
    return reduce_ast(read_from_tokens_gen((t for t in tokens), env=env), eval_cell)


def generate_all_possible_truth_vals(expr, sort_vars=False):
    """
    Given a set of variables, return a list of all possible
    dicts where:
        * the key is the variable name
        * the value is its truth value

    Usage::
    >>> generate_all_possible_truth_vals('''(p & ~q)''')
    [{'q': True, 'p': True},
     {'q': True, 'p': False},
     {'q': False, 'p': True},
     {'q': False, 'p': False}]
    """

    expr_vars = extract_variables(tokenize(expr))

    if sort_vars:
        expr_vars.sort()

    collection = []
    for p in product((True, False), repeat=len(expr_vars)):
        collection.append(OrderedDict(zip(expr_vars, p)))
    return collection

def same_truth_table(p1, p2):
    """
    Do two Propositions have the same truth table? Let's find out!
    """
    p1 = deepcopy(p1)
    p2 = deepcopy(p2)

    p1_vars = copy(p1.expr_vars)
    p2_vars = copy(p2.expr_vars)
    p1_vars.sort()
    p2_vars.sort()

    if p1_vars != p2_vars:
        return False

    if p1.truth_table() == p2.truth_table():
        return True

    p1_truth_table = p1._compute_truth_table(sort_vars=True)
    p2_truth_table = p2._compute_truth_table(sort_vars=True)
    return p1_truth_table == p2_truth_table
