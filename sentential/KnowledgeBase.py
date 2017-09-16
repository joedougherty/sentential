# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple
from copy import copy, deepcopy

from sentential.Expression import expressify
from sentential.rewrite_rules import cnf, group_cnf, negate, terms_are_complements
print('Update these imports before re-integrating into core project!')


class KnowledgeBase:
    def __init__(self):
        self._axioms = OrderedDict()
        self._goal = None

    def add_axiom(self, axiom_as_prop, axiom_is_goal=False):
        if axiom_is_goal:
            cnf_exp = cnf(negate(expressify(axiom_as_prop)))
        else:
            cnf_exp = cnf(expressify(axiom_as_prop))

        cnf_clauses = group_cnf(cnf_exp)

        self._axioms[len(self._axioms)] = {'proposition': axiom_as_prop, 
                                           'cnf': cnf_exp, 
                                           'clauses': cnf_clauses}

    def add_goal(self, goal_as_prop):
        self._goal = new_clause

        cnf_expr = cnf(negate(expressify(goal_as_prop)))
        clauses = group_cnf(cnf_expr)

        self._axioms[len(self._axioms)] = {'proposition': goal_as_prop,
                                           'cnf': cnf_expr,
                                           'clauses': clauses}

    def _gather_clauses(self):
        clause_collection = []
        for idx, axiom in self._axioms.items():
            clause_collection = clause_collection + axiom.get('clauses')
        return clause_collection

    def prove(self, goal=None):
        if goal is None:
            goal = self._goal

        raise NotImplementedError
        
        proof_attempt = Proof(goal, negated_goal, self._gather_clauses())
        return proof_attempt.search()
