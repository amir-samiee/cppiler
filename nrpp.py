from assets import Token_names
from cfg import CFG, Symbol, Rule


def is_symbol_terminal(token):
    return token[0] in [Token_names.reservedword.name, Token_names.symbol.name]


def nonrecursive_predictive_parser(tokens: list, cfg: CFG):
    res = []
    it = iter(tokens)
    n = next(it)
    ist = is_symbol_terminal(n)
    token_value = n[ist]
    stack = [Symbol("start")]
    while stack:
        top = stack.pop()
        if top == "":
            continue
        if top == token_value:
            if not ist:
                res.append((Rule(n[0], [n[1]]), n[2]))
            try:
                n = next(it)
                ist = is_symbol_terminal(n)
                token_value = n[ist]
            except StopIteration:
                break

        elif top in cfg.terminals:
            if top == ";":
                raise SyntaxError(f"Error: Missing ';' at line {n[2]-1}.")
            raise SyntaxError(f"Error: Unexpected token '{token_value}' at line {n[2]}, column {n[3]}.")

        elif not cfg.parse_table.get(top).get(token_value):
            if cfg.parse_table[top][";"]:
                raise SyntaxError(f"Error: Missing ';' at line {n[2]-1}.")
            elif top == Symbol("operation"):
                if token_value not in ["number", "identifier"]:
                    raise SyntaxError(
                        f"Error: Invalid assignment value '{token_value}' at line {n[2]}, column {n[3]}."
                    )
            raise SyntaxError(f"Error: Unexpected token '{token_value}' at line {n[2]}, column {n[3]}.")

        else:
            rule = cfg.parse_table[top][token_value][0]
            res.append((rule, n[2]))
            stack.extend(rule.rest[::-1])

    return res

