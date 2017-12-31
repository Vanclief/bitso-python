def dict_to_float(d):
    """
    Converts all strings to floats from a dict
    """
    if type(d) is dict:
        for key, value in d.items():
            if type(value) is str:
                try:
                    d[key] = float(value)
                except ValueError:
                    d[key] = str(value)

    return d


def list_dict_to_float(l):
    """
    Applies dict_to_float to all elements from a list
    """
    for d in l:
        d = dict_to_float(d)

    return l


def parse_symbol(s):
    """
    Converts from btcmxn to ?book=btc_mxn
    """
    s = s[:3] + "_" + s[3:]
    return "?book={0}".format(s)


def unparse_symbol(s):
    """
    Converts from btc_mxn  btcmxn
    """
    return s[:3] + s[4:]
