# -*- coding: utf-8 -*-

from itertools import takewhile

from environment import ENV
from utils import Stack

def tokenize(chars):
    ''' Convert a string expression into a list of tokens. '''
    return chars.replace('~', '~ ')  \
                .replace('(', ' ( ') \
                .replace(')', ' ) ') \
                .replace('!', '! ')  \
                .split()


def read_from_tokens_gen(tokens, current_token=None, env=ENV):
    if current_token:
        token = current_token
    else:
        token = next(tokens)
    if token == '(':
        L = []
        for t in takewhile(lambda x: x != ')', tokens):
            L.append(read_from_tokens_gen(tokens, current_token=t, env=env))
        return L
    else:
        try:
            return env[token]
        except KeyError:
            raise ValueError("I don't know what to do with {}!".format(token))


def balanced_parens(expression):
    stack = Stack()
    for idx, token in enumerate(expression):
        if token == '(':
            stack.push(token)
            last_open_paren = idx
        if token == ')':
            try:
                stack.pop()
            except IndexError:
                msg = 'Found unmatched )' + '\n'
                msg += expression + '\n'
                msg += (' ' * idx) + '^'
                raise SyntaxError(msg)
        there_are_more_tokens = (idx != len(expression)-1)
        if stack.isEmpty() and there_are_more_tokens:
            msg = 'Matched parens, but there are extra tokens!\n'
            msg += expression + '\n'
            msg += (' ' * (idx + 1)) + '^'
            raise SyntaxError(msg)
    if not stack.isEmpty():
        msg = 'Found unmatched (' + '\n'
        msg += expression + '\n'
        msg += (' ' * last_open_paren) + '^'
        raise SyntaxError(msg)
    return True
