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
    
    def find_variable_definition(self, target_name):
        node = self.BFS(target_name)
        if node == None:
            return f"No definition found for '{target_name}'."
        id_node = node.parent
        
        while id_node.name != Symbol('id'):
            id_node = id_node.parent
        data_type = id_node.children[0].name

        assignment_node = None
        for sibling in node.parent.siblings:
            if sibling.name == Symbol('assign'):
                assignment_node = sibling
        value = ";"
        if '=' in [mynode.name for mynode in assignment_node.children]:
            value_node = assignment_node.children[1].children[0].children[0]
            value = f' = {value_node.name}' + value
        

        return data_type + ' ' + node.name + value