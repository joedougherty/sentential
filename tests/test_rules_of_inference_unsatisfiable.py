# -*- coding: utf-8 -*-

from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

''' 
Think of this as the complement to test_rules_of_inference.

Where test_rules_of_inference verifies that a set of axioms
can produce a proof for a known rule of inference, 
test_rules_of_inference_unsatisfiable tests cases that *should not*
be provable.
'''

def test_case_analysis_unsat():
    kb = KnowledgeBase()

    axioms = ['a -> b', 'c -> b', 'a v c']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~b'''))

    assert kb.prove() == False


def test_disjunctive_syllogism_unsat_v1():
    kb = KnowledgeBase()

    axioms = ['p v q', '~p']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~q'''))

    assert kb.prove() == False


def test_disjunctive_syllogism_unsat_v2():
    kb = KnowledgeBase()

    axioms = ['p v q', '~q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~p'''))

    assert kb.prove() == False


def test_constructive_dilemma():
    kb = KnowledgeBase()

    axioms = ['a -> b', 'c -> d', 'a v c']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~(b v d)'''))

    assert kb.prove() == False
