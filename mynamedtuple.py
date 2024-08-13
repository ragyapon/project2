import keyword

def mynamedtuple(typename, fieldnames, mutable=False, defaults={}):
    # Validate typename
    if not typename.isidentifier() or typename in keyword.kwlist:
        raise SyntaxError(f"Invalid type name: {typename}")

    # Process fieldnames
    if isinstance(fieldnames, str):
        fieldnames = fieldnames.replace(',', ' ').split()
    fieldnames = list(dict.fromkeys(fieldnames))  # Remove duplicates while preserving order

    # Validate fieldnames
    for field in fieldnames:
        if not isinstance(field, str) or not field.isidentifier() or field in keyword.kwlist:
            raise SyntaxError(f"Invalid field name: {field}")

    # Ensure defaults match fieldnames
    for key in defaults:
        if key not in fieldnames:
            raise SyntaxError(f"Invalid default field: {key}")

    # Create class string
    indent = " " * 4
    class_str = f"class {typename}:\n"
    class_str += f"{indent}_fields = {fieldnames}\n"
    class_str += f"{indent}_mutable = {mutable}\n\n"

    # __init__ method
    init_params = ", ".join([f"{field}={defaults.get(field, 'None')}" for field in fieldnames])
    init_body = "\n".join([f"{indent*2}self.{field} = {field}" for field in fieldnames])
    class_str += f"{indent}def __init__(self, {init_params}):\n"
    class_str += f"{init_body}\n\n"

    # __repr__ method
    repr_body = ", ".join([f"{field}={{self.{field}!r}}" for field in fieldnames])
    class_str += f"{indent}def __repr__(self):\n"
    class_str += f"{indent*2}return f'{typename}({repr_body})'\n\n"

    # _asdict method
    class_str += f"{indent}def _asdict(self):\n"
    class_str += f"{indent*2}return {{field: getattr(self, field) for field in self._fields}}\n\n"

    # _replace method
    class_str += f"{indent}def _replace(self, **kwargs):\n"
    class_str += f"{indent*2}if any(key not in self._fields for key in kwargs):\n"
    class_str += f"{indent*3}raise AttributeError('Invalid field name')\n"
    class_str += f"{indent*2}if not self._mutable:\n"
    class_str += f"{indent*3}new_values = {{f: getattr(self, f) for f in self._fields}}\n"
    class_str += f"{indent*3}new_values.update(kwargs)\n"
    class_str += f"{indent*3}return self.__class__(**new_values)\n"
    class_str += f"{indent*2}else:\n"
    class_str += f"{indent*3}for key, value in kwargs.items():\n"
    class_str += f"{indent*4}if key not in self._fields:\n"
    class_str += f"{indent*5}raise AttributeError('Invalid field name')\n"
    class_str += f"{indent*4}setattr(self, key, value)\n"
    class_str += f"{indent*3}return None\n\n"

    # __getitem__ method (indexing)
    class_str += f"{indent}def __getitem__(self, index):\n"
    class_str += f"{indent*2}if not isinstance(index, int) or not (0 <= index < len(self._fields)):\n"
    class_str += f"{indent*3}raise IndexError('Index out of range')\n"
    class_str += f"{indent*2}return getattr(self, self._fields[index])\n\n"

    # __eq__ method
    class_str += f"{indent}def __eq__(self, other):\n"
    class_str += f"{indent*2}if not isinstance(other, self.__class__):\n"
    class_str += f"{indent*3}return False\n"
    class_str += f"{indent*2}return all(getattr(self, f) == getattr(other, f) for f in self._fields)\n\n"

    # _make method (for creating an instance from an iterable)
    class_str += f"{indent}@classmethod\n"
    class_str += f"{indent}def _make(cls, iterable):\n"
    class_str += f"{indent*2}return cls(*iterable)\n\n"

    # __setattr__ method (for immutability enforcement)
    class_str += f"{indent}def __setattr__(self, name, value):\n"
    class_str += f"{indent*2}if name in self._fields and not self._mutable:\n"
    class_str += f"{indent*3}raise AttributeError('Cannot modify immutable instance')\n"
    class_str += f"{indent*2}super().__setattr__(name, value)\n"

    # Execute the class definition
    namespace = {}
    exec(class_str, namespace)
    return namespace[typename]


