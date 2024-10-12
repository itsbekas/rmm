from pydantic.dataclasses import dataclass


@dataclass
class DeviceStatus:
    label: str
    status: str
    completionTime: str
    healthStatus: str
    healthUpdated: str


@dataclass
class DevicesStatusResponse:
    washers: list[DeviceStatus]
    dryers: list[DeviceStatus]
