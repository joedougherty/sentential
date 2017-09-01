from sentential.Expression import expressify, collect
from sentential.rewrite_rules import cnf, group_cnf
from sentential import Proposition

''' These examples from page 28 of:
    https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/lecture-notes/Lecture7FinalPart1.pdf '''

def test_first_prop():
    assert group_cnf(cnf(expressify(Proposition('''(p -> q) -> q''')))) == [{'p', 'q'}]

def test_second_prop():
    assert group_cnf(cnf(expressify(Proposition('''(p -> p) -> r''')))) == [{'p', 'r'}, {'r', '~p'}]

def test_third_prop():
    assert group_cnf(cnf(expressify(Proposition('''(r -> s) -> ~(s -> q)''')))) == [{'r', 's'}, {'r', '~q'}, {'~q', '~s'}]
