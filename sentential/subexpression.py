# -*- coding: utf-8 -*-

from copy import deepcopy
from operator import not_

from .environment import ENV


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
    """
    Traverse the subexpression and sort its contents
    into terms and binary_ops.

    *terms* will be a list containing any lists returned by
    negated_term_collector and/or 1-item lists of the terms
    (in the case that there are not negation operators).

    *binary_ops* will be a list of any/all found binary
    operators.
    """
    terms = []
    binary_ops = []
    orig_sub_expr = deepcopy(sub_expr)

    while not sub_expr == []:
        if sub_expr[0] == ENV['not']:
            terms.append(negated_term_collector(sub_expr))
        elif isinstance(sub_expr[0], bool):
            terms.append([sub_expr.pop(0)])
        elif is_binary_op(sub_expr[0]):
            binary_ops.append(sub_expr.pop(0))
        else:
            raise ValueError("I don't know what to do with {}!".format(sub_expr[0]))
    return (terms, binary_ops, orig_sub_expr)


def sub_expr_is_sane(sub_expr):
    """
    Verify that the given sub-expression contains no more than:
        * two terms (variables, possibly preceded by multiple negations)
        * one binary operator (and, or, conditional, biconditional)
    """
    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    if len(terms) > 2:
        err_msg = 'Expression contains more than 2 terms!'
        return (False, err_msg, orig_sub_expr)
    if len(binary_ops) > 1:
        err_msg = 'Expression contains more than 1 binary operator!'
        return (False, err_msg, orig_sub_expr)
    return (True, None, orig_sub_expr)


def ast_is_sane(ast):
    """
    Recursively traverse the AST and verify that each
    sub-expression is sane.
    """
    for idx, item in enumerate(ast):
        if isinstance(item, list):
            is_sane, err_msg, orig_sub_expr = sub_expr_is_sane(item)
            if not is_sane:
                print(orig_sub_expr)
                raise ValueError(err_msg)
            return ast_is_sane(item)
    return True
