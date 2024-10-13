from rmm.lavandaria.schema import DeviceStatus, Fetches  # noqa
from rmm_core.db import create_tables


def run():
    create_tables()


if __name__ == "__main__":
    run()
