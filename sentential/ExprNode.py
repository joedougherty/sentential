from collections import namedtuple
from operator import not_

from .evaluator import resolve_term_negation

"""
Provides models and tools for converting a nested list AST
into a tree model (given by ExprNode) and vice versa.
"""

token = namedtuple('token', ['TOKENTYPE', 'token'])

def negation_interpreter(list_of_tokens, negation_match_test, term_match_test):
    collected = []
    while negation_match_test(list_of_tokens[0]):
        collected.append(list_of_tokens.pop(0))
    if isinstance(list_of_tokens[0], list):
        return collected
    elif term_match_test(list_of_tokens[0]):
        collected.append(list_of_tokens.pop(0))
        return collected
    else:
        raise Exception("I don't know what to do with: {}!".format(list_of_tokens[0]))

class ExprNode:
    """
    Model a sentential logic subexpression
    with a binary tree-like structure.
    """
    def __init__(self, bin_op, left, right, preceding_negations=None):
        self.bin_op = bin_op
        self.left = left
        self.right = right
        self.preceding_negations = preceding_negations

    def resolve_term(self, term):
        if isinstance(term, ExprNode):
            return term.eval()
        else:
            if term[0] == not_:
                return resolve_term_negation(term)
            return term[0]

    def eval(self):
        if self.preceding_negations is None or (self.preceding_negations % 2 == 0):
            return self.bin_op(self.resolve_term(self.left), self.resolve_term(self.right))
        else:
            return not_(self.bin_op(self.resolve_term(self.left), self.resolve_term(self.right)))


def treeify(ast):
    """
    Convert as nested-list AST into a tree.

    The returned node will be the root.
    """
    left_term, bin_op, right_term = ast

    if isinstance(left_term, list):
        left_term = treeify(left_term)

    if isinstance(right_term, list):
        right_term = treeify(right_term)

    return ExprNode(bin_op, left_term, right_term)


def listify_ExprNode(expression_node):
    """
    Convert a tree into a nested-list AST.
    """
    list_rep = []

    if isinstance(expression_node.left, token):
        list_rep.append(expression_node.left)
    if isinstance(expression_node.left, ExprNode):
        list_rep.append(listify_ExprNode(expression_node.left))

    list_rep.append(expression_node.bin_op)

    if isinstance(expression_node.right, token):
        list_rep.append(expression_node.right)
    if isinstance(expression_node.right, ExprNode):
        list_rep.append(listify_ExprNode(expression_node.right))

    return list_rep
