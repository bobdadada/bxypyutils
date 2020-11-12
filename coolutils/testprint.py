"""
We introduce some useful functions to print attributes of target object.
"""
__all__ = ['display', 'camel_attr_print', 'trace']

import functools
import itertools
import sys


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result

    return wrapper


def _decorator_write_to_file(file):
    def wrapper(func):
        if not _validate_file_object(file):
            print("File doesn't have write() method. Print to sys.stdout\n")
            return func
        else:
            @functools.wraps(func)
            def nfunc(*args, **kwargs):
                return func(*args, file=file, **kwargs)

            return nfunc

    return wrapper


def _validate_file_object(file):
    if not hasattr(file, 'write'):
        return False
    return True


def display(obj, tp, *args, file=sys.stdout, **kwargs):
    """
    :param obj: specify your input object. It can be anything available in Python.
    :param tp: specify the type of what you want to print.  It can be 'state', 'attr', 'func', 'item'
    :param file: print the output to the file. the file must have write() method.

    >>>import numpy as np
    >>>display(np, 'attr', 'array')
    object: <module 'numpy' from 'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\numpy\\__init__.py'>
    attribute name: array
    attribute: <built-in function array>
    >>>display(np, 'func', 'array', [313])
    object: <module 'numpy' from 'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\numpy\\__init__.py'>
    function: array
    function in: ([313],) {}
    function return: [313]
    >>>display('1 in [1,32,4]', 'state')
    statement: 1 in [1,32,4]
    return: True
    >>>display('1 in a', 'state', {'a':[1,2,3,4]})
    statement: 1 in a
    return: True
    >>>display([1,3,23], 'item', 0)
    object: [1, 3, 23]
    item sequence: (0,)
    item return: 1
    >>>display([[23,424],3,23], 'item', 0, 1)
    object: [[23, 424], 3, 23]
    item sequence: (0, 1)
    item return: 424
    """
    if file != sys.stdout:
        mprint = _decorator_write_to_file(file)(print)
    else:
        mprint = print
    if tp == 'item':
        _display_item(obj, *args, mprint=mprint)
    elif tp == 'attr':
        _display_attr(obj, *args, mprint=mprint)
    elif tp == 'func':
        _display_func(obj, *args, mprint=mprint, **kwargs)
    elif tp == 'state':
        _display_state(obj, *args, mprint=mprint)
    else:
        print('Sorry, please choose a type "item", "attr", "func", "state"')


def camel_attr_print(obj, file=sys.stdout):
    """
    :param obj: specify your input object. It can be anything available in Python.
    :param file: print the output to the file. the file must have write() method.

    >>>import numpy as np
    >>>camel_attr_print(np)
    object: <module 'numpy' from 'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\numpy\\__init__.py'>
    attribute name: __NUMPY_SETUP__
    attribute: False

    object: <module 'numpy' from 'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\numpy\\__init__.py'>
    attribute name: __all__
    ...
    """
    if not _validate_file_object(file):
        print("File doesn't have write() method. Print to sys.stdout\n")
        file = sys.stdout
    i = itertools.filterfalse(_find_not_camel, dir(obj))
    display(obj, 'attr', *i, file=file)


def _find_not_camel(s):
    if s.startswith('__') and s not in ('__doc__', '__builtins__'):
        return False
    else:
        return True


def _display_attr(obj, *attrs, mprint=print):
    mprint('object:', obj)
    for attr in attrs:
        mprint('attribute name:', attr)
        attr = getattr(obj, attr)
        mprint('attribute:', attr)
    mprint('')


def _display_func(obj, func, *args, mprint=print, **kwargs):
    mprint('object:', obj)
    mprint('function:', func)
    attr = getattr(obj, func)
    mprint('function in:', args, kwargs)
    mprint('function return:', attr(*args, **kwargs))
    mprint('')


def _display_item(obj, *items, mprint=print):
    mprint('object:', obj)
    mprint('item sequence:', items)
    r = obj
    for item in items:
        r = r[item]
    mprint('item return:', r)
    mprint('')


def _display_state(statement, *args, mprint=print):
    mprint('statement:', statement)
    mprint('return:', eval(statement, *args))
    mprint('')
