import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException


DEFAULT_PORT = 8006


async def check_guests(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    address = config.get('address')
    if not address:
        address = asset.name
    port = config.get('port', DEFAULT_PORT)
    node = config.get('node')  # TODOK DEFAULT_NODE "pve"?
    if node is None:
        raise CheckException('invalid config: missing `node`')

    username = asset_config.get('username')
    realm = asset_config.get('realm')
    token_id = asset_config.get('token_id')
    token = asset_config.get('token')
    if None in (username, realm, token_id, token):
        raise CheckException('missing credentials')

    headers = {
        'Authorization': f'PVEAPIToken={username}@{realm}!{token_id}={token}'
    }
    url = f'https://{address}:{port}/api2/json/nodes/{node}/qemu'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as resp:
            resp.raise_for_status()
            data = await resp.json()

    guests = [{
        'name': str(d['vmid']),
        'status': d['status'],
        'vmid': d['vmid'],
        'cpu': d.get('cpu'),
        'cpus': d.get('cpus'),
        'disk': d.get('disk'),
        'diskread': d.get('diskread'),
        'diskwrite': d.get('diskwrite'),
        'maxdisk': d.get('maxdisk'),
        'maxmem': d.get('maxmem'),
        'mem': d.get('mem'),
        'netin': d.get('netin'),
        'netout': d.get('netout'),
        'pid': d.get('pid'),
        'uptime': d.get('uptime'),
        'vm_name': d.get('name'),
    } for d in data['data']]
    return {
        'guests': guests
    }
