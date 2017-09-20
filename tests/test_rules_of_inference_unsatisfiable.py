# -*- coding: utf-8 -*-

from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

''' 
Test known rules of inference
Source: https://en.wikipedia.org/wiki/List_of_rules_of_inference
'''

def test_biconditional_elimination_unsatisifiable_unrelated_prop():
    kb = KnowledgeBase()

    axioms = ['j <-> r', '~r v ~j']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''l'''))

    assert kb.prove() == False
