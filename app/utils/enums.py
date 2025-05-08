
from enum import Enum

class MappedEnumMixin:
    _mapping = {}

    @property
    def dbvalue(self):
        return self._mapping.value[self.value]

    @classmethod
    def from_dbvalue(cls, value):
        for k, v in cls._mapping.value.items():
            if v == value:
                return cls[k]
        raise ValueError(f"Invalid value for enum: {value}")

class AdRewardEnum(MappedEnumMixin, Enum):
    issued = "issued"
    claimed = "claimed"
    expired = "expired"
    _mapping = {
        "issued": "0",
        "claimed": "1",
        "expired": "2"
    }
  