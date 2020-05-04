from __future__ import annotations
from typing import Dict

class Metadata:
    def __init__(self, output_channel:str=None, custom:Dict[str, str]=None):
        self.output_channel = output_channel
        self.custom = custom
    
    def __str__(self):
        return str(self.__dict__)

    def to_json(self) -> dict:
        return self.__dict__

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls()
        for key in d.keys():
            result.__setattr__(key, d[key])

        return result