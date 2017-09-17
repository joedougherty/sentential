import pytest

from sentential.Proof import resolve, would_resolve, resolution_result

def test_tautologies_dont_resolve_with_themselves():
    c1, c2 = frozenset({'p', '~p'}), frozenset({'~p', 'p'})
    assert would_resolve(c1, c2) == False

''' http://intrologic.stanford.edu/exercises/exercise_05_02.html '''
def test_prob_1():
    assert resolve({'p', 'q', '~r'}, {'r', 's'}) == resolution_result(clause=frozenset({'s', 'q', 'p'}), resolved_by='~r')

def test_prob_2_b():
    assert would_resolve({'p', 'q', 'r'}, {'r', '~s', '~t'}) == False

def test_prob_2_a():
    with pytest.raises(Exception):
        resolve({'p', 'q', 'r'}, {'r', '~s', '~t'})

def test_prob_3():
    # This technically produces itself as a resolvent (i.e. {'q', '~q'})
    # I don't bother to resolve these since it can't possibly add any
    # new information to the clause collection.
    assert would_resolve({'q', '~q'}, {'q', '~q'}) == False

def test_prob_4():
    # Find all possible resolvents for c1, c2 where:
    #   c1 = {'q', 'r', '~p'}
    #   c2 = {'p', '~q', '~r'}
    c1, c2 = {'q', 'r', '~p'}, {'p', '~q', '~r'}
    resolution_possibilities = [resolve(c1, c2, resolve_by=literal) for literal in would_resolve(c1, c2)]
    
    generated_possibilities = [resolution_result(clause=frozenset({'~q', 'q', 'p', '~p'}), resolved_by='r'),
                               resolution_result(clause=frozenset({'r', '~r', 'p', '~p'}), resolved_by='q'),
                               resolution_result(clause=frozenset({'r', '~q', 'q', '~r'}), resolved_by='~p')]
    # Order should not matter, so run set!
    assert set(resolution_possibilities) == set(generated_possibilities)
