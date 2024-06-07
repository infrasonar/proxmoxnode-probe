import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException


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
    realm = asset_config.get('realm')
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
        'name': d['iface'],
        'active': d.get('active'),  # optional
        'address': d.get('address'),  # optional
        'autostart': d.get('autostart'),  # optional
        'bridge_fd': d.get('bridge_fd'),  # optional
        'bridge_ports': d.get('bridge_ports'),  # optional
        'bridge_stp': d.get('bridge_stp'),  # optional
        'cdir': d.get('cdir'),  # optional
        'exists': d.get('exists'),  # optional
        'families': d.get('families'),
        'gateway': d.get('gateway'),  # optional
        'method': d.get('method'),
        'method6': d.get('method6'),
        'netmask': d.get('netmask'),  # optional
        'priority': d.get('priority'),
        'type': d.get('type'),

    } for d in data['data']]
    return {
        'network': network
    }
