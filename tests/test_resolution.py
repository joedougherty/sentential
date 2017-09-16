from sentential.Proof import resolve, would_resolve, resolution_result

def test_tautologies_dont_resolve_with_themselves():
    c1, c2 = frozenset({'p', '~p'}), frozenset({'~p', 'p'})
    assert would_resolve(c1, c2) == False
