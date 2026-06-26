from libprobe.asset import Asset
from libprobe.check import Check
from ..utils import to_bool
from ..helpers import api_request


class CheckServices(Check):
    key = 'services'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        uri = '/services'
        data = await api_request(asset, local_config, config, uri, 'node')

        services = [{
            'name': d['name'],  # str
            'desc': d.get('desc'),  # str
            'service': d.get('service'),  # str
            'state': d.get('state'),  # str
            'active_state': d.get('active-state'),  # str
            'unit_state': d.get('unit-state'),  # str
        } for d in data['data']]

        return {
            'services': services
        }
