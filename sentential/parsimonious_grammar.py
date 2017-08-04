# -*- coding: utf-8 -*-

from parsimonious.grammar import Grammar
try:
    from string import lowercase
except:
    from string import ascii_lowercase as lowercase


def vars_expr():
    """ Generate a string to match all vars like:
            "a" / "b" / "c" / "d" (etc.)
    """
    return_str = ''
    for letter in lowercase.replace('v', ''):
        return_str += '"{}" / '.format(letter)
    return return_str[:-3]


g = Grammar(
	"""
	EXPR = NEG* OPENPAREN OPERAND SPACE BINOP SPACE OPERAND CLOSEPAREN

        # Character Classes
	SPACE = " "
	NEG = "~" / "!" / "¬"
	OPENPAREN = "("
	VAR = {}
	CLOSEPAREN = ")"
	BINOP = "v" / "&" / "=" / "<->" / "->" / "or"
	
        # Character Class Combinations
	OPERAND = TERM / EXPR
        TERM = NEG* VAR
	""".format(vars_expr()))

g.parse('''!(p & q)''')
g.parse('''!(p v (r -> s))''')
g.parse('''((p v w) <-> !e)''')
g.parse('''((p v !w) & (l <-> x))''')
g.parse('''(p <-> ~(!q -> (r v s)))''')
g.parse('''(p or ~(!q -> (r v s)))''')
g.parse('''!¬(p v ~!~q)''')
