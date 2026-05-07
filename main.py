from libprobe.probe import Probe
from lib.check.guests import CheckGuests
from lib.check.network import CheckNetwork
from lib.check.node import CheckNode
from lib.check.storage import CheckStorage
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckGuests,
        CheckNetwork,
        CheckNode,
        CheckStorage,
    )

    probe = Probe("proxmoxnode", version, checks)

    probe.start()
