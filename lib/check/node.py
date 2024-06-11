import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..utils import to_bool, to_int, to_float, to_list_str


DEFAULT_PORT = 8006


async def check_node(
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
    url = f'https://{address}:{port}/api2/json/nodes/{node}/status'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    node = data['data']
    boot = node.get('bootinfo')
    cpu = node.get('cpuinfo')
    k = node.get('current-kernel')
    ksm = node.get('ksm')
    mem = node.get('memory')
    rootfs = node.get('rootfs')
    swap = node.get('swap')
    item = {
        'name': 'node',  # str
        'kversion': node.get('kversion'),  # str
        'pversion': node.get('pversion'),  # str
        'loadavg': [float(v) for v in node['loadavg']] \
            if isinstance(node.get('loadavg'), list) else None,
        'cpu': node.get('cpu'),  # int
        'idle': node.get('idle'),  # int
        'wait': node.get('wait'),  # int
        'uptime': node.get('uptime'),  # int
    }
    state = {
        'node': item,
    }
    if boot is not None:
        state['bootinfo'] = [{
            'name': 'bootinfo',
            'secureboot': to_bool(boot.get('secureboot')),  # bool
            'mode': boot.get('mode'),  # str
        }]
    if cpu is not None:
        state['cpuinfo'] = [{
            'name': 'cpuinfo',
            'cores': cpu.get('cores'),  # int
            'cpus': cpu.get('cpus'),  # int
            # TODO flags metric has many items
            # 'flags': to_list_str(cpu.get('flags'), None),  # liststr
            'hvm': to_int(cpu.get('hvm')),  # int
            'mhz': to_float(cpu.get('mhz')),  # float
            'model': cpu.get('model'),  # str
            'sockets': cpu.get('sockets'),  # int
            'user_hz': cpu.get('user_hz'),  # int
        }]
    if k is not None:
        state['current_kernel'] = [{
            'name': 'current_kernel',
            'machine': k.get('machine'),  # str
            'release': k.get('release'),  # str
            'sysname': k.get('sysname'),  # str
            'version': k.get('version'),  # str
        }]
    if ksm is not None:
        state['ksm'] = [{
            'name': 'ksm',
            'shared': ksm.get('shared'),  # int
        }]
    if mem is not None:
        state['memory'] = [{
            'name': 'memory',
            'free': mem.get('free'),  # int
            'total': mem.get('total'),  # int
            'used': mem.get('used'),  # int
        }]
    if swap is not None:
        state['swap'] = [{
            'name': 'swap',
            'free': swap.get('free'),  # int
            'total': swap.get('total'),  # int
            'used': swap.get('used'),  # int
        }]
    if rootfs is not None:
        state['rootfs'] = [{
            'name': 'rootfs',
            'avail': rootfs.get('avail'),  # int
            'free': rootfs.get('free'),  # int
            'total': rootfs.get('total'),  # int
            'used': rootfs.get('used'),  # int
        }]

    return state
