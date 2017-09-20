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


''' More generic cases '''
def single_term_proposition():
    assert group_cnf(cnf(expressify(Proposition('''p''')))) == [{'p'}]


def single_negated_term_proposition():
    assert group_cnf(cnf(expressify(Proposition('''!r''')))) == [{'~r'}]


'''These examples from: http://intrologic.stanford.edu/exercises/exercise_05_01.html '''
def test_prob_1():
    assert group_cnf(cnf(expressify(Proposition('''(p & q) -> (r v s)''')))) == [{'r', 's', '~p', '~q'}]


def test_prob_2():
    assert group_cnf(cnf(expressify(Proposition('''(p v q) -> (r v s)''')))) == [{'r', 's', '~p'}, {'r', 's', '~q'}]


def test_prob_3():
    assert group_cnf(cnf(expressify(Proposition('''~(p v (q v r))''')))) == [{'~q'}, {'~r'}, {'~p'}]


def test_prob_4():
    assert group_cnf(cnf(expressify(Proposition('''~(p & (q & r))''')))) == [{'~p', '~q', '~r'}]


def test_prob_5():
    assert group_cnf(cnf(expressify(Proposition('''(p & q) <-> r''')))) == [{'p', '~r'}, {'q', '~r'}, {'r', '~p', '~q'}]


def test_biconditional():
    assert group_cnf(cnf(expressify(Proposition('''c <-> z''')))) == [{'z', '~c'}, {'c', '~z'}]


def test_negated_biconditional():
    assert group_cnf(cnf(expressify(Proposition('''!(c <-> z)''')))) == [{'c', 'z'}, {'~c', '~z'}]
