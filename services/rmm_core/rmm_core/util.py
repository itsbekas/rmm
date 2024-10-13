import os

def get_env(key: str, val_type: type | None = None) -> str | int:
    val: str | None = os.getenv(key)
    if val is None:
        raise ValueError(f"{key} is not set")
    else:
        clean_val: str = val
        if val_type is not None:
            try:
                clean_val = val_type(val)
            except ValueError:
                raise ValueError(f"{key} must be of type {val_type}")
        return clean_val
