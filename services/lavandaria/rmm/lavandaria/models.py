from pydantic.dataclasses import dataclass


@dataclass
class DeviceStatusResponse:
    label: str
    status: str
    completionTime: str
    healthStatus: str
    healthUpdated: str


@dataclass
class DevicesStatusResponse:
    washers: list[DeviceStatusResponse]
    dryers: list[DeviceStatusResponse]
