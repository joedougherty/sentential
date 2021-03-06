# -*- coding: utf-8 -*-

from prettytable import PrettyTable

from .Expression import expressify
from .grammar import expression_is_grammatical
from .parser import tokenize, balanced_parens, read_from_tokens_gen
from .rewrite_rules import group_cnf, cnf
from .sentential import derive_truth_value, generate_all_possible_truth_vals
from .subexpression import ast_is_sane
from .utils import parenthesize, extract_variables


class Proposition:
    """
    Evaluate a proposition in sentential logic.

    Usage::
    >>> lnc = Proposition('''¬(p & ¬p)''')

    >>> lnc.truth_table()
    [OrderedDict([('p', True), ('expr_truth_value', True)]),
     OrderedDict([('p', False), ('expr_truth_value', True)])]

    >>> lnc.pretty_truth_table()
    +-------+-----------+
    | p     | ¬(p & ¬p) |
    +-------+-----------+
    | True  | True      |
    | False | True      |
    +-------+-----------+

    >>> lnc.is_theorem()
    True
    """
    def __init__(self, expr, desc=None):
        balanced_parens(parenthesize(expr))
        tokens = tokenize(parenthesize(expr))
        expression_is_grammatical(tokens)
        ast = read_from_tokens_gen((t for t in tokens), evaluate_tokens=False)
        ast_is_sane(ast)    
        self.raw_ast = ast
        self.expr = expr
        self.expr_vars = extract_variables(tokenize(expr))
        self._truth_table = None
        self.desc = desc

    def truth_table(self, cond=None):
        """
        This method caches a computed truth table in self._truth_table.

        :cond: [lambda]
        An optional lambda to filter the resulting truth table.

        Example:
        =======
        >>> p.truth_table(cond=lambda row: row['p'] == True)

        You can determine the names of all the possible dict keys with:
        >>> p.truth_table()[0].keys()
        """
        if not self._truth_table:
            self._truth_table = self._compute_truth_table()

        if cond:
            return list(filter(cond, self._truth_table))
        return self._truth_table

    def pretty_truth_table(self, cond=None):
        """
        Pretty prints a truth table.

        :cond: [lambda]
        An optional lambda to filter the resulting truth table.

        Example:
        =======
        p.truth_table(cond=lambda row: row['p'] == True)
        """
        t = PrettyTable(self.expr_vars + [self.expr])
        t.align = 'l'
        for row in self.truth_table(cond=cond):
            t.add_row([row.get(x) for x in self.expr_vars] + [row.get('expr_truth_value')])
        print(t)

    def cnf(self):
        return group_cnf(cnf(expressify(self)))

    def _double_negation_elimination(self, found_terms):
        return [t.replace('~~','') for t in found_terms]

    def _negate_terms(self, row):
        terms = []
        for k, v in row.items():
            if k != 'expr_truth_value':
                if v == True:
                    terms.append('~{}'.format(k))
                else:
                    terms.append(k)

        return set(self._double_negation_elimination(terms))

    def _compute_truth_table(self, sort_vars=False):
        var_truth_vals = generate_all_possible_truth_vals(self.expr, sort_vars=sort_vars)
        for tv_dict in var_truth_vals:
            tv_dict['expr_truth_value'] = derive_truth_value(self.expr, tv_dict)
        return var_truth_vals

    def is_theorem(self):
        for tv_dict in self.truth_table():
            if tv_dict['expr_truth_value'] == False:
                return False
        return True

    def is_contradiction(self):
        for tv_dict in self.truth_table():
            if tv_dict['expr_truth_value'] == True:
                return False
        return True

    def eval_expr_with_custom_var_vals(self, truth_values_as_dict):
        return derive_truth_value(self.expr, truth_values_as_dict)

    def __repr__(self):
        """ Return a parenthesized version of the initial expression. """
        return parenthesize(self.expr)
