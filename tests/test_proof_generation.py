from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase 
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

pq = Proposition('''p v q''')
pr = Proposition('''p -> r''')
qr = Proposition('''q -> r''')

# TEST GOALS
r = Proposition('''r''')
not_r = Proposition('''!r''')

def test_minimal_kb_proof():
    kb = KnowledgeBase()

    kb.add_axiom(pq)
    kb.add_axiom(pr)
    kb.add_axiom(qr)
    kb.add_goal(r)
    conclusion = kb.prove()
    assert conclusion == True

def test_unsatisfiable_clause_collection():
    ''' http://intrologic.stanford.edu/exercises/exercise_05_03.html '''
    kb = KnowledgeBase()

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

''' https://www.ics.uci.edu/~welling/teaching/271fall09/HW6_sol.pdf '''

def test_medium_sized_kb():
    kb = KnowledgeBase()

    axioms = ['a', 'b', 'c', '(a & b) -> d', '(b & d) -> f', 'f -> g', '(a & e) -> h', '(a & c) -> e']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''h'''))

    assert kb.prove() == True

def test_medium_sized_kb_v2():
    kb = KnowledgeBase()

    axioms = ['p -> q', 'e -> b', 'r -> q', '(m & n) -> q', '(a & b) -> p', 'a -> m', 'c -> m', 'd -> n', 'd', 'a']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q'''))

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

def test_construtive_dilemma():
    '''
    It is the inference that, if P implies Q and R implies S and either P or R is true, then Q or S has to be true.
    Source: https://en.wikipedia.org/wiki/Constructive_dilemma
    '''
    kb = KnowledgeBase()

    axioms = ['p -> q', 'r -> s', 'p v r']
    [kb.add_axiom(Proposition(statement)) for statement in axioms]
    kb.add_goal(Proposition('''q v s'''))

    assert kb.prove() == True
