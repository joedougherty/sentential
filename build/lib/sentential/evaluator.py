# -*- coding: utf-8 -*-

from operator import not_

from .utils import Stack


def resolve_term_negation(L):
    """
    Given a partial expression cell, apply all negation
    operators to the next variable and return that value.

    Ex:
        input: [not_, not_, True]
        output: True

    Push each not_ onto a stack.
    Once the var value is found, apply all not_ operators
    to the var and return that value.
    """
    op_stack = Stack()
    while not isinstance(L[0], bool):
        op_stack.push(L.pop(0))

    var = L.pop(0)  # The boolean value (resolved val of 'p', 'q', etc.)
    while not op_stack.isEmpty():
        var = op_stack.pop()(var)

    return var


def eval_cell(expr_as_list):
    """
    Resolve a given expression cell into its truth value.

    Ex:
        input: [True, and_, not_, False]
        output: True
    """
    resolved_vals = []
    while not expr_as_list == []:
        next_token = expr_as_list[0]
        if next_token == not_:
            resolved_vals.append(resolve_term_negation(expr_as_list))
        else:
            resolved_vals.append(expr_as_list.pop(0))

    if len(resolved_vals) == 1:
        return resolved_vals[0]
    else:
        return resolved_vals[1](resolved_vals[0], resolved_vals[2])
