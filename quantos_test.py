#!/usr/bin/env python
#
# Script Test - Quantos
# DMG UoL

import time
from mettler_toledo_quantos import MettlerToledoDevice

dev = MettlerToledoDevice(port='/dev/tty.usbserial-14110') # Lewis' MacBook - port 2 - specific port

dev.move_frontdoor_open()
time.sleep(5)
dev.move_frontdoor_close()
time.sleep(10)
dev.quantos_test()
