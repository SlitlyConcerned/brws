def get_docstring(f, if_none=None):
    doc = f.__doc__
    if doc is none:
        return if_none
    else:
        return doc

def print_docstring(f, if_none=None, **kwargs):
    print(get_docstring(f, if_none), **kwargs)
