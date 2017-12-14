""" This example from: https://www.cs.rochester.edu/~nelson/courses/csc_173/proplogic/resolution.html 

* Either taxes are increased or if expenditures rise then the debt ceiling is raised. 
* If taxes are increased, then the cost of collecting taxes rises. 
* If a rise in expenditures implies that the government borrows more money, then if the debt ceiling is raised, then interest rates increase. 
* If taxes are not increased and the cost of collecting taxes does not increase then if the debt ceiling is raised, 
	then the government borrows more money. 
* The cost of collecting taxes does not increase. 
* Either interest rates do not increase or the government does not borrow more money.

Prove either the debt ceiling isn't raised or expenditures don't rise.
"""

from sentential import Proposition
from sentential.KnowledgeBase import KnowledgeBase

p3 = "If a rise in expenditures implies that the government borrows more money, then if the debt ceiling is raised, then interest rates increase."
p4 = "If taxes are not increased and the cost of collecting taxes does not increase then if the debt ceiling is raised, then the government borrows more money."

kb = KnowledgeBase()

kb.add_axiom(Proposition('''(t v (e -> d))''', desc="Either taxes are increased or if expenditures rise then the debt ceiling is raised."))
kb.add_axiom(Proposition('''(t -> c)''' , desc="If taxes are increased, then the cost of collecting taxes rises."))
kb.add_axiom(Proposition('''(e & ~g) v (~d v i)''' , desc=p3))
kb.add_axiom(Proposition('''((t v c) v ~d) v g''' , desc=p4))
kb.add_axiom(Proposition('''~c''', desc="The cost of collecting taxes does not increase."))
kb.add_axiom(Proposition('''~i v ~g''', desc="Either interest rates do not increase or the government does not borrow more money."))

kb.add_goal(Proposition('''~d v ~e''', desc="The debt ceiling isn't raised or expenditures don't rise."))

# We have successfully found a proof that "The debt ceiling isn't raised or expenditures don't rise."
assert kb.prove() == True

# You can also visualize the proof construction!
proof = kb.prove(return_proof=True)
proof.find()

from pprint import pprint
pprint(proof.steps)

# Uncomment this if you have graphziv installed 
#proof.visualize()
