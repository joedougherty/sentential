# -*- coding: utf-8 -*-

from itertools import takewhile

from .environment import ENV
from .utils import Stack, deparenthesize


def tokenize(chars):
    ''' Convert a string expression into a list of tokens. '''
    return chars.replace('~', '~ ')  \
                .replace('(', ' ( ') \
                .replace(')', ' ) ') \
                .replace('!', '! ')  \
                .replace('¬', '¬ ')  \
                .split()


def extract_from_env(env, token):
    try:
        return env[token]
    except KeyError:
        raise ValueError("{} is not defined the environment.".format(token))


def read_from_tokens_gen(tokens, current_token=None, env=ENV, evaluate_tokens=True):
    """
    Implements a simple recursive descent parser.

    Accepts a steam of tokens and returns an AST
    (modeled as a list of lists of expressions).

    This is (roughly) a generator-based implementation of
    the `read_from_tokens` function found in Peter Norvig's
    (How to Write a (Lisp) Interpreter (in Python))
    [https://norvig.com/lispy.html]
    """
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
        if evaluate_tokens:
            return extract_from_env(env, token)
        else:
            return token


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
                msg += deparenthesize(expression) + '\n'
                msg += (' ' * idx) + '^'
                raise SyntaxError(msg)
        there_are_more_tokens = (idx != len(expression)-1)
        if stack.isEmpty() and there_are_more_tokens:
            msg = 'Matched parens, but there are extra tokens!\n'
            msg += deparenthesize(expression) + '\n'
            msg += (' ' * (idx-1)) + '^'
            raise SyntaxError(msg)
    if not stack.isEmpty():
        msg = 'Found unmatched (' + '\n'
        msg += deparenthesize(expression) + '\n'
        msg += (' ' * (last_open_paren-1)) + '^'
        raise SyntaxError(msg)
    return True
