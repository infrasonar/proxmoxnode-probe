from libprobe.asset import Asset
from libprobe.check import Check
from ..utils import to_bool, to_float, to_list_str
from ..helpers import api_request


class CheckStorage(Check):
    key = 'storage'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/storage'
        data = await api_request(asset, local_config, config, uri, 'node')

        storage = [{
            'name': d['storage'],  # str
            'content': to_list_str(d['content']),  # liststr
            'type': d['type'],  # str
            'active': to_bool(d.get('active')),  # bool
            'avail': d.get('avail'),  # int
            'enabled': to_bool(d.get('enabled')),  # bool
            'shared': to_bool(d.get('shared')),  # bool
            'total': d.get('total'),  # int
            'used': d.get('used'),  # int
            'percent_used': to_float(d.get('used_fraction'), 100.0),
        } for d in data['data']]

        return {
            'storage': storage
        }
