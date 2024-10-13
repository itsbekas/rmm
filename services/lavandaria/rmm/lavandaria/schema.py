from rmm_core.db import BaseModel
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class DeviceStatus(BaseModel):
    __tablename__ = "device_status"

    label: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(8))
    completionTime: Mapped[str] = mapped_column(String(64))
    healthStatus: Mapped[str] = mapped_column(String(8))
    healthUpdated: Mapped[str] = mapped_column(String(64))


class Fetches(BaseModel):
    __tablename__ = "fetches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastUpdated: Mapped[str] = mapped_column(String(64))
