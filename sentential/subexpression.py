# -*- coding: utf-8 -*-

from copy import deepcopy

from .utils import ast_to_stack
from .grammar import NEGATION, token_is_binary_op, token_is_variable


def negated_term_collector(sub_expr):
    acc = []
    while sub_expr[0] in NEGATION:
        acc.append(sub_expr.pop(0))
    # Also collect the variable
    acc.append(sub_expr.pop(0))
    return acc


def classify_sub_expr_terms(sub_expr):
    """
    Traverse the subexpression (a list of tokens)
    and sort its contents into terms and binary_ops.

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
        if sub_expr[0] in NEGATION:
            terms.append(negated_term_collector(sub_expr))
        elif token_is_variable(sub_expr[0]):
            terms.append([sub_expr.pop(0)])
        elif token_is_binary_op(sub_expr[0]):
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
    def cell_to_str(expr_as_list):
        str_rep = "({})".format(' '.join(expr_as_list))
        for symbol in NEGATION:
            str_rep = str_rep.replace(symbol + ' ', symbol)
        return str_rep

    terms, binary_ops, orig_sub_expr = classify_sub_expr_terms(sub_expr)
    if len(terms) > 2 or len(binary_ops) > 1:
        err_msg = 'Expression may contain at most two variables and one binary operator!'
        raise ValueError("{}: {}".format(cell_to_str(orig_sub_expr), err_msg))
    return True


def ast_is_sane(ast):
    """
    Create of stack of all the sub-expressions that the AST
    is composed of.

    Iterate over them an ensure that each contains no more than
    two variables (possibly preceded by >=1 negation operators)
    and one binary operator.
    """
    stack_of_expressions = ast_to_stack(ast)
    while not stack_of_expressions.isEmpty():
        sub_expr_is_sane(stack_of_expressions.pop())
    return True
