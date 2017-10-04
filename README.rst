SENTENTIAL
==========

.. image:: https://travis-ci.org/joedougherty/sentential.svg?branch=master
    :target: https://travis-ci.org/joedougherty/sentential

An interpreter for sentential logic (propositional calculus) written in Python.

**sentential** can help you:

+ Generate truth tables

.. code-block:: python

    from sentential import Proposition
    law_of_non_contradiction = Proposition('''¬(p & ¬p)''')
    law_of_non_contradiction.pretty_truth_table()
    

    +-------+-----------+
    | p     | ¬(p & ¬p) |
    +-------+-----------+
    | True  | True      |
    +-------+-----------+
    | False | True      |
    +-------+-----------+


.. code-block:: python

	# Inspect the internal representation
    law_of_non_contradiction.truth_table()
    
    [OrderedDict([('p', True), ('expr_truth_value', True)]),
     OrderedDict([('p', False), ('expr_truth_value', True)])]


+ Determine if a proposition is a theorem/contradiction


.. code-block:: python

    law_of_non_contradiction.is_theorem()
    >>> True

	# Propositions can be combined with standard string operators
	law_of_non_contradiction = Proposition('''¬(p & ¬p)''')
	law_of_excluded_middle = Proposition('''(p v ¬p)''')

	the_nature_of_bivalence = Proposition('{} <-> {}'.format(law_of_non_contradiction.expr, law_of_excluded_middle.expr))

	the_nature_of_bivalence.pretty_truth_table()
	+-------+------------------------+
	| p     | ¬(p & ¬p) <-> (p v ¬p) |
	+-------+------------------------+
	| True  | True                   |
	| False | True                   |
	+-------+------------------------+

