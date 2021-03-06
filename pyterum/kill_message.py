from __future__ import annotations

# Message indicating that no more messages will be produced/received
# This indicates: Stop when you are ready to stop
class KillMessage:
    def __init__(self):
        self.status = "complete"
    
    def to_json(self) -> dict:
        return self.__dict__

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls()
        for key in result.__dict__.keys():
            result.__setattr__(key, d[key])
        return result