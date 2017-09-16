from sentential import Proposition
from sentential.KnowledgeBase import KnowledgeBase 

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
