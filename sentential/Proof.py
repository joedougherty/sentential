# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import copy, deepcopy

resolution_result = namedtuple('resolution_result', ['clause', 'resolved_by'])

class ResolutionAttempt:
    def __init__(self, c1_set, c2_set, resolve_by, resolvent=None):
        self.c1, self.c2 = frozenset(c1_set), frozenset(c2_set)
        self.resolve_by = resolve_by
        self.resolvent = resolvent

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            clauses_match = ((self.c1 == other.c1 and self.c2 == other.c2) or
                             (self.c1 == other.c2 and self.c2 == other.c1))
            if clauses_match and (self.resolve_by == other.resolve_by):
                return True
        return False

    def __hash__(self):
        return hash(frozenset((self.c1, self.c2, self.resolve_by)))

    def __repr__(self):
        return """{{{}, {}}}, resolve_by='{}', resolvent='{}'""".format(self.c1, self.c2, self.resolve_by, self.resolvent)


def minimum_pair_comparisons(L):
    if isinstance(L, set):
        L = list(L)

    retlist = []
    for idx, item in enumerate(L):
        for element in L[idx+1:]:
            retlist.append((item, element))
    return retlist


def negate_literal(literal):
    if literal[0] == '~':
        return literal[1]
    return '~{}'.format(literal)


def would_resolve(c1, c2):
    if c1 == c2:
        return False

    literals_to_resolve_by = []
    for literal in c1:
        if negate_literal(literal) in c2:
            literals_to_resolve_by.append(literal)

    if not literals_to_resolve_by:
        return False
    else:
        return literals_to_resolve_by


def extract_clause_literal(clause):
    for i in clause:
        return str(i)


def _resolve(c1, c2):
    c1, c2 = set(deepcopy(c1)), set(deepcopy(c2))
    for literal in c1:
        if negate_literal(literal) in c2:
            combined_clause = c1
            combined_clause.update(c2)
            combined_clause.remove(literal)
            combined_clause.remove(negate_literal(literal))
            return resolution_result(frozenset(combined_clause), literal)
    raise Exception("Could not resolve {} and {}!".format(c1, c2))


def resolve(c1, c2, resolve_by=None):
    if resolve_by:
        c1, c2 = set(deepcopy(c1)), set(deepcopy(c2))
        combined_clause = c1
        combined_clause.update(c2)
        combined_clause.remove(resolve_by)
        combined_clause.remove(negate_literal(resolve_by))
        return resolution_result(frozenset(combined_clause), resolve_by)
    else:
        return _resolve(c1, c2)


class Proof:
    def __init__(self, goal_as_cnf_clause, negated_goal_as_cnf_clause, clause_collection, debug=False):
        if isinstance(goal_as_cnf_clause, set):
            self.goal = [frozenset(goal_as_cnf_clause)]
        elif isinstance(goal_as_cnf_clause, list):
            self.goal = [frozenset(c) for c in goal_as_cnf_clause]
        else:
            raise Exception("I don't know how to handle {}".format(goal_as_cnf_clause))

        if isinstance(negated_goal_as_cnf_clause, set):
            self.negated_goal = [frozenset(negated_goal_as_cnf_clause)]
        elif isinstance(negated_goal_as_cnf_clause, list):
            self.negated_goal = [frozenset(c) for c in negated_goal_as_cnf_clause]
        else:
            raise Exception("I don't know how to handle {}".format(negated_goal_as_cnf_clause))

        self.clause_collection = set([frozenset(c) for c in clause_collection])
        self.attempted_combinations = set()
        self.set_of_support = set()
        [self.set_of_support.add(clause) for clause in self.negated_goal]
        self.at_least_one_goal_containing_clause_exists = False
        self.steps = list()

    def resolve(self, c1,  c2, resolve_by=None):
        if not resolve_by:
            resolvent = resolve(c1, c2)
        else:
            resolvent = resolve(c1, c2, resolve_by)

        self.clause_collection.add(resolvent.clause)

        if c1 in self.set_of_support or c2 in self.set_of_support:
            self.set_of_support.add(resolvent.clause)

        self.attempted_combinations.add(ResolutionAttempt(c1, c2, resolvent.resolved_by))
        self.steps.append(ResolutionAttempt(c1, c2, resolvent.resolved_by, resolvent=resolvent.clause))

    def cannot_resolve_further(self):
        for pair_of_clauses in minimum_pair_comparisons(self.clause_collection):
            c1, c2 = pair_of_clauses
            potential_resolvents = would_resolve(c1, c2)
            if potential_resolvents:
                for literal in potential_resolvents:
                    if ResolutionAttempt(c1, c2, literal) not in self.attempted_combinations:
                        self.resolve(c1, c2, literal)
        return True

    def prove_by_set_of_support(self):
        for clause in sorted(self.set_of_support, key=lambda x: len(x)):
            for new_clause in sorted(self.clause_collection, key=lambda x: len(x)):
                c1, c2 = copy(clause), copy(new_clause)
                potential_resolvents = would_resolve(c1, c2)
                if potential_resolvents:
                    for literal in potential_resolvents:
                        if ResolutionAttempt(c1, c2, literal) not in self.attempted_combinations:
                            self.resolve(c1, c2)
                            return True
        return False

    def complementary_unit_clauses_exist(self):
        for pair_of_clauses in minimum_pair_comparisons([c for c in self.clause_collection if len(c) == 1]):
            c1, c2 = pair_of_clauses
            potential_literals = would_resolve(c1, c2)
            if potential_literals:
                for literal in potential_literals:
                    self.resolve(c1, c2, resolve_by=literal)
                return True
        return False

    def _find(self):
        if (set() in self.clause_collection) or (frozenset([]) in self.clause_collection):
            return True
        elif self.prove_by_set_of_support():
            return self._find()
        elif self.complementary_unit_clauses_exist():
            return self._find()
        elif self.cannot_resolve_further():
            return False
        else:
            if self.cannot_resolve_further is False:
                msg = "Evidently, there are still more possible clause combinations, but SOS thinks it is exhausted.\n"
                msg += "Pretty sure this is not theoretically possible, so now you have an excellent opportunity to \n"
                msg += "find and patch an important bug!\n"
                raise Exception(msg)
            return self._find()

    def find(self):
        self.conclusion = self._find()
        return self.conclusion
