# -*- coding: utf-8 -*-

from copy import deepcopy

from environment import ENV
from evaluator import reduce_ast
from grammar import expression_is_grammatical
from parser import tokenize, balanced_parens, read_from_tokens_gen
from utils import parenthesize


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
    balanced_parens(expression)
    tokens = tokenize(parenthesize(expression))
    expression_is_grammatical(tokens)
    # CNF Conversion goes here eventually ...
    env = deepcopy(ENV)
    env.update(var_truth_values)
    return reduce_ast(read_from_tokens_gen((t for t in tokens), env=env))
