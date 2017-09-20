from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

''' 
Test known rules of inference
Source: https://en.wikipedia.org/wiki/List_of_rules_of_inference
'''

def test_case_analysis():
    kb = KnowledgeBase()

    axioms = ['a -> b', 'c -> b', 'a v c']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''b'''))

    assert kb.prove() == True


def test_disjunctive_syllogism_v1():
    kb = KnowledgeBase()

    axioms = ['p v q', '~p']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q'''))

    assert kb.prove() == True


def test_disjunctive_syllogism_v2():
    kb = KnowledgeBase()

    axioms = ['p v q', '~q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''p'''))

    assert kb.prove() == True


def test_constructive_dilemma():
    kb = KnowledgeBase()

    axioms = ['a -> b', 'c -> d', 'a v c']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''(b v d)'''))

    assert kb.prove() == True


def test_biconditional_introduction():
    kb = KnowledgeBase()

    axioms = ['e -> f', 'f -> e']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''e <-> f'''))

    assert kb.prove() == True


def test_biconditional_elimination_v1():
    kb = KnowledgeBase()

    axioms = ['p = q', 'p']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q'''))

    assert kb.prove() == True


def test_biconditional_elimination_v2():
    kb = KnowledgeBase()

    axioms = ['p = q', 'q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''p'''))

    assert kb.prove() == True


def test_biconditional_elimination_v3():
    kb = KnowledgeBase()

    axioms = ['p = q', '!p']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~q'''))

    assert kb.prove() == True


def test_biconditional_elimination_v4():
    kb = KnowledgeBase()

    axioms = ['p = q', '¬q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''!p'''))

    assert kb.prove() == True


def test_biconditional_elimination_v5():
    kb = KnowledgeBase()

    axioms = ['j <-> r', 'r v j']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''(r & j)'''))

    assert kb.prove() == True


def test_biconditional_elimination_v6():
    kb = KnowledgeBase()

    axioms = ['j <-> r', '~r v ~j']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''(~r & ~j)'''))

    assert kb.prove() == True
