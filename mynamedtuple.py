 #
 # def namedtuple(typename):
 #    def __init__(self, type_name, field_name, mutable=False, defaults=None):
 #        self.type_name = type_name
 #        self.field_name = field_name
 #        self.mutable = mutable
 #        self.defaults = defaults if defaults is not None else {}
 #
 #    def __repr__(self):
 #        return f"NamedTuple(type_name={self.type_name}, field_name={self.field_name})"
 #
 #    def __getitem__(self, index):
 #        if index == 0:
 #            return self.type_name
 #        elif index == 1:
 #            return self.field_name
 #        raise IndexError("Index out of range")
 #
 #    def __eq__(self, other):
 #        if isinstance(other, NamedTuple):
 #            return self.type_name == other.type_name and self.field_name == other.field_name
 #        return False
 #
 #    def __asdict__(self):
 #        return {"type_name": self.type_name, "field_name": self.field_name}
 #
 #    def __make__(self, values):
 #        if len(values) != len(self.field_name):
 #            raise ValueError("Number of values does not match the number of fields")
 #        my_dict = {}
 #        for i in range(len(self.field_name)):
 #            key = self.field_name[i]
 #            value = values[i]
 #            my_dict[key] = value
 #        return NamedTuple(self.type_name, self.field_name, self.mutable, my_dict)
 #
 #    def __replace__(self, **kargs):
 #        if self.mutable:
 #            for k, v in kargs.items():
 #                if k in self.defaults:
 #                    self.defaults[k] = v
 #        else:
 #            new_defaults = self.defaults.copy()
 #            new_defaults.update(kargs)
 #            return NamedTuple(self.type_name, self.field_name, self.mutable, new_defaults)
 #
 #    def __setattr__(self, name, value):
 #        if hasattr(self, 'mutable') and not self.mutable:
 #            if name in self.__dict__:
 #                raise AttributeError("Cannot modify because value is immutable")
 #        super().__setattr__(name, value)
from typing import List, Dict, Any, Union

def mynamedtuple(type_name: str, field_name: List[str], mutable: bool = False, defaults: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a namedtuple-like dictionary."""
    if defaults is None:
        defaults = {}
    return {
        'type_name': type_name,
        'field_name': field_name,
        'mutable': mutable,
        'defaults': defaults
    }

def __repr__(namedtuple: Dict[str, Any]) -> str:
    """Return a string representation of the namedtuple."""
    return f"NamedTuple(type_name={namedtuple['type_name']}, field_name={namedtuple['field_name']})"

def __getitem__(namedtuple: Dict[str, Any], index: int) -> Any:
    """Get an item by index."""
    if index == 0:
        return namedtuple['type_name']
    elif index == 1:
        return namedtuple['field_name']
    raise IndexError("Index out of range")

def __eq__(namedtuple1: Dict[str, Any], namedtuple2: Dict[str, Any]) -> bool:
    """Check if two namedtuples are equal."""
    return (namedtuple1['type_name'] == namedtuple2['type_name'] and
            namedtuple1['field_name'] == namedtuple2['field_name'])

def asdict_namedtuple(namedtuple: Dict[str, Any]) -> Dict[str, Any]:
    """Convert namedtuple to a dictionary."""
    return {
        "type_name": namedtuple['type_name'],
        "field_name": namedtuple['field_name']
    }

def make_namedtuple(namedtuple: Dict[str, Any], values: List[Any]) -> Dict[str, Any]:
    """Create a new namedtuple with the given values."""
    if len(values) != len(namedtuple['field_name']):
        raise ValueError("Number of values does not match the number of fields")
    new_defaults = dict(zip(namedtuple['field_name'], values))
    return create_namedtuple(namedtuple['type_name'], namedtuple['field_name'], namedtuple['mutable'], new_defaults)

def replace_namedtuple(namedtuple: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Replace fields in the namedtuple and return a new namedtuple."""
    if namedtuple['mutable']:
        for k, v in kwargs.items():
            if k in namedtuple['defaults']:
                namedtuple['defaults'][k] = v
        return namedtuple
    else:
        new_defaults = namedtuple['defaults'].copy()
        new_defaults.update(kwargs)
        return create_namedtuple(namedtuple['type_name'], namedtuple['field_name'], namedtuple['mutable'], new_defaults)

def set_attr_namedtuple(namedtuple: Dict[str, Any], name: str, value: Any) -> None:
    """Set an attribute if mutable."""
    if not namedtuple['mutable'] and name in namedtuple:
        raise AttributeError("Cannot modify because value is immutable")
    namedtuple[name] = value

