from assets import Token_names
from cfg import CFG, Symbol, Rule


def is_symbol_terminal(token):
    return token[0] in [Token_names.reservedword.name, Token_names.symbol.name]


def nonrecursive_predictive_parser(tokens: list, cfg: CFG):
    res = []
    it = iter(tokens)
    n = next(it)
    ist = is_symbol_terminal(n)
    a = n[ist]
    stack = [Symbol("start")]
    while stack:
        x = stack.pop()
        if x == "":
            continue
        if x == a:
            if not ist:
                res.append(Rule(n[0], [n[1]]))
            try:
                n = next(it)
                ist = is_symbol_terminal(n)
                a = n[ist]
            except StopIteration:
                break
        elif x in cfg.terminals:
            raise Exception("error type 1")
        elif not cfg.parse_table[x][a]:
            raise Exception("error type 2")
        else:
            rule = cfg.parse_table[x][a][0]
            res.append(rule)
            stack.extend(rule.rest[::-1])
    return res
