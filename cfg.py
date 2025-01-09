from assets import *
CFG_FILE_PATH = "cfg.txt"
CFG_RULES_STR = ""
with open(CFG_FILE_PATH, "r") as file:
    CFG_RULES_STR = file.read()

class Symbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Sym({self.name})"


class Rule:
    def __init__(self, origin, rest):
        self.origin = origin
        self.rest = rest

    def __eq__(self, other):
        return self.origin == other.origin and self.rest == other.rest

    def __repr__(self):
        return f"{self.origin} -> {" ".join([str(x) if isinstance(x, Symbol) else x for x in self.rest])}"


class CFG:
    def __init__(self, grammar_str: str):
        self.symbols = []
        symbol_names = set()
        self.rules = []

        def check_symbol(symbol):
            if symbol not in symbol_names:
                symbol_names.add(symbol)
                self.symbols.append(Symbol(symbol))
                return False
            return True

        for line in grammar_str.splitlines():
            symbol, rest = line.split(": ")
            check_symbol(symbol)

            rests = rest.split("|")
            for rest in rests:
                rule = Rule(Symbol(symbol), [])
                words = rest.split(" ")
                i = 0
                while i != len(words):
                    current = words[i]
                    if current.startswith('"'):
                        j = i
                        while not words[j].endswith('"'):
                            j += 1
                        rule.rest.append(" ".join(words[i:j + 1])[1:-1])
                        i = j + 1
                    else:
                        if current == "":
                            rule.rest.append("")
                        else:
                            check_symbol(current)
                            rule.rest.append(Symbol(current))
                        i += 1
                self.rules.append(rule)

    def __repr__(self):
        return "\n".join([str(x) for x in self.rules])
