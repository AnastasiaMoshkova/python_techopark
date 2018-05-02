import os
from collections.abc import MutableMapping


class DirDict(MutableMapping):
    def __init__(self, diectory):
        self._diectory = diectory

    def __setitem__(self, key, value):
        file=open(os.path.join(self._diectory, key), 'w')
        file.write(value)

    def __getitem__(self, item):
            if os.path.isfile(os.path.join(self._diectory, item)):
                data = open(os.path.join(self._diectory, item), 'r')
                return data.read()

    def __delitem__(self, key):
        print("delitem")
        if os.path.isfile(os.path.join(self._diectory, key)):
            value = self[key]
            os.remove(os.path.join(self._diectory, key))
            return value

    def __len__(self):
        return len([name for name in os.listdir(self._diectory)
                    if os.path.isfile(os.path.join(self._diectory, name))])

    def __iter__(self):
        for name in os.listdir(self._diectory):
            yield (self[name], name)





