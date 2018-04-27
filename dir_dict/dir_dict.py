import os
import json
from collections.abc import MutableMapping


class DirDict(MutableMapping):
    def __init__(self, diectory):
        self._diectory = diectory

    def __setitem__(self, key, value):
        with open(str(self._diectory)+"\\"+str(key)+".json",'w') as file:
            json.dump(value,file)

    def __getitem__(self, item):
            if os.path.isfile((str(self._diectory)+"\\"+str(item)+".json")):
                data=json.load(open(str(self._diectory)+"\\"+str(item)+".json"))
                return data

    def __delitem__(self, key):
        if os.path.isfile((str(self._diectory) + "\\" + str(key) + ".json")):
            value=self.__getitem__(key)
            os.remove(str(self._diectory)+"\\"+str(key)+".json")
            return value

    def __len__(self):
        return len([name for name in os.listdir(str(self._diectory))
                    if (os.path.isfile(os.path.join(str(self._diectory), name)) and name.split(".")[1]=="json")])

    def __iter__(self):
        for name in os.listdir(str(self._diectory)):
            yield (self.__getitem__(name.split(".")[1]),name.split(".")[1])



