# -*- coding: utf-8 -*-

from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

def test_cc_for_biconditional_introduction():
    kb = KnowledgeBase()

    axioms = ['e -> f', 'f -> e']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''e <-> f'''))

    p = kb.prove(return_proof=True)
    cc = {frozenset({'e', 'f'}), frozenset({'e', '~f'}), frozenset({'~e', '~f'}), frozenset({'f', '~e'})}
    
    assert p.clause_collection == cc
