from assets import Token_names as tkn, Re_names as ren
from collections import defaultdict
import re
import hashlib

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

def lex(code):
    position = 0
    tokens = []
    compiled_regex = generate_patterns()

    while position < len(code):
        match = compiled_regex.match(code, position)
        if match:
            for token_name, token_value in match.groupdict().items():
                if token_value is not None:
                    if token_name != ren.whitespace.name:
                        tokens.append((token_name, token_value))
                    position = match.end()
                    break
        else:
            raise ValueError(f'Invalid character at position {
                             position}: {code[position]}')
    return tokens

def calculate_hash(token_name, token_value):
    value = f"{token_name}#{token_value}"
    return hashlib.sha256(value.encode()).hexdigest()

def create_token_table(tokens:list):
    grouped_tokens = defaultdict(list)
    token_table = []
    
    for token_name, token_value in tokens:
        grouped_tokens[token_name].append(token_value)
    for token_name in grouped_tokens:
        grouped_tokens[token_name].sort()
    for token_type in tkn:
        token_name = token_type.name
        if token_name in grouped_tokens:
            for token_value in grouped_tokens[token_name]:
                token_table.append(calculate_hash(token_name, token_value))

    return token_table