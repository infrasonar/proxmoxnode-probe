import logging
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, NoCountException


async def check_xxx(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    address = config.get('address')
    if not address:
        address = asset.name

    result = None

    return result
