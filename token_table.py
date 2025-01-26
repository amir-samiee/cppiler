from assets import Token_names as tkn
from collections import defaultdict
import hashlib
from tabulate import tabulate
import os

class TokenTable:
    # Time Complexity: O(m log m + t × k),
    # where:
    # - m is the total number of tokens.
    # - t is the number of unique token types in `tkn`.
    # - k is the average number of tokens per token type.
    def __init__(self, tokens: list):
        grouped_tokens = defaultdict(list)
        token_table = []

        # Group tokens by type
        for token_name, token_value, _, _ in tokens:  # O(m)
            grouped_tokens[token_name].append(token_value)

        # Sort each group of tokens
        for token_name in grouped_tokens:  # O(t × k log k)
            grouped_tokens[token_name].sort()

        # Generate hashed values for the token table
        for token_type in tkn:  # O(t × k)
            token_name = token_type.name
            if token_name in grouped_tokens:
                for token_value in grouped_tokens[token_name]:
                    token_table.append(self.calculate_hash(token_name, token_value))

        self.token_table = token_table

    # Time Complexity: O(n),
    # where n is the length of the string `f"{token_name}#{token_value}"`.
    def calculate_hash(self, token_name, token_value):
        value = f"{token_name}#{token_value}"  # O(len(token_name) + len(token_value))
        return hashlib.sha256(value.encode()).hexdigest()  # O(n)

    # Time Complexity: O(h),
    # where h is the number of hash values in the token table.
    def save_table(self):
        data = self.token_table
        rows = []
        headers = ["Hash Values"]

        # Prepare rows for tabulation
        for hashed_value in data:  # O(h)
            rows.append([hashed_value])

        # Write the token table to a file
        with open("token_table.txt", "w") as file:  # O(h) (writing all rows to the file)
            file.write(str(tabulate(rows, headers=headers, tablefmt="grid")) + "\n")
