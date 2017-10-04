SENTENTIAL
==========

.. image:: https://travis-ci.org/joedougherty/sentential.svg?branch=master
    :target: https://travis-ci.org/joedougherty/sentential

An interpreter for sentential logic (propositional calculus) written in Python.

*Very much a work in progress.*

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

    # Propositions can be combined with standard string operators
    law_of_non_contradiction = Proposition('''¬(p & ¬p)''')
    law_of_excluded_middle = Proposition('''(p v ¬p)''')

    the_nature_of_bivalence = Proposition('{} <-> {}'.format(lnc, lem))

    the_nature_of_bivalence.pretty_truth_table()


+-------+------------------------+
| p     | ¬(p & ¬p) <-> (p v ¬p) |
+-------+------------------------+
| True  | True                   |
+-------+------------------------+
| False | True                   |
+-------+------------------------+

.. code-block:: python

    # Inspect the internal representation
    law_of_non_contradiction.truth_table()

    # Results in:
    [OrderedDict([('p', True), ('expr_truth_value', True)]),
     OrderedDict([('p', False), ('expr_truth_value', True)])]


+ Determine if a proposition is a theorem/contradiction

.. code-block:: python

    law_of_non_contradiction.is_theorem() # True

    negated_lnc = Proposition('''¬(¬(p & ¬p))''')

    negated_lnc.is_contradiction() # True

**sentential** can also help you find proofs (by resolution).

.. code-block:: python
    
    from sentential import Proposition
    from sentential.KnowledgeBase import KnowledgeBase

    kb = KnowledgeBase()

    # Let's verify that we can run a proof using hypothetical syllogism 
    # (https://en.wikipedia.org/wiki/Hypothetical_syllogism)
    kb.add_axiom(Proposition('''a -> b'''))
    kb.add_axiom(Proposition('''b -> c'''))
    kb.add_axiom(Proposition('''c -> d'''))

    # Let's say we know it's the case that "a"
    kb.add_axiom(Proposition('''a'''))

    # Can we construct a proof that "d" is true (given what we know above)?
    kb.add_goal(Proposition('''d'''))

    # Indeed we can. A proof was found!
    kb.prove() # True

Proofs can be inspected further...

.. code-block:: python

    proof = kb.prove(return_proof=True)


