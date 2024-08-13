"""
1. order matters
2. type and field names MUST begin with letter
3. Field can be a list or a  string
3a. duplicate names should be ignore
4. if names are invalid a SyntaxError should be raised
4a. if any keys in the defaults {} aren't in field_name throw SyntaxError


5. Create a string for an init and create variables for all]
 field names and update default values
  'def __init__(self, x, y=0):\n self.x = x\n self.y = y\n'

6. __repr__ should take values and assign them to variables

7. create get methods for every field_name

8. __getitem__ should return the field name in the right order
9 overload the __eq__ operator so it returns True when two namedtuples come
 from the same type name and same field_valyes

 10 __asdict method returns dictionary of the values


 11. define the __make__ methods to make a new object with
 corresponding values coordinate. make((0,1))

 12.??? __replace__ method that takes **kwargs as parameter come back???

 13. __setattr__ if the mutable parameter is False will raise AttrributeError
"""
class NamedTuple:
    def __init__(self, type_name, field_name, mutable=False, defaults=None):
        self.type_name = type_name
        self.field_name = field_name
        self.mutable = mutable
        self.defaults = defaults if defaults is not None else {}

    def __repr__(self):
        return f"NamedTuple(type_name={self.type_name}, field_name={self.field_name})"

    def __getitem__(self, index):
        if index == 0:
            return self.type_name
        elif index == 1:
            return self.field_name
        raise IndexError("Index out of range")

    def __eq__(self, other):
        if isinstance(other, NamedTuple):
            return self.type_name == other.type_name and self.field_name == other.field_name
        return False

    def __asdict__(self):
        return {"type_name": self.type_name, "field_name": self.field_name}

    def __make__(self, values):
        if len(values) != len(self.field_name):
            raise ValueError("Number of values does not match the number of fields")
        my_dict = {}
        for i in range(len(self.field_name)):
            key = self.field_name[i]
            value = values[i]
            my_dict[key] = value
        return NamedTuple(self.type_name, self.field_name, self.mutable, my_dict)

    def __replace__(self, **kargs):
        if self.mutable:
            for k, v in kargs.items():
                if k in self.defaults:
                    self.defaults[k] = v
        else:
            new_defaults = self.defaults.copy()
            new_defaults.update(kargs)
            return NamedTuple(self.type_name, self.field_name, self.mutable, new_defaults)

    def __setattr__(self, name, value):
        if hasattr(self, 'mutable') and not self.mutable:
            if name in self.__dict__:
                raise AttributeError("Cannot modify because value is immutable")
        super().__setattr__(name, value)

