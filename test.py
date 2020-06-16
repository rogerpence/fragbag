import sys, os, re
from collections import OrderedDict
import click, pyperclip
import rplib

TOKENS_DELIMITER = '||'
ESCAPED_TOKENS_DELIMITER = '\|\|'


def get_tokens_in_string(contents, token_delimiter):
    matches = re.finditer(token_delimiter, contents)
    positions = [match.start() for match in matches]

    initial_tokens = []
    for i in range(0, len(positions), 2):
        initial_tokens.append(contents[positions[i]+2: positions[i+1]])

    initial_tokens = list(OrderedDict.fromkeys(initial_tokens))

    tokens = []
    defaults = {}

    for token in initial_tokens:
        if '=' in token:
            value_pair = re.split('\s*\=\s*', token)
            token = value_pair[0]
            tokens.append(value_pair[0])
            defaults[value_pair[0]] = value_pair[1]
        else:
            tokens.append(token)

    return tokens, defaults

contents = rplib.read_file('tw\\form-field-test.html')
get_tokens_in_string(contents, ESCAPED_TOKENS_DELIMITER)