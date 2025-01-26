from assets import Token_names as tk
from cfg import Symbol
from anytree import Node
from collections import defaultdict

class ParseTree:
    def __init__(self, production_sequence: list):
        root = Node(Symbol("start"), line=1)
        stack = [root]
        i = 0
        while stack:
            x = stack.pop()
            rule, line = production_sequence[i]
            psr = [Node(y, parent=x, line=line) if y != "" else Node("epsilon", parent=x, line=line)
                   for y in rule.rest]
            for t in psr[::-1]:
                if isinstance(t.name, Symbol) or t.name in [tk.identifier.name, tk.number.name, tk.string.name]:
                    stack.append(t)
            i += 1
        self.root = root
        self.variables, self.values = self.dfs_traversal()

    def extract_identifiers_and_values(self, node):
        results = []

        def traverse_L(current_node):
            if not current_node:
                return

            identifier = None
            value = None

            for child in current_node.children:
                if child.name == "identifier":
                    identifier = child.children[0].name
                elif child.name == Symbol("assign"):
                    if len(child.children) == 1:
                        value = None
                    else:
                        for assign_child in child.children:
                            if assign_child.name == Symbol("operation"):
                                for operation_child in assign_child.children:
                                    if operation_child.name == "number":
                                        value = operation_child.children[0].name
                                    elif operation_child.name == "identifier":
                                        value = operation_child.children[0].name

            if identifier:
                results.append((identifier, value if value else None))

            for child in current_node.children:
                if child.name == Symbol("z"):
                    traverse_L(child)

        traverse_L(node)
        return results


    def dfs_traversal(self):
        variables = []
        values = defaultdict(list)
        stack = [self.root]

        while stack:
            top = stack.pop()
            if top.name == Symbol("id"):
                data_type = top.children[0].name
                key_values = self.extract_identifiers_and_values(top.children[1])
                for key, value in key_values:
                    variables.append(key)
                    values[key].append((data_type, value))
            for child in reversed(top.children):
                stack.append(child)
        return variables, values
    
    def first_definition(self, identifier):
        if not identifier:
            return identifier
        data_type, value = self.values[identifier][0]
        defenition = data_type + " " + identifier
        if value:
            defenition += " = " + value
        return defenition + ";"
    
    def find_misstype(self):
        pass