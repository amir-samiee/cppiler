from assets import Token_names
from cfg import CFG, Symbol, Rule


# Time Complexity: O(1)
# This function checks if a token is a terminal symbol.
def is_symbol_terminal(token):
    return token[0] in [Token_names.reservedword.name, Token_names.symbol.name]


# Time Complexity: O(m × (d + r × w))
# where:
# - m is the number of tokens in the input.
# - d is the average number of entries checked in the parse table for a token.
# - r is the average number of rules per non-terminal.
# - w is the average number of symbols on the right-hand side of a rule.
def nonrecursive_predictive_parser(tokens: list, cfg: CFG):
    res = []
    it = iter(tokens)  # O(1)
    n = next(it)  # O(1)
    ist = is_symbol_terminal(n)  # O(1)
    token_value = n[ist]  # O(1)
    stack = [Symbol("start")]  # O(1)

    while stack:  # Outer loop runs O(m) times (once per token).
        top = stack.pop()  # O(1)

        if top == "":
            continue

        # Case 1: Terminal matches the current token value.
        if top == token_value:
            if not ist:
                res.append((Rule(n[0], [n[1]]), n[2]))  # O(1)
            try:
                n = next(it)  # O(1)
                ist = is_symbol_terminal(n)  # O(1)
                token_value = n[ist]  # O(1)
            except StopIteration:
                break

        # Case 2: `top` is a terminal, but it doesn't match the token value.
        elif top in cfg.terminals:  # O(d), where d is the number of terminals in `cfg`.
            if top == ";":
                raise SyntaxError(f"Error: Missing ';' at line {n[2]-1}.")
            raise SyntaxError(f"Error: Unexpected token '{token_value}' at line {n[2]}, column {n[3]}.")

        # Case 3: `top` is a non-terminal but no matching rule is found in the parse table.
        elif not cfg.parse_table.get(top).get(token_value):  # O(d)
            if cfg.parse_table[top][";"]:
                raise SyntaxError(f"Error: Missing ';' at line {n[2]-1}.")
            elif top == Symbol("operation"):
                if token_value not in ["number", "identifier"]:
                    raise SyntaxError(
                        f"Error: Invalid assignment value '{token_value}' at line {n[2]}, column {n[3]}."
                    )
            raise SyntaxError(f"Error: Unexpected token '{token_value}' at line {n[2]}, column {n[3]}.")

        # Case 4: Valid rule is found for the non-terminal.
        else:
            rule = cfg.parse_table[top][token_value]  # O(d)
            res.append((rule, n[2]))  # O(1)
            stack.extend(rule.rest[::-1])  # O(w), where `w` is the length of `rule.rest`.

    return res  # O(1)
