from assets import Token_names as tkn, Re_names as ren
import re

token_specs = [
    (tkn.reservedword.name,
     r'#include|\b(int|float|void|return|if|while|cin|cout|continue|break|using|iostream|namespace|std|main)\b'),
    (tkn.identifier.name, r'[a-zA-Z][a-zA-Z0-9]*'),
    (tkn.number.name, r'\d+'),
    (tkn.string.name, r'"([^"]*)"'),
    (tkn.symbol.name,
     r'[()\[\]\{\},;]|(\+|-|\*|/|==|!=|<=|>=|<<|>>|=|\|\||&&|<|>)'),
    (ren.whitespace.name, r'\s+'),
    (ren.unknown.name, r'.'),
]

master_pattern = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specs)
compiled_regex = re.compile(master_pattern)


def lex(code):
    position = 0
    tokens = []

    while position < len(code):
        match = compiled_regex.match(code, position)
        if match:
            for token_name, group in match.groupdict().items():
                if group is not None:
                    if token_name != ren.whitespace.name:
                        tokens.append((token_name, group))
                    position = match.end()
                    break
        else:
            raise ValueError(f'Invalid character at position {
                             position}: {code[position]}')

    return tokens
