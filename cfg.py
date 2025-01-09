from assets import *
CFG_FILE_PATH = "cfg.txt"
CFG_RULES_STR = ""
with open(CFG_FILE_PATH, "r") as file:
    CFG_RULES_STR = file.read()


class Symbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, Symbol) else False

    def __repr__(self):
        return f"Sym({self.name})"

    def __hash__(self):
        return self.name.__hash__()


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
        for rule in self.rules:
            if all(["" == x for x in rule.rest]):
                rule.rest = [""]
            else:
                while "" in rule.rest:
                    rule.rest.remove("")
        # self._first_cache = {x: False for x in self.symbols}
        self._first_values = {x: set() for x in self.symbols}

    def calculate_firsts(self):
        keep_calculating = True
        while keep_calculating:
            keep_calculating = False
            for rule in self.rules:
                # i = 0
                # while i < len(rule.rest):
                for f in rule.rest:
                    # f = rule.rest[i]
                    # print(self._first_values[Symbol("number")])
                    if isinstance(f, str):
                        if f not in self._first_values[rule.origin]:
                            self._first_values[rule.origin].add(f)
                            keep_calculating = True
                        break
                    else:
                        if not self._first_values[f]:
                            break
                        no_epsilon = True
                        for x in self._first_values[f]:
                            if x == "":
                                no_epsilon = False
                                # if i != len(rule.rest):
                                if f != rule.rest[-1]:
                                    continue
                            if x not in self._first_values[rule.origin]:
                                self._first_values[rule.origin].add(x)
                                keep_calculating = True
                        if no_epsilon:
                            break
                        # i += 1

    # def calculate_follows(self):
    #     keep_calculating = True
    #     while keep_calculating:
    #         keep_calculating = False
    #         for rule in self.rules:
    #             for i in range(len(rule.rest)):
    #                 f = rule.rest[i]
                    

    def first(self, symbol):
        return self._first_values[symbol]

    def __repr__(self):
        return "\n".join([str(x) for x in self.rules])


# c = CFG(CFG_RULES_STR)
# print(c)
# c = CFG("""e: t e'
# e': "+" t e' | 
# t: f t'
# t': "*" f t' | 
# f: "(" e ")" | "id"
# """)
# c.calculate_firsts()
# print(c._first_values)
