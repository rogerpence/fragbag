import sys, os, re
from collections import OrderedDict
import click, pyperclip, jinja2
import rplib

TOKENS_DELIMITER = '||'

def load_template(template_file, searchpath):
    template_loader = jinja2.FileSystemLoader(searchpath='./' + searchpath)
    template_env = jinja2.Environment(
        loader=template_loader,
        lstrip_blocks=True,
        trim_blocks=True,
        variable_start_string='||',
        variable_end_string='||'
        )
        # ,block_start_string='@@',block_end_string='@@',)

    return template_env.get_template(template_file)

def render_template(loaded_template, token_dict):
    try:
        template_results = loaded_template.render(token_dict)
    except Exception as error:
        print('Error merging schema data with the template.')
        print(str(error))
        exit(1)

    return template_results

def prompt_for_token_values(contents):
    tokens = get_template_tokens(contents, omit_filters=False)
    replacements = {}
    if len(tokens) == 0:
        return {}

    for token in tokens:
        token_value = input(f'{token}: ')
        replacements[token] = token_value
    return replacements

def get_escaped_tokens_delimiter():
    escaped_tokens_delimiter = []
    for ch in TOKENS_DELIMITER:
        escaped_tokens_delimiter.append('\\')
        escaped_tokens_delimiter.append(ch)

    return ''.join(escaped_tokens_delimiter)

def get_template_tokens(contents, omit_filters=True):
    escaped_tokens_delimiter = get_escaped_tokens_delimiter()

    matches = re.finditer(escaped_tokens_delimiter, contents)
    positions = [match.start() for match in matches]

    tokens = []
    for i in range(0, len(positions), 2):
        current_token = contents[positions[i]+2: positions[i+1]].strip()
        if omit_filters:
            current_token = re.sub('\s*\|.*$', '', current_token)
        tokens.append(current_token)

    return list(OrderedDict.fromkeys(tokens))

def get_template(file_name):
    contents = rplib.read_file(file_name)
    return contents

def confirm_directory(ctx, parm, value):
    if os.path.isdir(value):
        return value
    else:
        raise click.BadParameter(f'[{value}] directory does not exist')

def confirm_template(ctx, parm, value):
    directory = ctx.params['directory']
    target = os.path.join(directory, value)
    if os.path.isfile(target):
        return value
    else:
        raise click.BadParameter(f'[{value}] file does not exist')

def confirm_subs(ctx, parm, value):
    if len(value) % 2 == 0:
        return value
    else:
        raise click.BadParameter(f'[{value}] provide an even number of subs')

def convert_tuple_to_dict(tup):
    if len(tup) % 2 != 0:
        print('error: tuple must be even')
        exit()

    result = {}
    for i in range(0, len(tup), 2):
        result[tup[i]] = tup[i+1]
    return result

@click.command()
@click.option('-d', '--directory', required=True, callback=confirm_directory, help="Directory name")
@click.option('-t', '--template', required=True, callback=confirm_template, help="Template name")
@click.option('--show-tokens/--no-show-tokens',default=False, required=False, help="Show token names")
@click.option('--prompt-tokens/--no-prompt-tokens',default=False, required=False, help="Prompt for token values")
@click.option('--subs', nargs=0, required=False, callback=confirm_subs, help="Substution values")
@click.argument('subs', nargs=-1)
def main(directory, template, show_tokens, prompt_tokens, subs):
    template_file_name = os.path.join(directory, template)
    print(f'Working with template: {template_file_name}')

    template_contents = get_template(template_file_name)
    tokens = get_template_tokens(template_contents)

    loaded_template = load_template(template, directory)

    if show_tokens:
        print(tokens)
        pyperclip.copy(', '.join(tokens))
        exit(0)
    elif prompt_tokens:
        template_data = prompt_for_token_values(template_contents)
        template_results = render_template(loaded_template, template_data)
    else:
        template_data = convert_tuple_to_dict(subs)
        template_results = render_template(loaded_template, template_data)

    # or append to file.
    pyperclip.copy(template_results)
    print('Template results on clipboard')

if __name__ == '__main__':
    main()