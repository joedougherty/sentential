# -*- coding: utf-8 -*-

from environment import ENV
from evaluator import reduce_ast
from grammar import expression_is_grammatical, token_is_variable
from parser import tokenize, balanced_parens, read_from_tokens_gen
from utils import parenthesize

# expr = '''((p & ~q) -> r)'''
# expr = '''((p & q) & (p & q))'''
# expr = '''((p & q) v r)'''

expr = parenthesize('''~~p''')

# Are the parens balanced?
#   If not, this will raise SyntaxError
balanced_parens(expr)

tokens = tokenize(expr)

# TODO:
#   Figure out a way to get this to recognize valid start/end tokens
#   This step (as implemented) is necessary, but not sufficient
expression_is_grammatical(tokens)

# TODO
# Is this where the CNF conversion should take place?
# How should this work? -- Is it even strictly necessary?
#   * Prob not for truth evaluation (truth tables and the like)
#   * Prob for unification, though

# Obtain the variables and set truth value(s)
variables = set(filter(lambda x: token_is_variable(x), tokens))

# TEMP DICT JAWN FOR TESTING
env = ENV
var_truth_vals = zip(variables, [True for i in variables])
env.update(var_truth_vals)

ast = read_from_tokens_gen((t for t in tokens), env=env)
truth_value = reduce_ast(ast)

print(expr)
print('Where: {}'.format(var_truth_vals))
print(truth_value)
