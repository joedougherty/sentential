# -*- coding: utf-8 -*-

from copy import deepcopy
from operator import or_, and_, not_

from .environment import conditional, biconditional
from .grammar import IFTHEN, IFF, OR, AND
from .Expression import Term, Expression

def is_bin_op(token):
    return token in IFTHEN + IFF + OR + AND


def is_flat(expression):
    return isinstance(expression.left, Term) and isinstance(expression.right, Term)


def negate(expression):
    if isinstance(expression, Expression) or isinstance(expression, Term):
        expr_copy = deepcopy(expression)
        expr_copy.negated = not_(expr_copy.negated)
        return expr_copy
    if is_bin_op(expression):
        if expression in ['&', 'and',]:
            return 'v'
        if expression in ['or', 'v',]:
            return '&'
    raise Exception("I don't know how to negate {}!".format(expr_copy))


def negation_rule(expression):
    if isinstance(expression, Expression) and expression.negated:
        expr_copy = deepcopy(expression)
        if expr_copy.bin_op is None and expr_copy.right is None:
            return negate(expression.left)
        return Expression(bin_op=negate(expression.bin_op),
                left=negate(expr_copy.left),
                right=negate(expr_copy.right), 
                negated=False)


def conditional_rule(expression):
    if isinstance(expression, Expression) and expression.bin_op in IFTHEN:
        expr_copy = deepcopy(expression)
        return Expression(bin_op='v',
                left=negate(expr_copy.left),
                right=expr_copy.right,
                negated=expr_copy.negated)


def biconditional_rule(expression):
    if isinstance(expression, Expression) and expression.bin_op in IFF:
        expr_copy = deepcopy(expression)
        return Expression(bin_op='&', 
                  left=Expression(bin_op='v', 
                      left=negate(expr_copy.left), 
                      right=expr_copy.right,
                      negated=expr_copy.negated),
                  right=Expression(bin_op='v', 
                      left=expr_copy.left, 
                      right=negate(expr_copy.right),
                      negated=expr_copy.negated))


def implication_rule(expression):
    if expression.bin_op in IFTHEN:
        return conditional_rule(expression)
    elif expression.bin_op in IFF:
        return biconditional_rule(expression)
    else:
        return expression


def distribution_rule(root):
    """
    Convert: 
        x v (y & z) <<Expression('v', 'x', Expression('&', 'y', 'z'))>>
    to: 
        (x v y) & (x v z) <<Expression('&', Expression('v', 'x', 'y'), Expression('v', 'x', 'z'))>>
    """
    if isinstance(root, Expression): 
        if isinstance(root.left, Expression) and isinstance(root.right, Term):
            distributee = root.right
            distribute_over = root.left
        else:
            if hasattr(root.right, 'bin_op') and (root.right.bin_op in AND):
                distributee = root.left
                distribute_over = root.right
            if hasattr(root.left, 'bin_op') and (root.left.bin_op in AND):
                distributee = root.right
                distribute_over = root.left

        return Expression(bin_op='&',
                            left=Expression('v',
                                left=distributee,
                                right=distribute_over.left),
                            right=Expression(bin_op='v',
                                left=distributee,
                                right=distribute_over.right))


def find_matching_node(expr, matching_fn, parent_node=None, parent_rel=None):
    if isinstance(expr, Expression) and matching_fn(expr):
        return (expr, parent_node, parent_rel)
    elif isinstance(expr, Term):
        return False
    elif expr is None:
        return False
    else: 
        left_match = find_matching_node(expr.left, matching_fn, parent_node=expr, parent_rel='left')
        right_match = find_matching_node(expr.right, matching_fn, parent_node=expr, parent_rel='right')

        if left_match:
            return left_match
        elif right_match:
            return right_match
        else:
            return False


def apply_rule(expr, rewrite_rule, matching_fn, trace=False):
    """
    Recursively apply rule until it can't be applied any more.
    """
    try:
        found_node, found_parent_node, found_parent_rel = find_matching_node(expr, matching_fn)
    except TypeError:
        found_node = find_matching_node(expr, matching_fn)                                 
        if found_node:
            raise Exception("???")
        return expr

    if trace:
        print('{} produced by {}'.format(expr, matching_fn.__name__))
                                  
    if found_parent_node is None:                                                   
        expr = rewrite_rule(found_node)
        return apply_rule(expr, rewrite_rule, matching_fn, trace=trace)                                         
    else:                                                                           
        setattr(found_parent_node, found_parent_rel, rewrite_rule(found_node))  
        return apply_rule(expr, rewrite_rule, matching_fn, trace=trace)


def convert_conjunctions_to_clauses(expression):
    return expression


def cnf(expression, trace=False):
    expression = apply_rule(expression, implication_rule, expression_is_implication, trace=trace)
    expression = apply_rule(expression, negation_rule, expression_is_negated, trace=trace)
    expression = apply_rule(expression, distribution_rule, expression_can_be_distributed, trace=trace)
    return convert_conjunctions_to_clauses(expression)

############# MATCHING RULES #############

def expression_is_negated(expression):
    return expression.negated


def expression_is_implication(expression):
    return expression.bin_op in IFTHEN + IFF


def at_least_one_side_contains_and(node):
    try:
        left_side_has_and = node.left.bin_op in AND
    except:
        left_side_has_and = False

    try:
        right_side_has_and = node.right.bin_op in AND
    except:
        right_side_has_and = False

    if (left_side_has_and or right_side_has_and):
        return True
    return False

def expression_can_be_distributed(node):
    '''
    Matching examples:
    -----------------
    p v (q & s)
    (s & r) v p
    (p & q) v (r v s)
    (p v q) v (r & s)
    (p & q) v (r & s)
    '''
    if (isinstance(node, Expression)    \
            and node.bin_op in OR       \
            and (at_least_one_side_contains_and(node) == True)):
        return True
    return False


def update_collected_terms(ct, group_cnf_call_result):
    if isinstance(group_cnf_call_result, set):
        ct.update(group_cnf_call_result)
    else:
        ct.add(group_cnf_call_result)

    return ct


def update_final_collection(fc, group_cnf_call_result):
    if isinstance(group_cnf_call_result, list):
        for item in group_cnf_call_result:
            if item not in fc:
                fc.append(item)
    else:
        if group_cnf_call_result not in fc:
            fc.append(group_cnf_call_result)

    return fc

def group_cnf(expr, previous_op=None, previous_terms=None, final_collection=None):
    if final_collection is None:
        final_collection = list()
    
    if isinstance(expr, Expression) and expr.bin_op is None:
        return group_cnf(expr.left)

    if isinstance(expr, Term):
        if previous_op in AND:
            s = set()
            s.add(expr)
            return s
        else:
            return str(expr)

    if isinstance(expr, Expression) and expr.bin_op in OR:
        if previous_op in OR:
            collected_terms = previous_terms
        else:
            collected_terms = set()

        left_result = group_cnf(expr.left, previous_op=expr.bin_op, previous_terms=collected_terms, final_collection=final_collection)
        right_result = group_cnf(expr.right, previous_op=expr.bin_op, previous_terms=collected_terms, final_collection=final_collection)

        collected_terms = update_collected_terms(collected_terms, left_result)    
        collected_terms = update_collected_terms(collected_terms, right_result)    

        if len(final_collection) == 0:
            return [collected_terms]
        else:
            return collected_terms

    if isinstance(expr, Expression) and expr.bin_op in AND:
        if final_collection is None:
            final_collection = list()

        left_result = group_cnf(expr.left, previous_op=expr.bin_op, final_collection=final_collection)
        right_result = group_cnf(expr.right, previous_op=expr.bin_op, final_collection=final_collection)

        final_collection = update_final_collection(final_collection, left_result)
        final_collection = update_final_collection(final_collection, right_result)

    return final_collection
