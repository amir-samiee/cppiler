import re

token_specs = [
    ('reservedword', r'#include|\b(int|float|void|return|if|while|cin|cout|continue|break|using|iostream|namespace|std|main)\b'),
    ('identifier', r'[a-zA-Z][a-zA-Z0-9]*'),
    ('number', r'\d+'),
    ('string', r'"([^"]*)"'),
    ('symbol', r'[()\[\]\{\},;]|(\+|-|\*|/|==|!=|<=|>=|<<|>>|=|\|\||&&|<|>)'),
    ('whitespace', r'\s+'),
    ('unknown', r'.'),
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
                    if token_name != 'whitespace' and token_name != 'comment':
                        tokens.append((token_name, group))
                    position = match.end()
                    break
        else:
            raise ValueError(f'Invalid character at position {position}: {code[position]}')
    
    return tokens