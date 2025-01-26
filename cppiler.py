from parse_tree import ParseTree
from npp import nonrecursive_predictive_parser
from lexical_analyzer import lex
from anytree import RenderTree
import rich
from cfg import CFG, CFG_RULES_STR
from token_table import TokenTable
from assets import clear_screen

if __name__ == "__main__":
    file_path = input("enter the path to your file (0 => exit): ")
    if file_path == "0":
        quit()
    code = ""
    with open(file_path, "r") as file:
        code = file.read()

    tokens = lex(code)
    token_tale = TokenTable(tokens)
    token_tale.save_table()
    cfg = CFG(CFG_RULES_STR)
    cfg.save_parse_table()
    try:
        productions = nonrecursive_predictive_parser(tokens, cfg)
    except SyntaxError as err:
        print(err)
        quit()
    tree = ParseTree(productions)

    searching_variable = ""
    while True:
        
        clear_screen()
        
        for pre, fill, node in RenderTree(tree.root):
            rich.print(f"{pre}{node.name}")
        print('\n')

        if searching_variable:
            print(tree.first_definition(searching_variable))
        
        searching_variable = input("Enter a variable to find the first definition for (0 => quit):")
        if searching_variable == '0':
            quit()