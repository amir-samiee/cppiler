from assets import Token_names as tkn, Re_names as ren
import re

# Time Complexity: O(n), where n is the total length of all regex patterns in `token_specs`.
def generate_patterns():
    token_specs = [
        (tkn.reservedword.name,
         r'#include|\b(int|float|void|return|if|while|cin|cout|continue|break|using|iostream|namespace|std|main)\b'),
        (tkn.identifier.name, r'[a-zA-Z][a-zA-Z0-9]*'),
        (tkn.number.name, r'\d+(\.\d+)?'),
        (tkn.string.name, r'"([^"]*)"'),
        (tkn.symbol.name,
         r'[()\[\]\{\},;]|(\+|-|\*|/|==|!=|<=|>=|<<|>>|=|\|\||&&|<|>)'),
        (ren.whitespace.name, r'\s+'),
        (ren.unknown.name, r'.'),
    ]
    master_pattern = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specs)
    return re.compile(master_pattern)

# Time Complexity: O(m × (n + k)),
# where:
# - m is the number of tokens in `code`.
# - n is the total length of all regex patterns in `token_specs`.
# - k is the average length of a token.
def lex(code):
    position = 0
    line = 1
    column = 1
    tokens = []
    compiled_regex = generate_patterns()

    while position < len(code):
        match = compiled_regex.match(code, position)
        if match:
            for token_name, token_value in match.groupdict().items():
                if token_value is not None:
                    if token_name != ren.whitespace.name:
                        tokens.append((token_name, token_value, line, column))
                    position = match.end()
                    line_breaks = token_value.count('\n')
                    if line_breaks > 0:
                        line += line_breaks
                        column = len(token_value.split('\n')[-1]) + 1
                    else:
                        column += len(token_value)
                    break
        else:
            raise ValueError(f'Invalid character at line {line}, column {column}: {code[position]}')
    return tokens
