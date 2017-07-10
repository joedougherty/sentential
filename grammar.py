# -*- coding: utf-8 -*-

try:
    from string import lowercase 
except:
    from string import ascii_lowercase as lowercase

OPENPAREN = '('
CLOSEPAREN = ')'
VAR = lowercase.replace('v','')
AND = '&'
OR  = 'v'
IFTHEN = '->'
NOT = '~'
IFF = 'iff'

"""
Keys in `grammar_rules` are a pattern to match.
Values are collections of valid following tokens.

Grammar rules can be extracted by checking if a token:
    1.) can be matched in any of the keys
    2.) is followed by a token given by the collection of valid patterns
"""
grammar_rules = {OPENPAREN: (OPENPAREN, VAR, NOT),
                 CLOSEPAREN: (CLOSEPAREN, AND, OR, IFTHEN, IFF),
                 VAR: (CLOSEPAREN, AND, OR, IFTHEN, IFF),
                 AND: (OPENPAREN, VAR, NOT),
                 OR: (OPENPAREN, VAR, NOT),
                 IFTHEN: (OPENPAREN, VAR, NOT),
                 NOT: (OPENPAREN, VAR, NOT),
                 IFF: (OPENPAREN, VAR, NOT)}


def token_is_variable(token):
    return token in VAR


def token_rule(token, grammar_rules=grammar_rules, join_tokens=True):
    for pattern in grammar_rules.keys():
        if token in pattern:
            if join_tokens:
                # Join all valid tokens into a single string
                return ''.join(grammar_rules.get(pattern))
            else:
                # Keep tokens separate for error reporting purposes
                return ', '.join([t for t in grammar_rules.get(pattern)])
    raise SyntaxError('"{}" is not a valid token!'.format(token))


def expression_is_grammatical(expr, trace=False):
    for idx, token in enumerate(expr):
        try:
            next_token = expr[idx+1]
        except IndexError:
            return True

        if trace:
            print('current token: {}'.format(token))
            print('next token: {}'.format(next_token))
            print('----------------')

        if next_token not in token_rule(token):
            msg = 'Could not parse expression!\n'
            msg += '{} was followed by: {}\n'.format(token, next_token)
            msg += '{} must be followed by one of: {}\n'.format(token, token_rule(token, join_tokens=False))
            raise SyntaxError(msg)
