import re
import subprocess

from serial import Serial


def get_serial_port():
    ports = subprocess.getoutput('python -m serial.tools.list_ports')
    match = re.search(r'/dev/ttyACM\d', ports)

    if match:
        return match.group()

    raise RuntimeError('Serial not found')


serial = Serial(get_serial_port(), 9600, timeout=5)
