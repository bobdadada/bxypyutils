import json
import os
import six
import re

__all__ = ['json_minify', 'write_json', 'load_json']

def json_minify(string, strip_space=True):
    """A port of the `JSON-minify` utility to the Python language.
    Based on JSON.minify.js: https://github.com/getify/JSON.minify
    Contributers:
    - Gerald Storer
        - Contributed original version
    - Felipe Machado
        - Performance optimization
    - Pradyun S. Gedam
        - Conditions and variable names changed
        - Reformatted tests and moved to separate file
        - Made into a PyPI Package
    """
    tokenizer = re.compile('"|(/\*)|(\*/)|(//)|\n|\r')
    end_slashes_re = re.compile(r'(\\)*$')

    in_string = False
    in_multi = False
    in_single = False

    new_str = []
    index = 0

    for match in re.finditer(tokenizer, string):

        if not (in_multi or in_single):
            tmp = string[index:match.start()]
            if not in_string and strip_space:
                # replace white space as defined in standard
                tmp = re.sub('[ \t\n\r]+', '', tmp)
            new_str.append(tmp)
        elif not strip_space:
            # Replace comments with white space so that the JSON parser reports
            # the correct column numbers on parsing errors.
            new_str.append(' ' * (match.start() - index))

        index = match.end()
        val = match.group()

        if val == '"' and not (in_multi or in_single):
            escaped = end_slashes_re.search(string, 0, match.start())

            # start of string or unescaped quote character to end string
            if not in_string or (escaped is None or len(escaped.group()) % 2 == 0):  # noqa
                in_string = not in_string
            index -= 1  # include " character in next catch
        elif not (in_string or in_multi or in_single):
            if val == '/*':
                in_multi = True
            elif val == '//':
                in_single = True
        elif val == '*/' and in_multi and not (in_string or in_single):
            in_multi = False
            if not strip_space:
                new_str.append(' ' * len(val))
        elif val in '\r\n' and not (in_multi or in_string) and in_single:
            in_single = False
        elif not ((in_multi or in_single) or (val in ' \r\n\t' and strip_space)):  # noqa
            new_str.append(val)

        if not strip_space:
            if val in '\r\n':
                new_str.append(val)
            elif in_multi or in_single:
                new_str.append(' ' * len(val))

    new_str.append(string[index:])
    return ''.join(new_str)

def write_json(path, data):

    path = os.path.abspath(path)

    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path, 'w', encoding='utf-8') as fd:
        json.dump(data, fd, indent=4, sort_keys=True)

def load_json(path, js_comments=False):

    path = os.path.abspath(path)

    with open(path, 'r', encoding='utf-8') as fd:
        content = fd.read()

    if js_comments:
        content = json_minify(content)
        content = content.replace(",]", "]")
        content = content.replace(",}", "}")

    try:
        d = json.loads(content)
    except ValueError as e:
        raise Exception(
            "Error parsing JSON in file '{0}': {1}".format(
                path, six.text_type(e)))

    return d

