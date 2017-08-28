# -*- coding: utf-8 -*-

from copy import copy, deepcopy

from .rewrite_rules import cnf, group_cnf


def terms_are_complements(t1, t2):
    if len(t1) == len(t2):
        return False
    try:
        if t1 == t2[1]:
            return True
        if t1[1] == t2:
            return True
        return False
    except:
        return False


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
        self._axioms = list()
        self._clause_collection = list()
        
    def add_axiom(self, axiom_as_prop):
        for clause in group_cnf(cnf(expressify(axiom_as_prop))):
            self._clause_collection.append(clause)

