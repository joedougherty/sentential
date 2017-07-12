# -*- coding: utf-8 -*-

from copy import deepcopy
from itertools import product

from environment import ENV
from evaluator import reduce_ast
from grammar import expression_is_grammatical
from parser import tokenize, balanced_parens, read_from_tokens_gen
from utils import parenthesize, extract_variables


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
    # CNF Conversion goes here eventually ...
    env = deepcopy(ENV)
    env.update(var_truth_values)
    return reduce_ast(read_from_tokens_gen((t for t in tokens), env=env))


def generate_all_possible_truth_vals(expr):
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
    collection = []
    for p in product((True, False), repeat=len(extract_variables(expr))):
        collection.append(dict(zip(extract_variables(expr), p)))
    return collection
