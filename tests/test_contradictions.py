# -*- coding: utf-8 -*-

from sentential.sentential import same_truth_table
from sentential import Proposition


def test_negated_lnc():
    prop = Proposition('''~(~(p and ~p))''')
    assert prop.is_contradiction() == True


def test_negated_lem():
    prop = Proposition('''~(p or ~p)''')
    assert prop.is_contradiction() == True
