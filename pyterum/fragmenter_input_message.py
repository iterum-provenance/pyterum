from __future__ import annotations
from typing import List
import json

from pyterum.local_fragment_desc import LocalFileDesc

# Input message that a fragmenter receives.
class FragmenterInputMessage:
    def __init__(self, data_files:List[str]):
        self.data_files = data_files
    
    def __str__(self):
        return str(self.to_json())

    def to_json(self) -> dict:
        result = {}
        result["data_files"] = self.data_files
        return result

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls([])
        result.data_files = d["data_files"]

        return result