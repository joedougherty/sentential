# Character classes
OPENPAREN := (
CLOSEPAREN := )
VAR := a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | w | x | y | z
NEG := ~ | ! | ¬
BINOP := v | ^ | & | and | or | iff | = | <-> | ->
SPACE := " "

# Possible combinations
TERM := NEG* VAR
OPERAND := TERM | EXPR
EXPR := NEG* OPENPAREN OPERAND SPACE BINOP SPACE OPERAND CLOSEPAREN
