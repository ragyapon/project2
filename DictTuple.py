"""
1. Define a class called DictTuple

2. defined an __init__ method that takes one parameter
3.
"""

class DictTuple:
    def __init__(self,*args):
        self.dt = args
    def __len__(self):
        key_counter = 0
        for key in self.dt:
            key_counter += len(key.keys())
        return key_counter
    def __bool__(self):
        if len(self.dt) == 1:
            return False
        else:
            return True
    def __repr__(self):
        return 'DictTuple({})'.format(','.join(str(d) for d in self.dt))

    def __contains__(self,k):
        return k in self.dt
    def __getitem__(self, k):
        for d in reversed(self.dt):
            if k in d:
                return d[k]
            else:
                return KeyError("Key not found")
    def __setitem__(self, k, v):
        for d in reversed(self.dt):
            if k in d:
                d[k] = v
                return
            self.dt[-1][k]=v
    def __delitem__(self, k):
        for d in self.dt:
            if k in d:
                del d[k]
            else:
                raise KeyError("Key not found in any dictionary")
    def __call__(self, k):
        return [d[k] for d in self.dt if k in d]

    def __iter__(self):
        latest_index ={}
        for index in range(len(self.dt)):
            d = self.dt[index]
            for key in d:
                latest_index[key] = index
        new_keys = sorted(latest_index.keys())
        for key in new_keys:
            yield key
    def __eq__(self, other):
        self_keys = set(self.__iter__())

        if isinstance(other, dict):
            other_keys = set(other.keys())
            if self_keys != other_keys:
                return False

            for key in self_keys:
                if self[key] != other[key]:
                    return False
            return True

        elif isinstance(other, DictTuple):
            other_keys = set(other.__iter__())
            if self_keys != other_keys:
                return False

            for key in self_keys:
                if self[key] != other[key]:
                    return False
            return True

        return False
    def __add__(self, other):
        if isinstance(other, DictTuple):
            return DictTuple(*(self.dt + other.dt))
        elif isinstance(other,dict):
            return DictTuple(*(self.dicts + [other]))
        elif isinstance(self,dict):
            return DictTuple(other,*self.dicts)
        raise TypeError ("Type is not supported")
    def __setattr__(self, key, value):
        pass

