from sentential.ExprNode import ExprNode, token, treeify, listify_ExprNode

simple_ast = [token('TERM', 'p'), token('BINOP', 'v'), token('TERM', 'q')]
complex_ast = [token('TERM', 'p'), token('BINOP', 'v'), [token('TERM', 'q'), token('BINOP', '&'), token('TERM', '~r')]]

def test_simple_ast_conversion_to_tree_and_back():
    assert simple_ast == listify_ExprNode(treeify(simple_ast))

def test_complex_ast_conversion_to_tree_and_back():
    assert complex_ast == listify_ExprNode(treeify(complex_ast))
