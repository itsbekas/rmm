import datetime as dt

from rmm_core.db import Session

import rmm.lavandaria.api_client as st_api
from rmm.lavandaria.models import DevicesStatusResponse, DeviceStatusResponse
from rmm.lavandaria.schema import DeviceStatus, Fetches


def get_device_status() -> DevicesStatusResponse:
    devices = st_api.get_devices()

    washers = []
    dryers = []

    for device in devices:
        if device["label"].startswith("Máquina de Lavar"):
            washers.append(device)
        elif device["label"].startswith("Máquina de Secar"):
            dryers.append(device)

    washer_status: list[DeviceStatusResponse] = []
    for washer in washers:
        status = st_api.get_washer_status(washer["deviceId"])
        health = st_api.get_device_health(washer["deviceId"])
        washer_status.append(
            {
                "label": washer["label"],
                "status": status.get("machineState").get("value"),
                "completionTime": status.get("completionTime").get("value"),
                "healthStatus": health.get("state"),
                "healthUpdated": health.get("lastUpdatedDate"),
            }
        )

    dryer_status: list[DeviceStatusResponse] = []
    for dryer in dryers:
        status = st_api.get_dryer_status(dryer["deviceId"])
        health = st_api.get_device_health(dryer["deviceId"])
        dryer_status.append(
            {
                "label": dryer["label"],
                "status": status.get("machineState").get("value"),
                "completionTime": status.get("completionTime").get("value"),
                "healthStatus": health.get("state"),
                "healthUpdated": health.get("lastUpdatedDate"),
            }
        )

    washer_status.sort(key=lambda x: x["label"])
    dryer_status.sort(key=lambda x: x["label"])

    return {"washers": washer_status, "dryers": dryer_status}


# similar to get_device_status, but stores the status in the redis database
def fetch_device_status():
    status = get_device_status()
    with Session() as session:
        for device in status["washers"] + status["dryers"]:
            db_device = (
                session.query(DeviceStatus)
                .filter(DeviceStatus.label == device["label"])
                .first()
            )
            if db_device:
                db_device.status = device["status"]
                db_device.completionTime = device["completionTime"]
                db_device.healthStatus = device["healthStatus"]
                db_device.healthUpdated = device["healthUpdated"]
            else:
                session.add(DeviceStatus(**device))

        db_fetches = session.query(Fetches).first()
        if db_fetches:
            db_fetches.lastUpdated = dt.datetime.now().isoformat()
        else:
            session.add(Fetches(lastUpdated=dt.datetime.now().isoformat()))

        session.commit()
    return status


def get_latest_device_status() -> DevicesStatusResponse:
    with Session() as session:
        devices = session.query(DeviceStatus).all()

        devices_dict = [
            {
                "label": device.label,
                "status": device.status,
                "completionTime": device.completionTime,
                "healthStatus": device.healthStatus,
                "healthUpdated": device.healthUpdated,
            }
            for device in devices
        ]

        washers = [
            device
            for device in devices_dict
            if device["label"].startswith("Máquina de Lavar")
        ]
        dryers = [
            device
            for device in devices_dict
            if device["label"].startswith("Máquina de Secar")
        ]

        washers.sort(key=lambda x: x["label"])
        dryers.sort(key=lambda x: x["label"])

    return {"washers": washers, "dryers": dryers}
