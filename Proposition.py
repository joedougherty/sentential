# -*- coding: utf-8 -*-

from prettytable import PrettyTable

from grammar import expression_is_grammatical
from parser import tokenize, balanced_parens
from utils import parenthesize, extract_variables
from sentential import derive_truth_value, generate_all_possible_truth_vals


class Proposition:
    """
    Evaluate a proposition in sentential logic.

    Usage::
    >>> lnc = Proposition('''¬(p & ¬p)''')
    <Proposition.Proposition at 0x7f8490845978>

    >>> lnc.truth_table()
    [OrderedDict([('p', True), ('expr_truth_value', True)]),
     OrderedDict([('p', False), ('expr_truth_value', True)])]

    >>> lnc.is_theorem()
    True

    >>> lnc.eval_expr_with_custom_var_vals({'p': False})
    True

    """
    def __init__(self, expr):
        balanced_parens(parenthesize(expr))
        expression_is_grammatical(tokenize(parenthesize(expr)))
        self.expr = expr
        self.expr_vars = extract_variables(tokenize(expr))
        self._truth_table = None

    def truth_table(self):
        """
        This method caches a computed truth table in self.truth_table.
        """
        if not self._truth_table:
            self._truth_table = self._compute_truth_table()
        return self._truth_table

    def pretty_truth_table(self):
        t = PrettyTable(self.expr_vars + [self.expr])
        t.align = 'l'
        for row in self.truth_table():
            t.add_row([row.get(x) for x in self.expr_vars] + [row.get('expr_truth_value')])
        print(t)

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

    def eval_expr_with_custom_var_vals(self, truth_values_as_dict):
        return derive_truth_value(self.expr, truth_values_as_dict)
