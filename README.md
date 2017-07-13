# SENTENTIAL #

An interpreter for sentential logic (propositional calculus) written in Python.

Very much a work in progress.


    Evaluate a proposition in sentential logic.

    Usage::
    >>> lnc = Proposition('''¬(p & ¬p)''')
    <Proposition.Proposition at 0x7f8490845978>

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
