from assets import Token_names as tk
from cfg import Symbol
from anytree import Node
from collections import deque

class ParseTree:
    def __init__(self, production_sequence: list):
        root = Node(Symbol("start"))
        stack = [root]
        i = 0
        while stack:
            x = stack.pop()
            psr = [Node(y, parent=x) if y != "" else Node("epsilon", parent=x)
                   for y in production_sequence[i].rest]
            for t in psr[::-1]:
                if isinstance(t.name, Symbol) or t.name in [tk.identifier.name, tk.number.name, tk.string.name]:
                    stack.append(t)
            i += 1
        self.root = root
    
    def BFS(self, target_name):
        queue= deque([self.root])
        while queue:
            node = queue.popleft()
            if node.name == target_name:
                return node
            queue.extend(node.children)
        return None

    def validate_type_mismatches(self):
        symbol_table = {}
        errors = []

        queue = deque([self.root])

        while queue:
            node = queue.popleft()

            if node.name == Symbol("id"):
                declared_type = None
                variable_name = None

                for child in node.children:
                    if child.name in ["int", "float"]:
                        declared_type = child.name
                    elif child.name == Symbol("l"):
                        for l_child in child.children:
                            if l_child.name == "identifier":
                                variable_name = l_child.children[0].name

                if declared_type and variable_name:
                    symbol_table[variable_name] = declared_type

            if node.name == Symbol("assign"):
                variable_name = None
                assigned_type = None

                parent = node.parent
                if parent and parent.name == Symbol("l"):
                    for sibling in parent.children:
                        if sibling.name == "identifier":
                            variable_name = sibling.children[0].name

                for assign_child in node.children:
                    if assign_child.name == Symbol("operation"):
                        for operation_child in assign_child.children:
                            if operation_child.name == "number":
                                assigned_type = "float" if "." in operation_child.children[0].name else "int"
                            elif operation_child.name == "identifier":
                                assigned_type = symbol_table.get(operation_child.children[0].name, None)

                if variable_name in symbol_table:
                    declared_type = symbol_table[variable_name]
                    if assigned_type and declared_type != assigned_type:
                        errors.append(
                            f"Error: Type mismatch in assignment to '{variable_name}': Cannot assign '{assigned_type}' to '{declared_type}'."
                        )
                else:
                    errors.append(f"Error: Undeclared variable '{variable_name}' used in assignment.")

            queue.extend(node.children)

        return errors

