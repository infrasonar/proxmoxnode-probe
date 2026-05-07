def to_bool(val: int | None) -> bool | None:
    if val is None:
        return
    return bool(val)


def to_int(val: str | None) -> int | None:
    if val is None:
        return
    return int(val)


def to_float(val: str | None, multiply: float = 1.0) -> float | None:
    if val is None:
        return
    return float(val) * multiply


def to_list_str(val: str | None, s: str = ',') -> list[str] | None:
    if val is None or not isinstance(val, str):
        return
    return val.split(s)


def to_percent_used(total: int | None, used: int | None) -> float | None:
    if used is None or total is None or total <= 0:
        return
    return used / total * 100
