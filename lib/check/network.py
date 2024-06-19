import aiohttp
from typing import Optional
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..utils import to_bool


DEFAULT_PORT = 8006


async def check_network(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    address = config.get('address')
    if not address:
        address = asset.name
    port = config.get('port', DEFAULT_PORT)
    ssl = config.get('ssl', False)
    node = config.get('node')
    if node is None:
        raise CheckException('invalid config: missing `node`')

    username = asset_config.get('username')
    realm = asset_config.get('realm', 'pam')
    token_id = asset_config.get('token_id')
    token = asset_config.get('secret')
    if None in (username, realm, token_id, token):
        raise CheckException('missing credentials')

    headers = {
        'Authorization': f'PVEAPIToken={username}@{realm}!{token_id}={token}'
    }
    url = f'https://{address}:{port}/api2/json/nodes/{node}/network'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

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
