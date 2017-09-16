# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple
from copy import copy, deepcopy

<<<<<<< HEAD
from .Expression import expressify
from .Proof import Proof
from .Proposition import Proposition
from .rewrite_rules import cnf, group_cnf, negate, terms_are_complements
=======
from sentential.Expression import expressify
from sentential.rewrite_rules import cnf, group_cnf, negate, terms_are_complements
print('Update these imports before re-integrating into core project!')
>>>>>>> 136ed30043dc8af173f6a141f6d2f39b03858b99


class KnowledgeBase:
    def __init__(self):
        self._axioms = OrderedDict()
        self._goal = None

    def add_axiom(self, axiom_as_prop, axiom_is_goal=False):
        if axiom_is_goal:
            cnf_exp = cnf(negate(expressify(axiom_as_prop)))
        else:
            cnf_exp = cnf(expressify(axiom_as_prop))

        self._axioms[len(self._axioms)] = {'proposition': axiom_as_prop, 
                                           'cnf': cnf_exp, 
                                           'clauses': group_cnf(cnf_exp),
                                           'is_goal': axiom_is_goal}

    def add_goal(self, goal_as_prop):
        if not isinstance(goal_as_prop, Proposition):
            raise Exception("Goal must be of the type Proposition!")

        self.add_axiom(goal_as_prop, axiom_is_goal=True)
        self._goal = goal_as_prop
        self._goal_as_unit_clause = group_cnf(cnf(expressify(goal_as_prop)))
        self._negated_goal_as_unit_clause = group_cnf(cnf(negate(expressify(goal_as_prop))))

    def remove_goal(self):
        self._goal, self._goal_as_unit_clause, self._negated_goal_as_unit_clause = None, None, None
        for k, v in self._axioms.items():
            if v.get('is_goal') == True:
                del self._axioms[k]
                return True
        raise Exception("No goal currently defined!")

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
            goal = self._goal_as_unit_clause[0]
            negated_goal = self._negated_goal_as_unit_clause[0]
        else:
            self.remove_goal()
            self.add_goal(goal)

        proof_attempt = Proof(goal, negated_goal, self._gather_clauses())
        return proof_attempt
