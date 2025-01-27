from tabulate import tabulate
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
        return isinstance(other, Rule) and self.origin == other.origin and self.rest == other.rest

    def __repr__(self):
        return f"{self.origin} -> {" ".join([str(x) if isinstance(x, Symbol) else x for x in self.rest])}"


class CFG:
    # Time Complexity: O(r × w + v × t)
    # - r: Number of rules in the grammar
    # - w: Average number of words per rule
    # - v: Number of unique non-terminal symbols
    # - t: Number of terminal symbols
    def __init__(self, grammar_str: str):
        self.symbols = []
        self.terminals = []
        symbol_names = set()
        self.rules = []

        def check_symbol(symbol):  # O(1)
            if symbol not in symbol_names:
                symbol_names.add(symbol)
                self.symbols.append(Symbol(symbol))
                return False
            return True

        # Parse grammar rules
        for line in grammar_str.splitlines():  # O(r × w)
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

        # Process rules for empty strings
        for rule in self.rules:  # O(r × w)
            if not any(rule.rest):
                rule.rest = [""]
            else:
                rule.rest = [x for x in rule.rest if x != ""]

        self._first_values = {x: set() for x in self.symbols}  # O(v)
        self._follow_values = {x: set() for x in self.symbols}  # O(v)

        self._m = None
        self._calculate_firsts()
        self._calculate_follows()
        self._create_parse_table()

    # Time Complexity: O(r × w × v × t^2)
    def _calculate_firsts(self):
        keep_calculating = True
        while keep_calculating:
            keep_calculating = False
            for rule in self.rules:  # O(r)
                for f in rule.rest:  # O(w)
                    if isinstance(f, str):
                        keep_calculating = keep_calculating or add_if_not_already_added(
                            f, self._first_values[rule.origin])
                        break
                    else:
                        if not self._first_values[f]:
                            break
                        no_epsilon = True
                        for x in self._first_values[f]:  # O(v)
                            if x == "":
                                no_epsilon = False
                                continue
                            keep_calculating = keep_calculating or add_if_not_already_added(
                                x, self._first_values[rule.origin])
                        if no_epsilon:
                            break
                else:
                    add_if_not_already_added(
                        "", self._first_values[rule.origin])

    # Time Complexity: O(r × w × v)
    def _calculate_follows(self):
        self._follow_values[Symbol("start")].add("$")
        keep_calculating = True
        while keep_calculating:
            keep_calculating = False
            for rule in self.rules:  # O(r)
                for i in range(len(rule.rest)):  # O(w)
                    f = rule.rest[i]
                    if isinstance(f, str):
                        continue
                    ff = self.first(
                        rule.rest[i+1:]) if i != len(rule.rest) - 1 else {""}
                    for x in ff - {""}:  # O(v)
                        keep_calculating = keep_calculating or add_if_not_already_added(
                            x, self._follow_values[f])
                    if "" in ff:
                        for x in self._follow_values[rule.origin]:  # O(v)
                            keep_calculating = keep_calculating or add_if_not_already_added(
                                x, self._follow_values[f])

    # Time Complexity: O(v × t)
    def _create_parse_table(self):
        M = {s: {t: None for t in self.terminals +
                 ["$"]} for s in self.symbols}  # O(v × t)
        for rule in self.rules:  # O(r)
            fa = self.first(rule.rest)  # O(w × t)
            ein = "" in fa
            if ein:
                fa.remove("")
            for t in fa:  # O(t)
                M[rule.origin][t] = rule
            if ein:
                for t in self.follow(rule.origin):  # O(v)
                    M[rule.origin][t] = rule
                if "$" in self.follow(rule.origin):
                    M[rule.origin]["$"] = rule
        self._m = M

    # Time Complexity: O(w × v)
    def first(self, symbols):
        if isinstance(symbols, Symbol):
            return self._first_values[symbols]
        fs = set()
        f1 = symbols[0]
        if isinstance(f1, str):
            fs.add(f1)
        else:
            for i in range(len(symbols)):  # O(w)
                f = symbols[i]
                if isinstance(f, str):
                    break
                fs |= self.first(f)  # O(v)
                if "" not in self.first(f):
                    break
                fs.remove("")
            else:
                fs.add("")
        return fs

    # Time Complexity: O(1)
    def follow(self, symbol):
        return self._follow_values[symbol]

    @property
    def parse_table(self):
        return self._m

    # Time Complexity: O(v × t)
    def save_parse_table(self):
        data = self.parse_table
        headers = data[Symbol("start")].keys()
        rows = []
        for symbol in data.keys():  # O(v)
            rows.append([symbol] + [data[symbol][header]
                                    for header in headers])  # O(t)
        with open("parse_table.txt", "w") as file:  # O(v × t)
            file.write(
                str(tabulate(rows, headers=headers, tablefmt="grid")) + "\n")

    def __repr__(self):
        return "\n".join([str(x) for x in self.rules])  # O(r)
