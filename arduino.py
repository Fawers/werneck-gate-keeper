import re
import subprocess

from serial import Serial


def get_serial_port():
    ports = subprocess.getoutput('python -m serial.tools.list_ports')
    match = re.search(r'/dev/ttyACM\d', ports)

    if match:
        return match.group()

    return None


serial = Serial(get_serial_port(), 9600)
serial.timeout = 5
