import datetime as dt

from rmm_core.db import Session

import rmm.lavandaria.api_client as st_api
from rmm.lavandaria.models import DevicesStatusResponse, DeviceStatusResponse
from rmm.lavandaria.schema import DeviceStatus, Fetches


def fetch_device_status() -> None:
    """
    Fetches the device status from the API and stores it in the database.
    """
    devices = st_api.get_devices()

    status = DevicesStatusResponse(washers=[], dryers=[])

    for device in devices:
        if device["label"].startswith("Máquina de Lavar"):
            device_status = st_api.get_washer_status(device["deviceId"])
            health = st_api.get_device_health(device["deviceId"])
        elif device["label"].startswith("Máquina de Secar"):
            device_status = st_api.get_dryer_status(device["deviceId"])
            health = st_api.get_device_health(device["deviceId"])
        
        label: str = device["label"]
        state: str = device_status.get("machineState").get("value")
        completion_time: dt.datetime = dt.datetime.fromisoformat(
            device_status.get("completionTime").get("value")
        )
        online: bool = health.get("state") == "online"
        # If the device is offline, the last seen time is not available
        # We use 1970-01-01 as a placeholder, which is overwritten later
        last_seen: dt.datetime = dt.datetime.now if online else dt.datetime(1970, 1, 1)

        res = DeviceStatusResponse(
            label=label,
            state=state,
            completionTime=completion_time,
            online=online,
            lastSeen=last_seen,
        )

        if label.startswith("Máquina de Lavar"):
            status.washers.append(res)
        elif label.startswith("Máquina de Secar"):
            status.dryers.append(res)

    status.washers.sort(key=lambda x: x.label)
    status.dryers.sort(key=lambda x: x.label)

    with Session() as session:
        for device in status.washers + status.dryers:
            db_device = (
                session.query(DeviceStatus)
                .filter(DeviceStatus.label == device.label)
                .first()
            )
            # If the device is already in the database, update its status
            # Otherwise, add it to the database
            if db_device:
                db_device.state = device.state
                db_device.completion_time = device.completion_time
                db_device.online = device.online
                if device.online:
                    db_device.last_seen = device.last_seen
            else:
                session.add(DeviceStatus(**device.dict()))

        db_fetches = session.query(Fetches).first()
        if db_fetches:
            db_fetches.last_updated = dt.datetime.now().isoformat()
        else:
            session.add(Fetches(last_updated=dt.datetime.now().isoformat()))

        session.commit()


def get_latest_device_status() -> DevicesStatusResponse:
    with Session() as session:
        devices = [
            DeviceStatusResponse(
                label=device.label,
                state=device.state,
                completion_time=device.completion_time,
                online=device.online,
                last_seen=device.last_seen,
            )
            for device in session.query(DeviceStatus).all()
        ]

        washers = [
            device
            for device in devices
            if device.label.startswith("Máquina de Lavar")
        ]
        dryers = [
            device
            for device in devices
            if device.label.startswith("Máquina de Secar")
        ]

        washers.sort(key=lambda x: x.label)
        dryers.sort(key=lambda x: x.label)

    return {"washers": washers, "dryers": dryers}
