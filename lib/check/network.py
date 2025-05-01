from libprobe.asset import Asset
from ..utils import to_bool
from ..helpers import api_request


async def check_network(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:

    uri = '/network'
    data = await api_request(asset, asset_config, config, uri, 'node')

    network = [{
        'name': d['iface'],  # str
        'active': to_bool(d.get('active')),  # bool/optional
        'address': d.get('address'),  # str/optional
        'autostart': to_bool(d.get('autostart')),  # int/optional
        'bridge_fd': d.get('bridge_fd'),  # str/optional
        'bridge_ports': d.get('bridge_ports'),  # str/ optional
        'bridge_stp': d.get('bridge_stp'),  # str/optional
        'cdir': d.get('cdir'),  # str/optional
        'exists': to_bool(d.get('exists')),  # int/optional
        'families': d.get('families'),  # liststr/optional
        'gateway': d.get('gateway'),  # str/optional
        'method': d.get('method'),  # str
        'method6': d.get('method6'),  # str
        'netmask': d.get('netmask'),  # str/optional
        'priority': d.get('priority'),  # int
        'type': d.get('type'),  # str
    } for d in data['data']]

    return {
        'network': network
    }
