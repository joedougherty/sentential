from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

def test_minimal_kb_proof():
    kb = KnowledgeBase()

    pq = Proposition('''p v q''')
    pr = Proposition('''p -> r''')
    qr = Proposition('''q -> r''')

    kb.add_axiom(pq)
    kb.add_axiom(pr)
    kb.add_axiom(qr)

    r = Proposition('''r''')
    kb.add_goal(r)
    conclusion = kb.prove()
    assert conclusion == True


def test_unsatisfiable_clause_collection():
    ''' http://intrologic.stanford.edu/exercises/exercise_05_03.html '''
    goal_as_prop = Proposition('''p v q''')
    goal = group_cnf(cnf(expressify(goal_as_prop)))

    negated_goal_as_prop = Proposition('''!(p v q)''')
    negated_goal = group_cnf(cnf(expressify(negated_goal_as_prop)))

    c1, c2, c3, c4 = goal[0], {'~p', 'r'}, {'~p', '~r'}, {'p', '~q'}

    goal = c1
    unsatisfiable = Proof(goal, negated_goal, clause_collection=[c1, c2, c3, c4])
    # If a contradiction (empty clause) is found, the set of clauses is unsatisfiable
    assert unsatisfiable.find() == True


def test_multiple_goal_clauses():
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''p -> q'''))
    kb.add_axiom(Proposition('''r -> s'''))
    kb.add_goal(Proposition('''(p v r) -> (q v s)'''))

    assert kb.prove() == True


def test_another_multiple_goal_clauses():
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''(p -> q) -> q'''))
    kb.add_axiom(Proposition('''(p -> p) -> r'''))
    kb.add_axiom(Proposition('''(r -> s) -> ~(s -> q)'''))
    kb.add_goal(Proposition('''r'''))

    assert kb.prove() == True


def test_medium_sized_kb():
    ''' https://www.ics.uci.edu/~welling/teaching/271fall09/HW6_sol.pdf '''
    kb = KnowledgeBase()

    axioms = ['a', 'b', 'c', '(a & b) -> d', '(b & d) -> f', 'f -> g', '(a & e) -> h', '(a & c) -> e']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''h'''))

    assert kb.prove() == True


def test_modus_ponens():
    kb = KnowledgeBase()

    axioms = ['p -> q', 'p']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q'''))

    assert kb.prove() == True


def test_modus_tollens():
    kb = KnowledgeBase()

    axioms = ['p -> q', '~q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''~p'''))

    assert kb.prove() == True


def test_hypothetical_syllogism():
    kb = KnowledgeBase()

    axioms = ['a -> b', 'b -> c', 'c -> d', 'd -> e', 'e -> f', 'f -> g', 'a']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''g'''))

    assert kb.prove() == True


def test_affirming_the_consequent():
    ''' Affirming the consequent should return False '''
    kb = KnowledgeBase()

    axioms = ['p -> q', 'q']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''p'''))

    assert kb.prove() == False


def test_constructive_dilemma():
    '''
    It is the inference that, if P implies Q and R implies S and either P or R is true, then Q or S has to be true.
    Source: https://en.wikipedia.org/wiki/Constructive_dilemma
    '''
    kb = KnowledgeBase()

    axioms = ['p -> q', 'r -> s', 'p v r']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q v s'''))

    assert kb.prove() == True


def test_contraposition_theorem():
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''p -> q'''))
    kb.add_goal(Proposition('''(~q -> ~p)'''))

    assert kb.prove() == True


def test_implication_distribution():
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''p -> (q -> r)'''))
    kb.add_goal(Proposition('''(p -> q) -> (p -> r)'''))

    assert kb.prove() == True


def test_absorption():
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''(p -> q)'''))
    kb.add_axiom(Proposition('''(p -> (p & q))'''))
    kb.add_goal(Proposition('''(p -> q)'''))

    assert kb.prove() == True


def test_exercise_5_4():
    ''' http://intrologic.stanford.edu/exercises/exercise_05_04.html '''
    kb = KnowledgeBase()

    kb.add_axiom(Proposition('''p -> q'''))
    kb.add_axiom(Proposition('''r -> s'''))
    kb.add_goal(Proposition('''(p v r) -> (q v s)'''))

    assert kb.prove() == True


def test_lnc_is_theorem():
    kb = KnowledgeBase()

    lnc = Proposition('''~(p & ~p)''')

    kb.add_axiom(lnc)
    kb.add_goal(lnc)

    assert kb.prove() == True


def test_lem_is_theorem():
    kb = KnowledgeBase()

    lem = Proposition('''p v ~p''')
    kb.add_axiom(lem)
    kb.add_goal(lem)

    assert kb.prove() == True


def test_lnc_conflicts_with_negated_lnc():
    """ You should *not* be able to derive a negation of a theorem (from itself)! """
    kb = KnowledgeBase()

    lnc = Proposition('''~(p & ~p)''')
    negated_lnc = Proposition('''~(~(p & ~p))''')

    kb.add_axiom(lnc)
    kb.add_goal(negated_lnc)

    assert kb.prove() == False


def test_lem_and_lnc_imply_one_another():
    kb = KnowledgeBase()

    lem = Proposition('''p v ~p''')
    lnc = Proposition('''~(p & ~p)''')

    kb.add_axiom(lem)
    kb.add_goal(lnc)

    assert kb.prove() == True
