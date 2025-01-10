from rich import print
from sympy import symbols
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
        self.terminals = []
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
                        result = " ".join(words[i:j + 1])[1:-1]
                        self.terminals.append(result)
                        rule.rest.append(result)
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
        self._first_values = {x: set() for x in self.symbols}
        self._follow_values = {x: set() for x in self.symbols}

        self._m = None
        self._calculate_firsts()
        self._calculate_follows()
        self._create_parse_table()

    def _calculate_firsts(self):
        keep_calculating = True
        while keep_calculating:
            keep_calculating = False
            for rule in self.rules:
                for f in rule.rest:
                    if isinstance(f, str):
                        # if f not in self._first_values[rule.origin]:
                        #     self._first_values[rule.origin].add(f)
                        #     keep_calculating = True
                        keep_calculating = keep_calculating or add_if_not_already_added(
                            f, self._first_values[rule.origin])
                        break
                    else:
                        if not self._first_values[f]:
                            break
                        no_epsilon = True
                        for x in self._first_values[f]:
                            if x == "":
                                no_epsilon = False
                                if f != rule.rest[-1]:
                                    continue
                            # if x not in self._first_values[rule.origin]:
                            #     self._first_values[rule.origin].add(x)
                            #     keep_calculating = True
                            keep_calculating = keep_calculating or add_if_not_already_added(
                                x, self._first_values[rule.origin])
                        if no_epsilon:
                            break

    def _calculate_follows(self):
        self._follow_values[Symbol("start")].add("$")
        keep_calculating = True
        while keep_calculating:
            keep_calculating = False
            for rule in self.rules:
                has_epsilon = ["" in self.first(x) if isinstance(
                    x, Symbol) else False for x in rule.rest]
                for i in range(len(rule.rest)):
                    f = rule.rest[i]
                    if isinstance(f, str):
                        continue
                    do = True
                    while i + 1 < len(rule.rest) and (do or has_epsilon[i + 1]):
                        do = False
                        i += 1
                        g = rule.rest[i]
                        if isinstance(g, str):
                            keep_calculating = keep_calculating or add_if_not_already_added(
                                g, self._follow_values[f])
                        else:
                            for x in self.first(g) - {""}:
                                keep_calculating = keep_calculating or add_if_not_already_added(
                                    x, self._follow_values[f])
                i = len(rule.rest) - 1
                do = True
                while i >= 0 and (do or has_epsilon[i + 1]):
                    f = rule.rest[i]
                    if isinstance(f, str):
                        break
                    for x in self._follow_values[rule.origin] - {""}:
                        keep_calculating = keep_calculating or add_if_not_already_added(
                            x, self._follow_values[f])
                    i -= 1

    def first(self, symbol):
        return self._first_values[symbol]

    def follow(self, symbol):
        return self._follow_values[symbol]

    def _create_parse_table(self):
        # rows = len(self.symbols)
        # columns = len(self.terminals) + 1  # $
        # M = [[[] for j in range(columns)] for i in range(rows)]
        M = {s: {t: [] for t in self.terminals + ["$"]} for s in self.symbols}
        for rule in self.rules:
            fa = set()  # First(A)
            f1 = rule.rest[0]
            if isinstance(f1,str):
                fa.add(f1)
            else:
                for i in range(len(rule.rest)):
                    f = rule.rest[i]
                    if isinstance(f, str):
                        # if not f:
                        #     fa.add(f)
                        break
                    fa |= self.first(f)
                    if "" not in self.first(f):
                        break
            ein = "" in fa
            if ein:
                fa.remove("")
            print(rule, fa, "==========")
            for t in fa:
                M[rule.origin][t].append(rule)
            if ein:
                for t in self.follow(rule.origin):
                    M[rule.origin][t].append(rule)
                if "$" in self.follow(rule.origin):
                    M[rule.origin]["$"].append(rule)
        self._m = M

    @property
    def parse_table(self):
        return self._m

    def __repr__(self):
        return "\n".join([str(x) for x in self.rules])


# c = CFG(CFG_RULES_STR)
# print(c)
# c = CFG("""start: t e'
# e': "+" t e' |
# t: f t'
# t': "*" f t' |
# f: "(" start ")" | "id"
# """)
# c.calculate_firsts()
# c.calculate_follows()
# print(c._first_values)
# print(c._follow_values)
# print(c.terminals)
# print(c.parse_table[Symbol("t")])
# print(c.parse_table)
