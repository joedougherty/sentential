from sentential.ExprNode import ExprNode, token, treeify, listify_ExprNode

simple_clause = [token('TERM', 'p'), token('BINOP', 'v'), token('TERM', 'q')]
simple_clause = [token('TERM', 'p'), token('BINOP', 'v'), token('TERM', 'q')]

simple_ast = simple_clause

complex_ast = [token('TERM', 'p'), token('BINOP', 'v'), simple_clause]
equivalence_of_simple_clauses = [simple_clause, token('BINOP', '='), simple_clause]

slightly_more_complex_ast = [complex_ast, token('BINOP', '->'), simple_clause]

def test_simple_ast_conversion_to_tree_and_back():
    assert simple_ast == listify_ExprNode(treeify(simple_ast))

def test_complex_ast_conversion_to_tree_and_back():
    assert complex_ast == listify_ExprNode(treeify(complex_ast))

def test_ast_composed_of_smaller_asts():
    assert equivalence_of_simple_clauses == listify_ExprNode(treeify(equivalence_of_simple_clauses))

def test_slightly_more_complex_ast():
    assert slightly_more_complex_ast == listify_ExprNode(treeify(slightly_more_complex_ast))
