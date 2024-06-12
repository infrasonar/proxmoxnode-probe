import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..utils import to_bool, to_list_str


DEFAULT_PORT = 8006


async def check_storage(
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
    url = f'https://{address}:{port}/api2/json/nodes/{node}/storage'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

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
        'percent_used': float(d['used_fraction'] * 100) \
        if isinstance(d.get('used_fraction'), (int, float)) else None,
    } for d in data['data']]
    return {
        'storage': storage
    }
