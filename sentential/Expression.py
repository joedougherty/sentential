try:
    from string import lowercase
except:
    from string import ascii_lowercase as lowercase

from copy import deepcopy
from operator import not_

from .Proposition import Proposition
from .utils import list_is_nested

"""
Provides models and tools for converting a nested list AST
into a tree model (given by Expression) and vice versa.
"""

class Term:
    """
    Models a term (in a n expression).

    Find its truth value by calling eval() with
    an environment.
    """
    def __init__(self, variable, negated):
        self.variable = variable
        self.negated = negated

    def eval(self, env):
        if self.negated:
            return not_(env[self.variable])
        return env[self.variable]

    def __repr__(self):
        negation = ''
        if self.negated:
            negation = '~'
        return '{}{}'.format(negation, self.variable)


class Expression:
    """
    Model a sentential logic subexpression
    with a tree-like structure.
    """
    def __init__(self, bin_op=None, left=None, right=None, negated=False):
        self.bin_op = bin_op
        self.left = left
        self.right = right
        self.negated = negated

    def eval(self, env):
        if self.bin_op is None:
            if self.negated:
                return not_(self.left.eval(env))
            return self.left.eval(env)
        else:
            evaluation = self.bin_op(self.left.eval(env), self.right.eval(env))
            if self.negated:
                return not_(evaluation)
            return evaluation

    def __repr__(self):
        negation = ''
        if self.negated:
            negation = '~'

        if self.bin_op is None:
            bin_op = ''
        else:
            bin_op = self.bin_op

        if self.right is None:
            right = ''
        else:
            right = self.right

        if bin_op == '':
            return '{}({})'.format(negation, self.left)
        return '{}({} {} {})'.format(negation, self.left, bin_op, right)


def is_negation(token):
    return token in ['!', '~', 'not', '¬']


def is_variable(token):
    return token in [letter for letter in lowercase.replace('v', '')]


def collect(ast):
    if isinstance(ast[0], list):
        return ast.pop(0)

    negated = False
    while is_negation(ast[0]):
        ast.pop(0)
        negated = not_(negated)
    if is_variable(ast[0]):
        return Term(ast.pop(0), negated=negated)
    return negated

def neither_negation_nor_variable(t):
    return (not is_negation(t)) and (not is_variable(t))


def ast_is_a_term(ast):
    if neither_negation_nor_variable(ast[0]):
        return False
    for item in ast:
        if neither_negation_nor_variable(item):
            return False
    return True

def expressify(proposition):
    prop = deepcopy(proposition)
    if isinstance(prop, Proposition):
        return _treeify(prop.raw_ast)
    return _treeify(prop)


def _treeify(ast, next_negation=None, previous_level_was_negated=False):
    """
    Convert nested-list AST into a tree.

    The returned node will be the root.
    """
    preceding_negation = False

    negation_or_term = collect(ast)
    if isinstance(negation_or_term, bool):
        preceding_negation = negation_or_term
        left_term = collect(ast)
    else:
        left_term = negation_or_term

    if len(ast) == 0:
        if isinstance(left_term, Term):
            return Expression(bin_op=None,
                    left=left_term,
                    right=None,
                    negated=preceding_negation)
        elif isinstance(left_term, list) and ast_is_a_term(left_term):
            return Expression(bin_op=None,
                    left=collect(left_term),
                    right=None,
                    negated=preceding_negation)
        else: # The negation needs to get passed to the subsequent call to _treeify
            return Expression(bin_op=None,
                    left=_treeify(left_term, previous_level_was_negated=preceding_negation),
                    right=None,
                    negated=previous_level_was_negated)
    else:
        bin_op = ast.pop(0)

    negation_or_term = collect(ast)
    if isinstance(negation_or_term, bool):
        next_negation = negation_or_term
        right_term = collect(ast)
    else:
        right_term = negation_or_term

    if isinstance(left_term, list):
        left_term = _treeify(left_term, previous_level_was_negated=preceding_negation)

    if isinstance(right_term, list):
        right_term = _treeify(right_term, previous_level_was_negated=next_negation)

    return Expression(bin_op, left_term, right_term, negated=previous_level_was_negated)


def listify_Expression(expression_node):
    """
    Convert a tree into a nested-list AST.
    """
    list_rep = []

    if isinstance(expression_node.left, Term):
        list_rep.append(expression_node.left)
    if isinstance(expression_node.left, Expression):
        list_rep.append(listify_Expression(expression_node.left))

    list_rep.append(expression_node.bin_op)

    if isinstance(expression_node.right, Term):
        list_rep.append(expression_node.right)
    if isinstance(expression_node.right, Expression):
        list_rep.append(listify_Expression(expression_node.right))

    return list_rep
