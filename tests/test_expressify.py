# -*- coding: utf-8 -*-

from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf


def test_expressify_single_term_exp():
    assert str(cnf(expressify(Proposition('''p''')))) == '(p)'


def test_expressify_double_negated_single_term_exp():
    assert str(cnf(expressify(Proposition('''!!p''')))) == '(p)'


def test_expressify_double_paren_negated_single_term_exp():
    assert str(cnf(expressify(Proposition('''~(!p)''')))) == 'p'
