from sentential.sentential import same_truth_table
from sentential import Proposition
from sentential.rewrite_rules import cnf
from sentential.Expression import expressify


def test_simple_prop_cnf_has_same_truth_table():
    pq = Proposition('''p -> q''')
    pq_cnf = Proposition(str(cnf(expressify(pq))))
    assert same_truth_table(pq, pq_cnf)


def test_complex_prop_cnf_has_same_truth_table():
    pqrst = Proposition('''((p v q) -> (r -> s)) <-> ~t''')
    pqrst_cnf = Proposition(str(cnf(expressify(pqrst))))
    assert same_truth_table(pqrst, pqrst_cnf)
