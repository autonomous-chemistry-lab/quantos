#!/usr/bin/env python
#
# Script Test - Quantos
# DMG UoL

import time
from mettler_toledo_quantos import MettlerToledoDevice

dev = MettlerToledoDevice(port='/dev/tty.usbserial-14110') # Lewis' MacBook - port 2 - specific port

'''
A test algorithm. Working.
'''
#dev.set_tolerance_value_pct(1)
#time.sleep(1)

#dev.set_target_value_mg(100)
#time.sleep(1)

#dev.lock_dosing_pin()
#time.sleep(2)

#dev.move_frontdoor_open()
#time.sleep(10)

#dev.move_to(6)
#time.sleep(10)

#dev.move_frontdoor_close()

'''
End.
'''

# Tested and working
#dev.move_frontdoor_open()
#dev.move_to(15)
#dev.move_frontdoor_close()
#dev.lock_dosing_pin()
#dev.unlock_dosing_pin()
#dev.set_target_value_mg(200)
#dev.set_tolerance_value_pct(5)
#dev.request_frontdoor_position()

# Untested
#dev.start_dosing()
dev.request_autosampler_position()  # This command is not working - see driver.



