from assets import Token_names as tk
from cfg import Symbol
from anytree import Node


def parse_tree(production_sequence: list):
    start = Node(Symbol("start"))
    stack = [start]
    i = 0
    while stack:
        x = stack.pop()
        psr = [Node(y, parent=x) if y != "" else Node("epsilon", parent=x)
               for y in production_sequence[i].rest]
        for t in psr[::-1]:
            if isinstance(t.name, Symbol) or t.name in [tk.identifier.name, tk.number.name, tk.string.name]:
                stack.append(t)
        i += 1
    return start
