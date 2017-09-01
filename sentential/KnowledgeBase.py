# -*- coding: utf-8 -*-

from collections import OrderedDict
from copy import copy, deepcopy

from .Expression import expressify
from .rewrite_rules import cnf, group_cnf


def resolve(clause1, clause2):
    combined_clause = copy(clause1)
    combined_clause.update(clause2)
    for term in combined_clause:
        for t in combined_clause:
            if terms_are_complement(term, t):
                combined_clause.remove(t)
                combined_clause.remove(term)
                return combined_clause
    return combined_clause


class KnowledgeBase:
    def __init__(self):
        self._axioms = OrderedDict()
        self._clause_collection = list()

    def add_axiom(self, axiom_as_prop):
        cnf_exp = cnf(expressify(axiom_as_prop))
        cnf_clauses = group_cnf(cnf_exp)

        self._axioms[len(self._axioms)] = {'proposition': axiom_as_prop, 
                                           'cnf': cnf_exp, 
                                           'clauses': cnf_clauses}

        for clause in cnf_clauses:
            self._clause_collection.append(clause)
