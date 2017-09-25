from copy import copy
import string

from graphviz import Digraph


def stringify_clause(c):
    if c == set() or c == frozenset():
        return '{}'
    return str(set(c)).replace("'", '').replace('"', '')


class ProofGraph:
    def __init__(self, steps):
        self.steps = steps
        self._steps_shadow = copy(self.steps)
        self._steps_shadow.reverse()
        self.reverse_steps = self._steps_shadow
        self.nodes, self.edge_pairs = list(), list()

        potential_node_names = list()
        for letter in string.ascii_lowercase:
            for num in range(0, 10):
                potential_node_names.append('{}{}'.format(letter, num))

        self.node_names = (x for x in potential_node_names)

    def _get_resolvent_node_id(self, resolvent):
        for n in self.nodes:
            if n.get('rep') == stringify_clause(resolvent):
                return n.get('name')

    def mint_new_nodes(self, step, mint_resolvent=False, current_clause=None):
        gen_node_names = list()

        if mint_resolvent:
            relevant_clauses = (step.c1, step.c2, step.resolvent)
        else:
            relevant_clauses = (step.c1, step.c2)

        for c in relevant_clauses:
            nn = next(self.node_names)
            gen_node_names.append(nn)
            self.nodes.append({'name': nn, 'rep': stringify_clause(c)})

        if current_clause is None:
            target_node = gen_node_names[2]
        else:
            target_node = current_clause

        self.edge_pairs.append((gen_node_names[0], target_node))
        self.edge_pairs.append((gen_node_names[1], target_node))

    def find_parents(self, s):
        for clause in (s.c1, s.c2):
            for step in self.reverse_steps:
                if step.resolvent == clause:
                    self.mint_new_nodes(step,
                                        mint_resolvent=False,
                                        current_clause=self._get_resolvent_node_id(clause))
                    self.find_parents(step)

    def generate(self):
        current_step = self.reverse_steps.pop(0)
        self.mint_new_nodes(current_step, mint_resolvent=True)
        self.find_parents(current_step)

        dot = Digraph()

        [dot.node(node['name'], node['rep']) for node in self.nodes]
        [dot.edge(e[0], e[1]) for e in self.edge_pairs]

        return dot
