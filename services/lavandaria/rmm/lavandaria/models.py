import datetime as dt
from typing import Literal

from rmm_core.api import ResponseModel


class DeviceStatusResponse(ResponseModel):
    label: str
    state: Literal["run", "pause", "stop"]
    completion_time: dt.datetime
    online: bool
    last_seen: dt.datetime

class DevicesStatusResponse(ResponseModel):
    washers: list[DeviceStatusResponse]
    dryers: list[DeviceStatusResponse]
