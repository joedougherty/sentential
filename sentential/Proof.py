# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple
from copy import copy, deepcopy

from .Expression import expressify
from .rewrite_rules import cnf, group_cnf, negate, terms_are_complements


class ClausePair:
    def __init__(self, c1_set, c2_set):
        self.c1, self.c2 = frozenset(c1_set), frozenset(c2_set)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return ((self.c1 == other.c1 and self.c2 == other.c2) or
                    (self.c1 == other.c2 and self.c2 == other.c1))
        return False

    def __hash__(self):
        return hash(frozenset((self.c1, self.c2)))


def minimum_pair_comparisons(L):
    if isinstance(L, set):
        L = list(L)

    retlist = []
    for idx, item in enumerate(L):
        for element in L[idx+1:]:
            retlist.append(ClausePair(item,element))
    return retlist


def negate(literal):
    if literal[0] == '~':
        return literal[1]
    return '~{}'.format(literal)


def would_resolve(c1, c2):
    if c1 == c2:
        return False

    for literal in c1:
        if negate(c1) in c2:
            return True
    return False


def extract_clause_literal(clause):
    for i in clause:
        return str(i)


def resolve(c1, c2):
    c1, c2 = deepcopy(c1), deepcopy(c2)
    for literal in c1:
        if negate(literal) in c2:
            combined_clause = c1
            combined_clause.update(c2)
            combined_clause.remove(literal)
            combined_clause.remove(negate(literal))
            return frozenset(combined_clause)
    raise Exception("Could not resolve {} and {}!".format(c1, c2))


class Proof:
    def __init__(self, goal_as_cnf_clause, negated_goal_as_cnf_clause, clause_collection):
        self.goal = frozenset(goal_as_cnf_clause)
        self.negated_goal = frozenset(negated_goal_as_cnf_clause)
        self.clause_collection = set([frozenset(c) for c in clause_collection])
        self.attempted_combinations = set()
        self.set_of_support = set(self.negated_goal)
        self.at_least_one_goal_containing_clause_exists = False

        if not self.there_are_clauses_that_contain_goal():
            raise Exception("There are no clauses that contain the goal!")
        else:
            self.at_least_one_goal_containing_clause_exists = True

    def there_are_clauses_that_contain_goal(self):
        if self.at_least_one_goal_containing_clause_exists:
            return True

        for clause in self.clause_collection:
            if extract_clause_literal(self.goal) in clause:
                return True
        return False

    def resolve(self, c1, c2):
        resolvent = resolve(c1, c2)
        self.clause_collection.add(resolvent)

        if c1 in self.set_of_support or c2 in self.set_of_support:
            self.set_of_support.add(resolvent)
           
        self.attempted_combinations.add(ClausePair(c1, c2))

    def cannot_resolve_further(self):
        for pair_of_clauses in minimum_pair_comparisons(self.clause_collection):
            if (ClausePair(pair_of_clauses.c1, pair_of_clauses.c2) not in self.attempted_combinations and
		would_resolve(pair_of_clauses.c1, pair_of_clauses.c2)):
                return False
        return True

    def prove_by_set_of_support(self):
        for clause in sorted(self.set_of_support, key=lambda x: len(x.clause)):
            for new_clause in sorted(self.clause_collection, key=lambda x: len(x.clause)):
                c1, c2 = clause, new_clause
                if (ClausePair(c1.clause, c2.clause) not in self.attempted_combinations and
		    would_resolve(c1.clause, c2.clause)):
                        resolvent = resolve(c1, c2)
                        self.clause_collection.add(resolvent)
                        self.set_of_support.add(resolvent)
                        self.attempted_combinations.add(ClausePair(clause, new_clause))
                        return True
        return False

    def main(self):
        if (self.negated_goal in self.clause_collection) and (self.goal in self.clause_collection):
            return True

        if self.prove_by_set_of_support():
            return self.main()

        if self.cannot_resolve_further():
            return False

        # Consider trying to generate/detect cases where:
        #   prove_by_set_of_support returns False *AND*
        #   cannot_resolve_futher return True
        #
        # If cases like this can occur, there's a chance of
        # getting stuck in an infinite loop

        return self.main()
