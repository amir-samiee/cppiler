from assets import Token_names as tk
from cfg import Symbol
from anytree import Node
from collections import defaultdict

class ParseTree:
    # Time Complexity: O(p × r × w),
    # where:
    # - p is the number of productions in `production_sequence`.
    # - r is the average number of symbols on the right-hand side of a rule.
    # - w is the average number of children per node in the parse tree.
    def __init__(self, production_sequence: list):
        root = Node(Symbol("start"), line=1)
        stack = [root]
        i = 0
        while stack:  # O(p)
            x = stack.pop()
            rule, line = production_sequence[i]
            psr = [Node(y, parent=x, line=line) if y != "" else Node("epsilon", parent=x, line=line)
                   for y in rule.rest]  # O(r)
            for t in psr[::-1]:  # O(r)
                if isinstance(t.name, Symbol) or t.name in [tk.identifier.name, tk.number.name, tk.string.name]:
                    stack.append(t)
            i += 1
        self.root = root
        self.variables, self.values = self.dfs_traversal()

    # Time Complexity: O(v × o),
    # where:
    # - v is the number of variables in a single `l_node` subtree.
    # - o is the number of operations in the `operation` subtree.
    def extract_identifiers_and_values(self, l_node: Node):
        res = []

        def single_var(mynode: Node):  # O(o)
            key = None
            value = None
            line = None
            for child in mynode.children:  # O(w), where w is the number of children in the node.
                if child.name == "identifier":
                    key = child.children[0].name
                    line = child.children[0].line
                elif child.name == Symbol("assign"):
                    if child.children[0].name == "epsilon": 
                        return key, None, line
                    op_node = child.children[1]
                    value = op_node.children[0].children[0].name
                    p_node = op_node.children[1]
                    while p_node.children[0].name == Symbol("o"):  # O(o), processing `P` nodes.
                        op = p_node.children[0].children[0].name
                        tmp_value = p_node.children[1].children[0].children[0].name
                        value += " " + op + " " + tmp_value
                        p_node = p_node.children[2]
            return key, value, line

        node = l_node
        while node.children[0].name != ";":  # O(v)
            key, value, line = single_var(node)  # O(o)
            res.append((key, value, line))
            node = node.children[-1]
        return res

    # Time Complexity: O(n × v × o),
    # where:
    # - n is the number of nodes in the parse tree.
    # - v is the number of variables in a single subtree.
    # - o is the number of operations in the subtree.
    def dfs_traversal(self):
        declared_variables = []
        values = defaultdict(list)
        stack = [self.root]

        while stack:  # O(n)
            top = stack.pop()

            if top.name == Symbol("id"):
                data_type = top.children[0].name
                key_value_lines = self.extract_identifiers_and_values(top.children[1])  # O(v × o)
                for key, value, line in key_value_lines:  # O(v)
                    declared_variables.append(key)
                    values[key].append((data_type, value, line))

            elif top.name == Symbol("l"):
                key_value_lines = self.extract_identifiers_and_values(top)  # O(v × o)
                for key, value, line in key_value_lines:  # O(v)
                    if key in values:
                        data_type = values[key][0][0]
                        if (data_type, value, line) not in values[key]:
                            values[key].append((data_type, value, line))

            for child in reversed(top.children):  # O(w)
                stack.append(child)

        return declared_variables, values

    # Time Complexity: O(1) for lookup and string construction.
    def first_definition(self, identifier):
        if not identifier:
            return identifier
        data_type, value, line = self.values[identifier][0]
        definition = data_type + " " + identifier
        if value:
            definition += " = " + value
        return f"First definition of variable '{identifier}': {definition}; (line {line})"

    # Time Complexity: O(e × d × c),
    # where:
    # - e is the number of expressions in the values list.
    # - d is the average number of variables per expression.
    # - c is the average cost of evaluating an expression.
    def find_misstype(self):
        errors = []

        def evaluate_expression(exp: str, line):  # O(d × c)
            values = list(filter(lambda x: x not in "+-*", exp.split()))  # O(c)
            vars = list(filter(lambda x: not x.isdigit() and '.' not in x, values))  # O(d)
            data_type = "int"
            for var in vars:  # O(d)
                tmp = self.values.get(var)
                if tmp is None:
                    errors.append((f"- Error: Variable '{var}' is not declared at line {line}.", line))
                    return None
                if tmp[0][0] == "float":
                    data_type = "float"
            not_vars = list(filter(lambda x: x not in vars, values))  # O(c)
            for element in not_vars:  # O(c)
                if '.' in element:
                    return "float"
            return data_type

        for key in self.values:  # O(e)
            for assignment in self.values[key]:  # O(d)
                declared_type = assignment[0]
                assigned_type = declared_type
                if assignment[1]:
                    assigned_type = evaluate_expression(assignment[1], assignment[2])  # O(d × c)
                if declared_type != assigned_type and assigned_type is not None:
                    errors.append((
                        f"- Error: Cannot assign '{assigned_type}' to '{declared_type}' variable '{key}' at line {assignment[2]}.", assignment[2]
                    ))
        return sorted(errors, key=lambda x: int(x[1]))  # O(e log e)
