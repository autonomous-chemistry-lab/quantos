#!/usr/bin/env python
#
# Script Test - Quantos
# DMG UoL

import time
from mettler_toledo_quantos import MettlerToledoDevice

dev = MettlerToledoDevice(port='/dev/ttyUSB0') # Linux specific port
#dev.move_frontdoor_open()
#dev.move_frontdoor_close()
dev.quantos_test()
