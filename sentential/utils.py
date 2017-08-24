# -*- coding: utf-8 -*-

from copy import copy, deepcopy

from .grammar import token_is_variable


class Stack:
    def __init__(self, size_limit=None):
        self.contents = []
        self.size_limit = size_limit

    def push(self, item):
        if self.size_limit:
            if (self.size() + 1) > self.size_limit:
                msg = 'This Stack has a size_limit set to: {}'.format(self.size_limit)
                raise ValueError(msg)
        self.contents.append(item)

    def pop(self):
        return self.contents.pop()

    def peek(self):
        return self.contents[-1]

    def isEmpty(self):
        return self.size() == 0

    def size(self):
        return len(self.contents)


def list_is_nested(L):
    for item in L:
        if isinstance(item, list):
            return True
    return False


def resolve_left_innermost(L, resolve_fn, inner=None):
    """
    Given a nested list L:
        * Find the left-innermost nested list
        * Resolve it by applying resolve_fn
        * Replace the nested list with the resolved value
        * Return L
    """
    if inner is None:
        inner = L

    for idx, item in enumerate(inner):
        """
        If we found a flat list, we know we've bottomed out.

        Replace the list with the resolved value and pass the
        modified containing list back to the caller.
        """
        if isinstance(item, list) and not list_is_nested(item):
            inner[idx] = resolve_fn(item)
            return L
        if isinstance(item, list):
            return resolve_left_innermost(L, resolve_fn, inner=item)


def flatten_left_innermost(L, inner=None):
    """
    Given a nested list L:
        * Find the left-innermost nested list
        * Set it to None
        * Return a cop  found list
    """
    if inner is None:
        inner = L

    if not list_is_nested(L):
        return_cell = []
        while L != []:
            return_cell.append(L.pop(0))
        return return_cell

    for idx, item in enumerate(inner):
        """
        If we found a flat list, we know we've bottomed out.
        """
        if isinstance(item, list) and not list_is_nested(item):
            return_cell = copy(inner[idx])
            inner[idx] = None
            return return_cell
        if isinstance(item, list):
            return flatten_left_innermost(L, inner=item)


def reduce_ast(expr_as_ast, eval_fn):
    while list_is_nested(expr_as_ast):
        expr_as_ast = resolve_left_innermost(expr_as_ast, eval_fn)
    return eval_fn(expr_as_ast)


def ast_to_stack(expr_as_ast):
    """
    Create of stack of all the sub-expressions that the AST
    is composed of.
    """
    ast_copy = deepcopy(expr_as_ast)
    expression_stack = Stack()
    while ast_copy != []:
        expression_stack.push(flatten_left_innermost(ast_copy))
    return expression_stack


def parenthesize(expr):
    return '({})'.format(expr)


def deparenthesize(expr):
    if expr[0] == '(' and expr[-1] == ')':
        return expr[1:-1]
    return expr


def extract_variables(expr, sort_vars=False):
    """
    We do this rather than use set() + a list comprehension
    to retain order of appearance in the expression.
    """
    found = []
    for token in expr:
        if token_is_variable(token) and token not in found:
            found.append(token)

    if sort_vars:
        found.sort()

    return found
