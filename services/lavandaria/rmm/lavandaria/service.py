import rmm.lavandaria.api_client as st_api
from rmm.lavandaria.schema import DevicesStatusResponse, DeviceStatus


def get_device_status() -> DevicesStatusResponse:
    devices = st_api.get_devices()

    washers = []
    dryers = []

    for device in devices:
        if device["label"].startswith("Máquina de Lavar"):
            washers.append(device)
        elif device["label"].startswith("Máquina de Secar"):
            dryers.append(device)

    washer_status: list[DeviceStatus] = []
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

    dryer_status: list[DeviceStatus] = []
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
