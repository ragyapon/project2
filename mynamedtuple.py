from typing import List, Dict, Any


def mynamedtuple(type_name: str, field_name: List[str], mutable: bool = False, defaults: Dict[str, Any] = None) -> Dict[str, Any]:
    if defaults is None:
        defaults = {}
    return {
        'type_name': type_name,
        'field_name': field_name,
        'mutable': mutable,
        'defaults': defaults
    }
def __repr__(namedtuple: Dict[str, Any]) -> str:
    return f"NamedTuple(type_name={namedtuple['type_name']}, field_name={namedtuple['field_name']})"

def __getitem__(namedtuple: Dict[str, Any], index: int) -> Any:
    if index == 0:
        return namedtuple['type_name']
    elif index == 1:
        return namedtuple['field_name']
    raise IndexError("Index out of range")

def __eq__(namedtuple1: Dict[str, Any], namedtuple2: Dict[str, Any]) -> bool:
    """Check if two namedtuples are equal."""
    return (namedtuple1['type_name'] == namedtuple2['type_name'] and
            namedtuple1['field_name'] == namedtuple2['field_name'])

def __asdict__(namedtuple: Dict[str, Any]) -> Dict[str, Any]:
    """Convert namedtuple to a dictionary."""
    return {
        "type_name": namedtuple['type_name'],
        "field_name": namedtuple['field_name']
    }

def __make__(namedtuple: Dict[str, Any], values: List[Any]) -> Dict[str, Any]:
    """Create a new namedtuple with the given values."""
    if len(values) != len(namedtuple['field_name']):
        raise ValueError("Number of values does not match the number of fields")
    new_defaults = dict(zip(namedtuple['field_name'], values))
    return mynamedtuple(namedtuple['type_name'], namedtuple['field_name'], namedtuple['mutable'], new_defaults)

def __replace__(namedtuple: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Replace fields in the namedtuple and return a new namedtuple."""
    if namedtuple['mutable']:
        for k, v in kwargs.items():
            if k in namedtuple['defaults']:
                namedtuple['defaults'][k] = v
        return namedtuple
    else:
        new_defaults = namedtuple['defaults'].copy()
        new_defaults.update(kwargs)
        return mynamedtuple(namedtuple['type_name'], namedtuple['field_name'], namedtuple['mutable'], new_defaults)

def __setattr__(namedtuple: Dict[str, Any], name: str, value: Any) -> None:
    """Set an attribute if mutable."""
    if not namedtuple['mutable'] and name in namedtuple:
        raise AttributeError("Cannot modify because value is immutable")
    namedtuple[name] = value

