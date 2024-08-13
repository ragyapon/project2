class DictTuple:
    def __init__(self, *dt):
        self.dt = dt

    def __len__(self):
        key_counter = 0
        for key in self.dt:
            key_counter += len(key.keys())
        return key_counter

    def __bool__(self):
        return len(self.dt) > 1

    def __repr__(self):
        return 'DictTuple({})'.format(', '.join(str(d) for d in self.dt))

    def __contains__(self, k):
        return any(k in d for d in self.dt)

    def __getitem__(self, k):
        for d in reversed(self.dt):
            if k in d:
                return d[k]
        raise KeyError("Key not found")

    def __setitem__(self, k, v):
        for d in reversed(self.dt):
            if k in d:
                d[k] = v
                return
        self.dt[-1][k] = v

    def __delitem__(self, k):
        for d in self.dt:
            if k in d:
                del d[k]
                return
        raise KeyError("Key not found in any dictionary")

    def __call__(self, k):
        return [d[k] for d in self.dt if k in d]

    def __iter__(self):
        latest_index = {}
        for index, d in enumerate(self.dt):
            if not isinstance(d, dict):
                raise TypeError("wrong type")
            for key in d:
                latest_index[key] = index
        new_keys = sorted(latest_index.keys())
        for key in new_keys:
            yield key


    def __eq__(self, other):
        if isinstance(other, DictTuple):
            self_keys = set(self.__iter__())
            other_keys = set(other.__iter__())
            if self_keys != other_keys:
                return False
            return all(self[key] == other[key] for key in self_keys)
        elif isinstance(other, dict):
            self_keys = set(self.__iter__())
            other_keys = set(other.keys())
            if self_keys != other_keys:
                return False
            return all(self[key] == other[key] for key in self_keys)
        return False

    def __add__(self, other):
        if isinstance(other, DictTuple):
            return DictTuple(*(self.dt + other.dt))
        elif isinstance(other, dict):
            return DictTuple(*(self.dt + [other]))
        else:
            raise TypeError("Unsupported type for addition")

    def __setattr__(self, key, value):
        if hasattr(self, '_mutable') and not self._mutable:
            raise AttributeError("Cannot modify because instance is immutable")
        super().__setattr__(key, value)
