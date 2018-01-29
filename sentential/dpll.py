# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import copy, deepcopy

from .ProofGraph import ProofGraph
from .rewrite_rules import clause_is_tautology

            
#####################################################################    
# ASSUMPTION:                                                       #
#                                                                   #
#   Each clause collection (as cc) has the following properties:    #
#                                                                   #
#       + cc.as_lists: representation of CNF as lists               #
#           (ex: [['p', '~q'], ['~p', '~q', 'r']])                  #
#                                                                   #
#       + cc.variables: tuple of "positivized" literals             #
#          (ex: ('p', 'q, 'r'))                                     #
#                                                                   #
#####################################################################


class ClauseCollection:
    def __init__(self, clauses_as_list):
        self.as_list = clauses_as_list

        variables = set()
        for clause in clauses_as_list:
            for var in clause:
                variables.add(var[-1])

        self.variables = list(variables)

    def next_variable(self):
        if len(self.variables) > 0:
            return self.variables.pop(0)
        return False


def is_negated(literal):
    return literal[0] in ('!', '~', '¬')


def contains_unit_clause(clause_collection):
    for clause in clause_collection:
        if len(clause) == 1:
            return clause.pop()
    return False


def dpll(clause_collection):
    if clause_collection == []:
        return True

    if [] in clause_collection:
        return False

    unit_clause_literal = contains_unit_clause(clause_collection)
    if unit_clause_literal:
        return dpll(simplify(clause_collection, unit_clause_literal))

    variable = clause_collection.next_variable()
    negated  = '~{}'.format(variable)

    if dpll(simplify(clause_collection, variable)):
        return True
    return dpll(simplify(clause_collection, negated))


def simplify(clause_collection, literal):
    if is_negated(literal):
        positive, negative = literal[0], literal
    else:
        positive, negative = literal, '~{}'.format(literal)

    for idx, clause in enumerate(clause_collection):
        if positive in clause:
            del clause_collection[idx]

        if negative in clause:
            del clause[clause.index(negative)]

    return clause_collection
