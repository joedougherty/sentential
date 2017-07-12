# -*- coding: utf-8 -*-

from grammar import expression_is_grammatical
from parser import tokenize, balanced_parens
from utils import parenthesize
from sentential import derive_truth_value, generate_all_possible_truth_vals


class Proposition:
    def __init__(self, expr):
        balanced_parens(parenthesize(expr))
        expression_is_grammatical(tokenize(parenthesize(expr)))
        self.expr = expr
        self._truth_table = None

    def truth_table(self):
        """
        This method caches a computed truth table in self.truth_table.
        """
        if not self._truth_table:
            self._truth_table = self._compute_truth_table()
        return self._truth_table

    def _compute_truth_table(self):
        var_truth_vals = generate_all_possible_truth_vals(self.expr)
        for tv_dict in var_truth_vals:
            tv_dict['expr_truth_value'] = derive_truth_value(self.expr, tv_dict)
        return var_truth_vals

    def is_theorem(self):
        for tv_dict in self.truth_table():
            if tv_dict['expr_truth_value'] == False:
                return False
        return True
