from deepcopy import copy

from sentential import Proposition

class KnowledgeBase:
    def __init__(self):
        self.axioms = []

    def add(self, axiom):
        if isinstance(axiom, Proposition):
            for clauses in axiom.cnf():
                self.axioms.append(clauses)
        else:   
            raise TypeError('You may add only Propositions to the Knowledge Base!')

    def _negated_term(self, term):
        if term.startswith('~'):
            return term.replace('~', '')
        else:
            return '~{}'.format(term)

    def resolve(self):
        for current_axiom in self.axioms:
            for term in current_axiom:
                remaining_axioms = [a for a in self.axioms if a != current_axiom]
                for axiom in remaining_axioms:
                    if self._negated_term(term) in axiom:
                        result = copy(current_axiom)
                        result.remove(term)
                        if len(result) > 0:
                            return result
                        else:
                            result = copy(axiom)
                            result.remove(self._negated_term(term))
                            return result
