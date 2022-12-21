from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from datetime import datetime


@dataclass_json
@dataclass(kw_only=True)
class SensorModel:
   sensorid: str
   write_at: datetime
   value: float 