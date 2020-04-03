import re
from pandas import isnull

def return_args(args):
    if len(args) == 1:
        return args[0]
    else:
        return args

def join(*args, sep=''):
    """Joins the arguments with a separator in between. 
    Arguments that are None or np.nan are skipped.
    
    Parameters
    ----------
    sep : str, optional
        The separator placed between the arguments, by default ''
    
    Returns
    -------
    string
        The concatenated string
    """
    if type(args[0]) == list:
        outputs = [join(*arg, sep=sep) for arg in args]
        return return_args(outputs)
    else:
        joined = sep.join(str(arg) for arg in args if not isnull(arg))
    return joined

def split(*args, sep=None):
    """Splits the input string at the separator
    
    Parameters
    ----------
    *args
        list containing a single string
    sep : string, optional
        The separator, by default None
    
    Returns
    -------
    list
        A list of parts
    """
    assert len(args) == 1, "expects a single input"
    return args[0].split(sep)

def pick(*args, index=0):
    """Returns one argument from a list of arguments"""
    return args[index]

def first(*args):
    """Returns the first argument"""
    return args[0]

def last(*args):
    """Returns the last argument"""
    if type(args[0]) == list:
        outputs = [arg[-1] for arg in args]
        return return_args(outputs)
    else:
        return args[-1]

def lowercase(*args):
    """Transform all arguments to lowercase"""
    lowercased = [arg.lower() for arg in args]
    return return_args(lowercased)

def uppercase(*args):
    """Transform all arguments to uppercase"""
    uppercased = [arg.upper() for arg in args]
    return return_args(uppercased)

def titlecase(*args):
    """Transform all arguments to titlecase"""
    return [arg.title() for arg in args]

def rename(*args):
    """Passes the arguments, allowing you to rename them"""
    return return_args(args)

def to_int(*args):
    integers = [int(arg) for arg in args]
    return return_args(integers)

def to_float(*args):
    floats = args([float(arg) for arg in args])
    return return_args(floats)

def to_string(*args):
    strings = [str(arg) for arg in args]
    return return_args(strings)

def default(*args, values=[]):
    output = []
    for arg, default_value in zip(args, values):
        if arg is None:
            output.append(default_value)
        else:
            output.append(arg)
    return return_args(output)

def format(*args, pattern=None):
    """Format a string using positional placeholders.
    
    There are two ways of calling this function. First, you can
    provide a `pattern` keyword, which will then be formatted using
    the input arguments:

    ```python
    >>> format("hello", pattern="{} world")
    hello world
    ```

    Second, if the `pattern` is omitted, the first argument is used
    as pattern, and the other arguments are used for formatting:

    ```python
    >>> format('{} world', 'hello')
    hello world
    ```
    
    Parameters
    ----------
    pattern : string, optional
        The pattern to format using the input args, by default None
    
    Returns
    -------
    string
        The formatted string
    """
    if pattern is not None:
        return pattern.format(*args)
    elif len(args) > 1:
        pattern = args[0]
        return pattern.format(*args[1:])
    else:
        raise Exception('Either provide a pattern or multiple inputs')

def set_value(*args, value=None):
    values = [value] * len(args)
    return return_args(values)

def constant(*args, value=None):
    values = [value] * len(args)
    return return_args(values)

def regex_extract_groups(*args, pattern=None, extract_groups=None):
    matches = re.match(pattern, args[0])
    if matches:
        if extract_groups is None: 
            extract_groups = range(len(matches.regs))
        outputs = []
        for group_num in extract_groups:
            if matches[group_num] is not None:
                outputs.append(matches[group_num])
        return return_args(outputs)
    elif extract_groups is not None:
        outputs = [None for _ in range(len(extract_groups))]
        return return_args(outputs)
    else:
        raise Exception('Regex did not match, cannot determine how many groups to return.\
            Provide the `extract_groups` argument should resolve this.')

def map_values(*args, mapping={}, regex=True):
    """Map input values to other values according to a dictionary mapping.
    It tests whether an input value matches any of the keys in the mapping
    dictionary using a regular expression. If so, the value is replaced
    by the value in the mapping dictionary. If the input matches none of the
    keys, `None` is returned.
    
    Parameters
    ----------
    mapping : dict
        A dictionary with regex patterns as keys. If an input matches
        the pattern, it is replaced by the value in this dictionary.
    regex : bool, optional
        Use regular expressions? If False, it performs a literal match.
        By default True.
    
    Returns
    -------
    list
        The list of new values, or just the new value if only a 
        single argument is passed
    """
    if not regex:
        outputs = [mapping.get(arg, None) for arg in args]
        return return_args(outputs)
    else:
        outputs = []
        for orig_value in args:
            found_match = False
            for pattern, target_value in mapping.items():
                matches = re.match(pattern, orig_value)
                if matches:
                    outputs.append(target_value)
                    found_match = True
            if not found_match:
                outputs.append(None)
        return return_args(outputs)
