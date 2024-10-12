from os import getenv

import requests

ST_TOKEN = getenv("SMART_THINGS_TOKEN")

if ST_TOKEN is None:
    print("SMART_THINGS_TOKEN is not set")
    exit(1)

HEADERS = {"Authorization": f"Bearer {ST_TOKEN}"}
BASE_URL = "https://api.smartthings.com/v1"


def get_devices():
    res = requests.get(f"{BASE_URL}/devices", headers=HEADERS)
    return res.json().get("items", [])


def get_device_health(device_id):
    res = requests.get(f"{BASE_URL}/devices/{device_id}/health", headers=HEADERS)
    return res.json()


def get_washer_status(device_id):
    res = requests.get(
        f"{BASE_URL}/devices/{device_id}/components/main/capabilities/washerOperatingState/status",
        headers=HEADERS,
    )
    return res.json()


def get_dryer_status(device_id):
    res = requests.get(
        f"{BASE_URL}/devices/{device_id}/components/main/capabilities/dryerOperatingState/status",
        headers=HEADERS,
    )
    return res.json()
