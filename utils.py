# -*- coding: utf-8 -*-


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


def parenthesize(expr):
    return '({})'.format(expr)


def deparenthesize(expr):
    if expr[0] == '(' and expr[-1] == ')':
        return expr[1:-1]
    return expr
