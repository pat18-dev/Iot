from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from datetime import datetime


@dataclass_json
@dataclass(kw_only=True)
class SensorModel:
    sensorid: int
    write_at: datetime
    data: float

    def get_values(self):
        return [self.sensorid, self.write_at, self.data]
