from operator import not_

from sentential.evaluator import resolve_term_negation


class ExprNode:
    """
    Model a sentential logic subexpression.

    (p v ~p) => ExprNode([<truth val of p>], [not_, <truth val of p>], or_) 
    (p v (q & r)) => ExprNode([<truth val of p>], ExprNode([<truth val of q>], [<truth val of r>], and_), or_)
    """
    def __init__(self, left, right, bin_op):
        self.raw_left = left
        self.raw_right = right
        self.bin_op = bin_op
        self.truth_value = None
        
    def resolve_term(self, term):
        if term[0] == not_:
            return resolve_term_negation(term)
        return term[0]

    def eval(self):
        if isinstance(self.raw_left, ExprNode):
            self.raw_left.eval()
        if isinstance(self.raw_right, ExprNode):
            self.raw_right.eval()
        return bin_op(resolve_term(raw_left), resolve_term(raw_right))
