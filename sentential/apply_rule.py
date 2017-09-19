def apply_rule(expr, rule):
    try:
        found_node, found_parent_node, found_parent_rel = find_matching_node(expr, rule)
    except:
        found_node = find_matching_node(expr, rule)

    if found_parent_node is None:
        return rewrite_rule(found_node)
    else:
        set_attr(found_parent_node, found_parent_rel, rewrite_rule(found_node))
        return apply_rule(expr, rule)

    if not found_node:
        return expr
