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
                res.append(Rule(n[0], [n[1]]))
            try:
                n = next(it)
                ist = is_symbol_terminal(n)
                token_value = n[ist]
            except StopIteration:
                break
        elif top in cfg.terminals:
            raise Exception("error type 1")
        elif not cfg.parse_table[top][token_value]:
            raise Exception("error type 2")
        else:
            rule = cfg.parse_table[top][token_value][0]
            res.append(rule)
            stack.extend(rule.rest[::-1])
    return res
