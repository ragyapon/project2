import keyword


def mynamedtuple(typename, fields, defaults=None, mutable=False):
    # Validate typename
    if not typename.isidentifier() or typename in keyword.kwlist:
        raise SyntaxError(f"Invalid type name: '{typename}'")

    # Validate and process fields
    if isinstance(fields, str):
        fields = fields.replace(',', ' ').split()
    fields = list(dict.fromkeys(fields))  # Remove duplicates

    if any(not field.isidentifier() or field in keyword.kwlist for field in fields):
        raise SyntaxError(f"Invalid field names in: {fields}")

    # Validate defaults
    if defaults is None:
        defaults = {}
    else:
        invalid_defaults = set(defaults) - set(fields)
        if invalid_defaults:
            raise SyntaxError(f"Invalid defaults for fields: {invalid_defaults}")

    # Generate class string
    indent = " " * 4  # Four spaces for indentation
    class_str = f"class {typename}:\n"
    class_str += f"{indent}_fields = {fields}\n"
    class_str += f"{indent}_mutable = {mutable}\n\n"

    # Generate __init__ method
    params = ", ".join([f"{f}={defaults[f]}" if f in defaults else f for f in fields])
    init_body = "\n".join([f"{indent * 2}self.{f} = {f}" for f in fields])
    class_str += f"{indent}def __init__(self, {params}):\n{init_body}\n\n"

    # Generate __repr__ method
    repr_body = ", ".join([f"{f}={{self.{f}!r}}" for f in fields])
    class_str += f"{indent}def __repr__(self):\n"
    class_str += f"{indent * 2}return f'{typename}({repr_body})'\n\n"

    # Generate accessors
    for field in fields:
        class_str += f"{indent}def get_{field}(self):\n"
        class_str += f"{indent * 2}return self.{field}\n\n"

    # Generate __eq__ method
    eq_body = " and ".join([f"self.{f} == other.{f}" for f in fields])
    class_str += f"{indent}def __eq__(self, other):\n"
    class_str += f"{indent * 2}return isinstance(other, {typename}) and {eq_body}\n\n"

    # Generate __getitem__ method
    getitem_body = "\n".join([f"{indent * 2}if index == {i}: return self.{f}" for i, f in enumerate(fields)])
    class_str += f"{indent}def __getitem__(self, index):\n{getitem_body}\n"
    class_str += f"{indent * 2}raise IndexError('Index out of range')\n\n"

    # Generate asdict method
    asdict_body = ", ".join([f"'{f}': self.{f}" for f in fields])
    class_str += f"{indent}def asdict(self):\n"
    class_str += f"{indent * 2}return {{{asdict_body}}}\n\n"

    # Generate make method
    make_body = ", ".join([f"iterable[{i}]" for i, _ in enumerate(fields)])
    class_str += f"{indent}@classmethod\n"
    class_str += f"{indent}def make(cls, iterable):\n"
    class_str += f"{indent * 2}return cls({make_body})\n\n"

    # Generate replace method
    replace_body = "\n".join([f"{indent * 2}{f} = kargs.get('{f}', self.{f})" for f in fields])
    replace_mutable = "\n".join([f"{indent * 2}self.{f} = {f}" for f in fields])
    replace_immutable = ", ".join([f"{f}={f}" for f in fields])

    class_str += f"{indent}def replace(self, **kargs):\n"
    class_str += f"{indent * 2}if self._mutable:\n{replace_body}\n{replace_mutable}\n"
    class_str += f"{indent * 2}else:\n{replace_body}\n"
    class_str += f"{indent * 3}return {typename}({replace_immutable})\n\n"

    # Generate setattr method
    class_str += f"{indent}def __setattr__(self, name, value):\n"
    class_str += f"{indent * 2}if not self._mutable and hasattr(self, name):\n"
    class_str += f"{indent * 3}raise AttributeError(f'Cannot modify immutable instance')\n"
    class_str += f"{indent * 2}super().__setattr__(name, value)\n"

    # Compile the class and return it
    namespace = {}
    exec(class_str, namespace)
    return namespace[typename]


