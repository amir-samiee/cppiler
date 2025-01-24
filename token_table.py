from assets import Token_names as tkn
from collections import defaultdict
import hashlib
from tabulate import tabulate
import os

class TokenTable:
    def __init__(self, tokens:list):
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
                    token_table.append(self.calculate_hash(token_name, token_value))
        self.token_table = token_table

    def calculate_hash(self, token_name, token_value):
        value = f"{token_name}#{token_value}"
        return hashlib.sha256(value.encode()).hexdigest()

    def save_table(self):
        data = self.token_table
        rows = []
        headers = ["Hash Values"]

        for hashed_value in data:
            rows.append([hashed_value])

        with open("token_table.txt", "w") as file:
            file.write(str(tabulate(rows, headers=headers, tablefmt="grid")) + "\n")
