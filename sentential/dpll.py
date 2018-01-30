# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import copy, deepcopy

            
#####################################################################    
# ASSUMPTION:                                                       #
#                                                                   #
#   Each clause collection (as cc) has the following properties:    #
#                                                                   #
#       + cc.as_list: representation of CNF as list of sets         #
#           (ex: [['p', '~q'], ['~p', '~q', 'r']])                  #
#                                                                   #
#       + cc.variables: list of "positivized" literals              #
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


def pop_negatives(clause, negated_literal):
    return [l for l in clause if l != negated_literal]


def simplify(clause_collection, literal):
    positive, negated = literal, '~{}'.format(literal)

    sans_positives = [c for c in clause_collection if positive not in c]
    return [pop_negatives(c, negated) for c in sans_positives]
