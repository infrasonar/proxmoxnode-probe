from libprobe.asset import Asset
from ..utils import to_bool, to_int, to_float, to_percent_used
from ..helpers import api_request


async def check_node(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    uri = '/status'
    data = await api_request(asset, asset_config, config, uri, 'node')

    node = data['data']
    boot = node.get('boot-info')
    cpu = node.get('cpuinfo')
    k = node.get('current-kernel')
    ksm = node.get('ksm')
    mem = node.get('memory')
    rootfs = node.get('rootfs')
    swap = node.get('swap')
    item = {
        'name': 'node',  # str
        'kversion': node.get('kversion'),  # str
        'pveversion': node.get('pveversion'),  # str
        'loadavg': [float(v) for v in node['loadavg']]
        if isinstance(node.get('loadavg'), list) else None,
        'cpu': to_float(node.get('cpu'), 100.0),  # float
        'idle': to_float(node.get('idle'), 100.0),  # float
        'wait': to_float(node.get('wait'), 100.0),  # float
        'uptime': node.get('uptime'),  # int
    }
    state = {
        'node': [item],
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
            'percent_used':
            to_percent_used(mem.get('total'), mem.get('used'))
        }]
    if swap is not None:
        state['swap'] = [{
            'name': 'swap',
            'free': swap.get('free'),  # int
            'total': swap.get('total'),  # int
            'used': swap.get('used'),  # int
            'percent_used':
            to_percent_used(swap.get('total'), swap.get('used'))
        }]
    if rootfs is not None:
        state['rootfs'] = [{
            'name': 'rootfs',
            'avail': rootfs.get('avail'),  # int
            'free': rootfs.get('free'),  # int
            'total': rootfs.get('total'),  # int
            'used': rootfs.get('used'),  # int
            'percent_used':
            to_percent_used(rootfs.get('total'), rootfs.get('used'))
        }]

    return state
