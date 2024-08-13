import keyword


def mynamedtuple(typename, fields, defaults=None):
    if not typename.isidentifier() or typename in keyword.kwlist:
        raise SyntaxError(f"Invalid type name: '{typename}'")

    if isinstance(fields, str):
        fields = fields.replace(',', ' ').split()
    fields = list(dict.fromkeys(fields))  # Remove duplicates

    if any(not field.isidentifier() or field in keyword.kwlist for field in fields):
        raise SyntaxError(f"Invalid field names in: {fields}")

    if defaults is None:
        defaults = {}
    else:
        invalid_defaults = set(defaults) - set(fields)
        if invalid_defaults:
            raise SyntaxError(f"Invalid defaults for fields: {invalid_defaults}")

    class_str = f"class {typename}:\n"
    class_str += f"    _fields = {fields}\n"
    class_str += f"    _mutable = False\n\n"

    params = ", ".join([f"{f}={defaults[f]}" if f in defaults else f for f in fields])
    init_body = "\n".join([f"        self.{f} = {f}" for f in fields])
    class_str += f"    def __init__(self, {params}):\n{init_body}\n\n"

    repr_body = ", ".join([f"{f}={{self.{f}!r}}" for f in fields])
    class_str += f"    def __repr__(self):\n"
    class_str += f"        return f'{typename}({repr_body})'\n\n"

    for field in fields:
        class_str += f"    def get_{field}(self):\n"
        class_str += f"        return self.{field}\n\n"

    eq_body = " and ".join([f"self.{f} == other.{f}" for f in fields])
    class_str += f"    def __eq__(self, other):\n"
    class_str += f"        return isinstance(other, {typename}) and {eq_body}\n\n"

    getitem_body = "\n".join([f"        if index == {i}: return self.{f}" for i, f in enumerate(fields)])
    class_str += f"    def __getitem__(self, index):\n{getitem_body}\n"
    class_str += f"        raise IndexError('Index out of range')\n\n"

    asdict_body = ", ".join([f"'{f}': self.{f}" for f in fields])
    class_str += f"    def asdict(self):\n"
    class_str += f"        return {{{asdict_body}}}\n\n"

    make_body = ", ".join([f"iterable[{i}]" for i, _ in enumerate(fields)])
    class_str += f"    @classmethod\n"
    class_str += f"    def make(cls, iterable):\n"
    class_str += f"        return cls({make_body})\n\n"

    replace_body = "\n".join([f"        {f} = kargs.get('{f}', self.{f})" for f in fields])
    replace_mutable = "\n".join([f"        self.{f} = {f}" for f in fields])
    replace_immutable = ", ".join([f"{f}={f}" for f in fields])

    class_str += f"    def replace(self, **kargs):\n"
    class_str += f"        if self._mutable:\n{replace_body}\n{replace_mutable}\n"
    class_str += f"        else:\n{replace_body}\n"
    class_str += f"            return {typename}({replace_immutable})\n\n"
    class_str += f"    def __setattr__(self, name, value):\n"
    class_str += f"        if not self._mutable and hasattr(self, name):\n"
    class_str += f"            raise AttributeError(f'Cannot modify immutable instance')\n"
    class_str += f"        super().__setattr__(name, value)\n"
    namespace = {}
    exec(class_str, namespace)
    return namespace[typename]


