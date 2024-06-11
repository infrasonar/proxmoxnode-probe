from typing import Optional, List


def to_bool(val: Optional[int]) -> bool:
    if val is None:
        return
    return bool(val)


def to_list_str(val: Optional[str]) -> List[str]:
    if val is None or not isinstance(val, str):
        return
    return val.split(',')
