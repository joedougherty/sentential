# -*- coding: utf-8 -*-

from collections import OrderedDict

from .Expression import expressify
from .Proof import Proof
from .ProofGraph import ProofGraph
from .Proposition import Proposition
from .rewrite_rules import cnf, group_cnf, negate


class KnowledgeBase:
    def __init__(self):
        self._axioms = OrderedDict()
        self._goal = None
        self.run_proofs = list()

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
        if self._goal:
            raise Exception("{} is already defined as the goal! Use .remove_goal() before adding a new goal.".format(self._goal))

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

    def _gather_clauses(self):
        clause_collection = []
        for idx, axiom in self._axioms.items():
            clause_collection = clause_collection + axiom.get('clauses')
        return clause_collection

    def most_recent_proof(self):
        if self.run_proofs:
            return self.run_proofs[-1]
        else:
            raise Exception("Run a proof first!")

    def prove(self, goal=None, return_proof=False):
        if goal is None:
            if not hasattr(self, '_goal_as_unit_clause'):
                raise Exception("You must set a goal before running a proof!")
            goal = self._goal_as_unit_clause
        else:
            self.remove_goal()
            self.add_goal(goal)

        negated_goal = self._negated_goal_as_unit_clause
        proof_attempt = Proof(goal, negated_goal, self._gather_clauses())
        self.run_proofs.append(proof_attempt)

        if return_proof:
            return proof_attempt

        try:
            return proof_attempt.find(trace=True)
        except Exception as e:
            print(e)
            print('Clause Collection: {}'.format(proof_attempt.clause_collection))
            print('Set of Support: {}'.format(proof_attempt.set_of_support))
            return proof_attempt

    def visualize(self, steps=None):
        if steps is None:
            s = self.most_recent_proof().steps
        else:
            s = steps

        pg = ProofGraph(s)
        dot = pg.generate()

        dot.view()
