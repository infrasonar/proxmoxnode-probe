from libprobe.asset import Asset
from ..helpers import api_request


async def check_guests(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:

    uri = '/qemu'
    data = await api_request(asset, asset_config, config, uri, 'node')

    vm = [{
        'name': str(d['vmid']),  # str
        'status': d['status'],  # str
        'vm_name': d.get('name'),  # str
    } for d in data['data']]

    uri = '/lxc'
    data = await api_request(asset, asset_config, config, uri, 'node')

    ct = [{
        'name': str(d['vmid']),  # str
        'status': d['status'],  # str
        'vm_name': d.get('name'),  # str
    } for d in data['data']]

    return {
        'vm': vm,
        'ct': ct,
    }
