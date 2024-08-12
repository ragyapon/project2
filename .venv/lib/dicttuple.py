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

    def _contains__(self):
        return k in self.dt
    def __iter__(self):
        pass
    def __eq__(self, other):
        pass

