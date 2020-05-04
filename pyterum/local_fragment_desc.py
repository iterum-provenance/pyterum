from __future__ import annotations
from typing import List

from pyterum.metadata import Metadata

class LocalFileDesc:
    def __init__(self, name:str, path:str):
        self.name = name
        self.path = path

    def __str__(self):
        return "{ name: " + self.name + ", path: " + self.path + " }"

    def to_json(self) -> dict:
        return self.__dict__

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls("", "")
        for key in result.__dict__.keys():
            result.__setattr__(key, d[key])
        return result


class LocalFragmentDesc:
    def __init__(self, files:List[LocalFileDesc]):
        self.files = files
        self.metadata = None
    
    def __str__(self):
        result = "{\n"
        result += "" if self.metadata == None else "    metadata: " + str(self.metadata) + "\n"
        result += "    files: ["
        for f in self.files:
            result += "\n        " + str(f)
        result += ("" if len(self.files) == 0 else "\n") + "]\n"
        result += "}"
        return result

    def to_json(self) -> dict:
        result = {}
        for key in self.__dict__.keys():
            result[key] = self.__dict__[key]
        result["files"] = [f.to_json() for f in self.files]
        if self.metadata != None:
            result["metadata"] = self.metadata.to_json()
        return result

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")

        result = cls([])
        result.files = [LocalFileDesc.from_json(f) for f in d["files"]]
        if "metadata" in d:
            result.metadata = Metadata.from_json(d["metadata"])

        return result