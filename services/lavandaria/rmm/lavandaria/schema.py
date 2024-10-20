import datetime as dt

from rmm_core.db import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class DeviceStatus(BaseModel):
    __tablename__ = "device_status"

    label: Mapped[str] = mapped_column(String(64), primary_key=True)
    state: Mapped[str] = mapped_column(String(8))
    completion_time: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)
    online: Mapped[bool] = mapped_column()
    last_seen: Mapped[dt.datetime] = mapped_column(default=dt.datetime(1970, 1, 1))


class Fetches(BaseModel):
    __tablename__ = "fetches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_updated: Mapped[str] = mapped_column(String(64))
