from collections import namedtuple
from operator import not_

from sentential.evaluator import resolve_term_negation

"""
Provides models and tools for converting a nested list AST 
into a tree model (given by ExprNode) and vice versa.
"""

token = namedtuple('token', ['TOKENTYPE', 'token']) 

class ExprNode:
    """
    Model a sentential logic subexpression 
    with a binary tree-like structure.
    """
    def __init__(self, bin_op, left, right):
        self.bin_op = bin_op
        self.left = left
        self.right = right
        
    def resolve_term(self, term):
        if isinstance(term, NodeExpr):
            return self.resolve_term(term)
        else:
            if term[0] == not_:
                return resolve_term_negation(term)
            return term[0]

    def eval(self):
        return bin_op(resolve_term(left), resolve_term(right))


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
