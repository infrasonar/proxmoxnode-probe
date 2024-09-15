from typing import Optional, List


def to_bool(val: Optional[int]) -> Optional[bool]:
    if val is None:
        return
    return bool(val)


def to_int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return
    return int(val)


def to_float(val: Optional[str], multiply: float = 1.0) -> Optional[float]:
    if val is None:
        return
    return float(val) * multiply


def to_list_str(val: Optional[str], s: str = ',') -> Optional[List[str]]:
    if val is None or not isinstance(val, str):
        return
    return val.split(s)


def to_percent_used(total: Optional[int], used: Optional[int]
                    ) -> Optional[float]:
    if used is None or total is None or total <= 0:
        return
    return used / total * 100
