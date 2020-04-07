"""This module collects all operations that can be used in a
transformation using the Transformer class.

Most operations accept multiple inputs. The output size will always
match the input size. So if you pass just a single argument, you
will get a single output, and not a list with one item:

>>> lowercase('THIS', 'IS', 'A', 'TEST')
['this', 'is', 'a', 'test']
>>> lowercase('THIS IS A TEST')
'this is a test'
"""
#
import re
import html
from pandas import isnull

def _return(args):
    """Returns a single value if a single argument was passed,
    and a list of values if multiple arguments were passed.
    This function is used to ensure that the number of inputs
    matches the number of outputs"""
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
        The separator placed between the arguments, by default ``''``
    
    Returns
    -------
    string
        The concatenated string
    """
    if type(args[0]) == list:
        outputs = [join(*arg, sep=sep) for arg in args]
        return _return(outputs)
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
    return args[index]

def first(*args):
    """Returns the first argument"""
    return args[0]

def last(*args):
    """Returns the last argument"""
    if type(args[0]) == list:
        outputs = [arg[-1] for arg in args]
        return _return(outputs)
    else:
        return args[-1]

def lowercase(*args):
    """Transform all arguments to lowercase"""
    outputs = []
    for arg in args:
        if type(arg) == str:
            outputs.append(arg.lower())
        else:
            outputs.append(arg)
    return _return(outputs)

def uppercase(*args):
    """Transform all arguments to uppercase

    >>> uppercase('this is a test')
    'THIS IS A TEST'
    >>> uppercase('this is', 'another test')
    ['THIS IS', 'ANOTHER TEST']
    
    Returns
    -------
    [type]
        [description]
    """
    uppercased = [arg.upper() for arg in args]
    return _return(uppercased)

def titlecase(*args):
    """Transform all arguments to titlecase

    >>> titlecase('this is a test')
    'This Is A Test'
    >>> titlecase('This is', 'another test')
    ['This Is', 'Another Test']
    
    Returns
    -------
    string(s)
        The titlecased input strings
    """
    outputs = [arg.title() for arg in args]
    return _return(outputs)

def rename(*args):
    """Passes the arguments allowing you to rename them.

    >>> rename('foo')
    'foo'
    >>> rename(1, 2, 3)
    (1, 2, 3)
    
    Returns
    -------
    mixed
        Whatever you pass as arguments is returned
    """
    return _return(args)

def to_int(*args):
    integers = [int(arg) for arg in args]
    return _return(integers)

def to_float(*args):
    floats = args([float(arg) for arg in args])
    return _return(floats)

def to_string(*args):
    strings = [str(arg) for arg in args]
    return _return(strings)

def default(*args, values=[]):
    output = []
    for arg, default_value in zip(args, values):
        if arg is None:
            output.append(default_value)
        else:
            output.append(arg)
    return _return(output)

def format(*args, pattern=None):
    """Format a string using positional placeholders.
    
    There are two ways of calling this function. First, you can
    provide a `pattern` keyword, which will then be formatted using
    the input arguments:

    
    >>> format("hello", pattern="{} world")
    'hello world'

    Second, if the `pattern` is omitted, the first argument is used
    as pattern, and the other arguments are used for formatting:

    >>> format('{} world', 'hello')
    'hello world'
    
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

def constant(*args, value=None):
    """Returns a constant value. This allows you to introduce constant
    or default values into the computation graph. The function returns 
    as many values as you provide input argument. The inputs are otherwise
    ignored.

    >>> constant('_', value=4)
    4
    >>> constant('_', '_', '_', value='foo')
    ['foo', 'foo', 'foo']
    
    Parameters
    ----------
    value : mixed, optional
        The value of the constant, by default None
    
    Returns
    -------
    mixed
        The value, or a list of values
    """
    values = [value] * len(args)
    return _return(values)

def unescape_html(*args):
    """Unescape an html string: replace html special characters
    by utf-8 characters.

    >>> unescape_html('f&ouml;&ograve; bar')
    'föò bar'
    
    Returns
    -------
    string(s)
        Unescaped html string
    """
    outputs = []
    for arg in args:
        try:
            outputs.append(html.unescape(arg))
        except TypeError:
            outputs.append(arg)
    return _return(outputs)
    

def extract_groups(string, pattern=None, groups=None):
    """Extract parts of a string using a regular expression:
    it returns the groups of the regular expression
    
    Examples
    --------

    >>> extract_groups('foo-bar', pattern='(.+)\-(.+)')
    ['foo-bar', 'foo', 'bar']

    >>> extract_groups('foo-bar', pattern='(.+)\-(.+)', groups=[1,2])
    ['foo', 'bar']

    Parameters
    ----------
    string : str
        The input string from which the groups are extracted
    pattern : str
        The regular expression, by default None
    groups : [type], optional
        A list of indices (!) of groups to return. Note that group 0
        is the entire input string, so group 1 is the first group 
        specified by the regex. Defaults to returning all groups.
    
    Returns
    -------
    list
        A list of extracted groups (strings), or a string if only
        one group has to be returned
    """
    matches = re.match(pattern, string)
    if matches:
        if groups is None: 
            groups = range(len(matches.regs))
        outputs = []
        for group_num in groups:
            if matches[group_num] is not None:
                outputs.append(matches[group_num])
        return _return(outputs)
    elif groups is not None:
        outputs = [None for _ in range(len(groups))]
        return _return(outputs)
    else:
        raise Exception('Regex did not match, cannot determine how many groups to return.\
            Provide the `groups` argument should resolve this.')

def map_values(*args, mapping={}, regex=True, return_missing=False):
    """Map input values to other values according to a dictionary mapping.
    It tests whether an input value matches any of the keys in the mapping
    dictionary using a regular expression. If so, the value is replaced
    by the value in the mapping dictionary. When there is no match,
    the input string is returned if `return_missing` is True; else `None`.

    >>> map_values('foo', 'bar', 'fop', mapping={'fo.': 'FOO!'})
    ['FOO!', None, 'FOO!']

    >>> map_values('foo', 'bar', 'fop', mapping={'fo.': 'FOO!'}, return_missing=True)
    ['FOO!', 'bar', 'FOO!']

    >>> map_values('foo', 'bar', 'fo.', mapping={'fo.': 'FOO!'}, regex=False)
    [None, None, 'FOO!']
    
    Parameters
    ----------
    mapping : dict
        A dictionary with regex patterns as keys. If an input matches
        the pattern, it is replaced by the value in this dictionary.
    regex : bool, optional
        Use regular expressions? If False, it performs a literal match.
        By default True.
    return_missing : bool, optional
        Return input values when they are not matched to any entry in 
        the mapping? Otherwise, it returns None for those values. 
        Default to False.
    
    Returns
    -------
    list
        The list of new values, or just the new value if only a 
        single argument is passed
    """
    if not regex:
        if return_missing:
            outputs = [mapping.get(arg, arg) for arg in args]
        else:
            outputs = [mapping.get(arg, None) for arg in args]
        return _return(outputs)
    else:
        outputs = []
        for orig_value in args:
            found_match = False
            for pattern, target_value in mapping.items():
                if not type(orig_value) == str: continue
                matches = re.match(pattern, orig_value)
                if matches:
                    outputs.append(target_value)
                    found_match = True
                    continue
            if not found_match:
                default = orig_value if return_missing else None
                outputs.append(default)
        return _return(outputs)


def map_numeric_bins(*args, bins=[], default=None):
    """Map numbers to values corresponding to certain bins.
    Bins are dictionaries with a `min`, `max` (exclusive)
    and `value` attribute. For example:

    >>> bins = [
    ...    {'min': 0, 'max': 10, 'value': 'foo'},
    ...    {'min': 10, 'max': 100, 'value': 'bar'}
    ... ]
    >>> map_numeric_bins(2, bins=bins)
    'foo'
    >>> map_numeric_bins(20, bins=bins)
    'bar'
    
    Parameters
    ----------
    bins : list
        A list of bins; see above.
    default : string, optional
        Default value if none of the bins matched, 
        by default None
    
    Returns
    -------
    list
        A list of output values
    """
    outputs = []
    for arg in args:
        try:
            orig_value = float(arg)
            found_match = False
            for value_bin in bins:
                if value_bin['min'] <= orig_value < value_bin['max']:
                    outputs.append(value_bin['value'])
                    found_match = True
                    break
            if not found_match:
                outputs.append(default) 
        except:
            outputs.append(default)
    return _return(outputs)

if __name__ == '__main__':
    import doctest
    doctest.testmod()