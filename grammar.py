# -*- coding: utf-8 -*-

from collections import namedtuple
try:
    from string import lowercase
except:
    from string import ascii_lowercase as lowercase


grammar_rule = namedtuple('grammar_rule', ['pattern', 'valid_following_patterns'])

OPENPAREN = ['(']
CLOSEPAREN = [')']
VAR = [letter for letter in lowercase.replace('v', '')]
AND = ['&', 'and']
OR  = ['v', 'or']
IFTHEN = ['->']
NOT = ['~', 'not', '¬']
IFF = ['iff']

grammar_rules = []
grammar_rules.append(grammar_rule(OPENPAREN, OPENPAREN + VAR + NOT))
grammar_rules.append(grammar_rule(CLOSEPAREN, CLOSEPAREN + AND + OR + IFTHEN + IFF))
grammar_rules.append(grammar_rule(VAR, CLOSEPAREN + AND + OR + IFTHEN + IFF))
grammar_rules.append(grammar_rule(AND, OPENPAREN + VAR + NOT))
grammar_rules.append(grammar_rule(OR, OPENPAREN + VAR + NOT))
grammar_rules.append(grammar_rule(IFTHEN, OPENPAREN + VAR + NOT))
grammar_rules.append(grammar_rule(NOT, OPENPAREN + VAR + NOT))
grammar_rules.append(grammar_rule(IFF, OPENPAREN + VAR + NOT))


def token_is_variable(token):
    return token in VAR


def token_rule(token, grammar_rules=grammar_rules):
    for rule in grammar_rules:
        if token in rule.pattern:
            return rule.valid_following_patterns
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
            msg = 'Statement is not grammatical!\n'
            msg += '{} was followed by: {}\n'.format(token, next_token)
            msg += '{} must be followed by one of: {}\n'.format(token, ', '.join(token_rule(token)))
            raise SyntaxError(msg)
