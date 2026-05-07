from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request


class CheckGuests(Check):
    key = 'guests'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/qemu'
        data = await api_request(asset, local_config, config, uri, 'node')

        vm = [{
            'name': str(d['vmid']),  # str
            'vmid': d['vmid'],  # int
            'status': d['status'],  # str
            'vm_name': d.get('name'),  # str
        } for d in data['data']]

        uri = '/lxc'
        data = await api_request(asset, local_config, config, uri, 'node')

        ct = [{
            'name': str(d['vmid']),  # str
            'vmid': d['vmid'],  # int
            'status': d['status'],  # str
            'ct_name': d.get('name'),  # str
        } for d in data['data']]

        return {
            'vm': vm,
            'ct': ct,
        }
