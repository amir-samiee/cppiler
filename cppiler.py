from parse_tree import ParseTree
from nonrecursive_predictive_parser import nonrecursive_predictive_parser
from lexical_analyzer import lex
from anytree import RenderTree
import rich
from cfg import CFG, CFG_RULES_STR

if __name__ == "__main__":
    file_path = input("enter the path to your file (q => exit): ")
    if file_path == "q":
        quit()
    code = ""
    with open(file_path, "r") as file:
        code = file.read()

    tokenized = lex(code)
    cfg = CFG(CFG_RULES_STR)
    productions = nonrecursive_predictive_parser(tokenized, cfg)
    tree = ParseTree(productions)

    for pre, fill, node in RenderTree(tree.root):
        rich.print(f"{pre}{node.name}")
    print(tree.find_variable_definition(input()))
