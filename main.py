from libprobe.probe import Probe
from lib.check.guests import check_guests
from lib.check.network import check_network
from lib.check.node import check_node
from lib.check.storage import check_storage
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'guests': check_guests,
        'network': check_network,
        'node': check_node,
        'storage': check_storage,
    }

    probe = Probe("proxmoxnode", version, checks)

    probe.start()
