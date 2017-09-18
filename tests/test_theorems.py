from sentential.sentential import same_truth_table
from sentential import Proposition

def test_contraposition_theorem():
    assert same_truth_table(Proposition('''(p -> q)'''), Proposition('''(~q -> ~p)'''))

def test_contraposition_via_direct_truth_table():
    prop = Proposition('''(p -> q) <-> (~q -> ~p)''')
    assert prop.is_theorem() == True

def test_implication_distribution():
    assert same_truth_table(Proposition('''p -> (q -> r)'''), Proposition('''(p -> q) -> (p -> r)'''))

def test_implication_distribution_via_direct_truth_table():
    prop = Proposition('''(p -> (q -> r)) <-> ((p -> q) -> (p -> r))''')
    assert prop.is_theorem() == True
