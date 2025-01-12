from assets import Token_names
from cfg import CFG, Symbol


def representing_value(token):
    if Token_names[token[0]] in [Token_names.reservedword, Token_names.symbol]:
        return token[1]
    return token[0]


def nonrecursive_predictive_parser(tokens: list, cfg: CFG):
    res = []
    it = iter(tokens)
    a = representing_value(next(it))
    stack = [Symbol("start")]
    while stack:
        x = stack.pop()
        if x == "":
            continue
        if x == a:
            try:
                a = representing_value(next(it))
            except StopIteration:
                pass
        elif x in cfg.terminals:
            raise Exception("error type 1")
        elif not cfg.parse_table[x][a]:
            raise Exception("error type 2")
        else:
            rule = cfg.parse_table[x][a][0]
            res.append(rule)
            stack.extend(rule.rest[::-1])
    return res
