 -*- coding: utf-8 -*-

from collections import namedtuple
from operator import not_

from .environment import ENV

decomposed_sub_expr = namedtuple('decomposed_sub_expr', ['terms', 'binary_ops'])

def is_binary_op(term, env=ENV):
    return term in set([fn for fn in env.values() if fn != not_])


def negated_term_collector(sub_expr):
    acc = []
    while sub_expr[0] == ENV['not']:
        acc.append(sub_expr.pop(0))
    # Also collect the boolean value
    acc.append(sub_expr.pop(0))
    return acc


def classify_sub_expr_terms(sub_expr):
    terms = []
    binary_ops = []
    while not sub_expr == []:
        if sub_expr[0] == ENV['not']:
            terms.append(negated_term_collector(sub_expr))
        elif is_binary_op(sub_expr[0]):
            binary_ops.append(sub_expr.pop(0))
        else:
            raise ValueError("I don't know what to do with {}!".format(sub_expr[0]))
    return decomposed_sub_expr(terms, binary_ops)


def sub_expr_is_sane(sub_expr):
    terms, binary_ops = classify_sub_expr_terms(sub_expr)
    if len(terms) > 2:
        raise ValueError('Expression contains more than 2 terms!')
    if len(binary_ops) > 1:
        raise ValueError('Expression contains more than 1 binary operator!')
    return True
