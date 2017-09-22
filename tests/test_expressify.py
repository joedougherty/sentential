# -*- coding: utf-8 -*-

from sentential import Proposition
from sentential.Expression import expressify
from sentential.KnowledgeBase import KnowledgeBase
from sentential.Proof import Proof
from sentential.rewrite_rules import group_cnf, cnf

def test_single_term_expression():
    assert str(expressify(Proposition('''p'''))) == '(p)'


def test_single_term_negated_expression():
    assert str(expressify(Proposition('''!p'''))) == '(~p)'


def test_single_term_double_negated_expression():
    assert str(expressify(Proposition('''~(!p)'''))) == '~(~p)'


def test_complex_expression():
    assert str(expressify(Proposition('''~(b v d) -> ~!(!r)'''))) == '(~(b v d) -> (~r))'
