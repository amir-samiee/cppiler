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

    def extract_identifiers_and_values(self, l_node:Node):
        res = []
        def single_var(mynode:Node):
            key = None
            value = None
            line = None
            for child in mynode.children:
                if child.name == "identifier":
                    key = child.children[0].name
                    line = child.children[0].line
                elif child.name == Symbol("assign"):
                    if child.children[0].name == "epsilon": 
                        return key, None, line
                    op_node = child.children[1]
                    value = op_node.children[0].children[0].name
                    p_node = op_node.children[1]
                    while p_node.children[0].name == Symbol("o"):
                        op = p_node.children[0].children[0].name
                        tmp_value = p_node.children[1].children[0].children[0].name
                        value += " " + op + " " + tmp_value
                        p_node = p_node.children[2]
            return key, value, line
        
        node = l_node
        while node.children[0].name != ";":
            key, value, line = single_var(node)
            res.append((key, value, line))
            node = node.children[-1]
        return res


    def dfs_traversal(self):
        declared_variables = []
        values = defaultdict(list)
        stack = [self.root]

        while stack:
            top = stack.pop()

            if top.name == Symbol("id"):
                data_type = top.children[0].name
                key_value_lines = self.extract_identifiers_and_values(top.children[1])
                for key, value, line in key_value_lines:
                    declared_variables.append(key)
                    values[key].append((data_type, value, line))

            elif top.name == Symbol("l"):
                key_value_lines = self.extract_identifiers_and_values(top)
                for key, value, line in key_value_lines:
                    if key in values:
                        data_type = values[key][0][0]
                        if (data_type, value, line) not in values[key]:
                            values[key].append((data_type, value, line))

            for child in reversed(top.children):
                stack.append(child)

        return declared_variables, values


    
    def first_definition(self, identifier):
        if not identifier:
            return identifier
        data_type, value = self.values[identifier][0]
        defenition = data_type + " " + identifier
        if value:
            defenition += " = " + value
        return defenition + ";"

    def find_misstype(self):
        errors = []
            
        def evaluate_expression(exp:str):
            values = list(filter(lambda x: x not in "+-*" , exp.split()))
            vars = list(filter(lambda x: not x.isdigit() and not '.' in x, values))
            data_type = "int"
            for var in vars:
                tmp = self.values.get(var)
                if tmp == None:
                    errors.append((
                        f"not declared", tmp[2])
                    )
                    return None
                if tmp[0][0] == "float":
                    data_type = "float"
            not_vars = list(filter(lambda x: x not in vars, values))
            for element in not_vars:
                if '.' in element:
                    return "float"
            return data_type
                
        for key in self.values:
            for assignment in self.values[key]:
                declared_type = assignment[0]
                assigned_type = declared_type
                if assignment[1]:
                    assigned_type = evaluate_expression(assignment[1])
                if declared_type != assigned_type:
                    errors.append((
                        f"- Error: Cannot assign '{assigned_type}' to '{declared_type}' variable '{key}' at line {assignment[2]}.", assignment[2])
                    )
        return sorted(errors, key = lambda x: int(x[1]))