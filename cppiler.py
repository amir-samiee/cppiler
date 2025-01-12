from parse_tree import parse_tree
from nonrecursive_predictive_parser import nonrecursive_predictive_parser
from lexical_analyzer import lex
from anytree import RenderTree
import rich
from cfg import CFG, CFG_RULES_STR

if __name__ == "__main__":
    file_path = input("enter the path to your file to compile (q => exit): ")
    if file_path == "q":
        quit()
    code = ""
    with open(file_path, "r") as file:
        code = file.read()

    tokenized = lex(code)
    cfg = CFG(CFG_RULES_STR)
    productions = nonrecursive_predictive_parser(tokenized, cfg)
    tree = parse_tree(productions)

    for pre, fill, node in RenderTree(tree):
        rich.print(f"{pre}{node.name}")
