import re
from collections import OrderedDict

def get_escaped_delimiter(delimiter):
    escaped_tokens_delimiter = []
    for ch in delimiter:
        escaped_tokens_delimiter.append('\\')
        escaped_tokens_delimiter.append(ch)

    return ''.join(escaped_tokens_delimiter)

def get_unique_tokens_with_same_delimiter(delimiter, buffer):
    escaped_delimiter = get_escaped_delimiter(delimiter)
    matches = re.finditer(escaped_delimiter, buffer)
    positions = [match.start() for match in matches]

    if len(positions) % 2 != 0:
        print('delimiters not correctly matched')
        exit()

    tokens = []
    for i in range(0, len(positions), 2):
        current_token = buffer[positions[i]+2: positions[i+1]].strip()
        current_token = re.sub('\s*\|.*$', '', current_token)
        tokens.append(current_token)

    return  list(OrderedDict.fromkeys(tokens))

def get_unique_tokens_with_diff_delimiter(begin_delimiter, end_delimiter, buffer):

    def get_matching_positions(delimiter, buffer):
        escaped_delimiter = get_escaped_delimiter(delimiter)
        matches = re.finditer(escaped_delimiter, buffer)
        positions = [match.start() for match in matches]

        return positions

    begin_positions = get_matching_positions(begin_delimiter, buffer)
    end_positions = get_matching_positions(end_delimiter, buffer)

    if len(begin_positions) != len(end_positions):
        print('delimiters not correctly matched')
        exit()

    tokens = []
    counter = 0
    for begin_pos in begin_positions:
        end_pos = end_positions[counter]
        counter += 1
        current_token = buffer[begin_pos + len(begin_delimiter): end_pos].strip()
        current_token = re.sub('\s*\|.*$', '', current_token)
        tokens.append(current_token)

    return list(OrderedDict.fromkeys(tokens))




if __name__ == '__main__':

# ------ same delimiters

    buffer = \
'form_||model_instance|| = ||model_bbnstance | capitalize||Form(request.POST or None)form_||model_instance||.is_valid()'

    delimiter = '||'

    unique_tokens = get_unique_tokens_with_same_delimiter(delimiter, buffer)

    print('unique tokens:')
    print(unique_tokens)

# ------ different delimiters

    buffer = \
'form_{{model_instance}} = {{model_bbnstance | capitalize}}Form(request.POST or None)form_{{model_instance}}.is_valid()'

    begin_delimiter = '{{'
    end_delimiter = '}}'

    unique_tokens = get_unique_tokens_with_diff_delimiter(begin_delimiter, end_delimiter, buffer)

    print('unique tokens:')
    print(unique_tokens)