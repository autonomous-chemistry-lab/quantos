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
#dev.move_to(0)
#dev.move_frontdoor_close()
dev.lock_dosing_pin()
#dev.unlock_dosing_pin()
#dev.set_target_value_mg(50)
#dev.set_tolerance_value_pct(5)
#dev.request_frontdoor_position()
#dev.start_dosing()

# Untested
#dev.request_autosampler_position()  # This command is not working - see driver.


#dev.set_target_value_mg(150)
#time.sleep(5)

#dev.move_to(0)
#time.sleep(10)
#dev.start_dosing()
#time.sleep(120)

#dev.set_target_value_mg(75)
#time.sleep(5)

#dev.move_to(1)
#time.sleep(10)
#dev.start_dosing()
#time.sleep(180)

#dev.move_to(3)
#time.sleep(10)
#dev.start_dosing()
#time.sleep(180)

dev.lock_dosing_pin()
time.sleep(4)

dev.move_to(6)
time.sleep(10)
dev.start_dosing()
time.sleep(180)

dev.move_to(10)
time.sleep(10)
dev.start_dosing()

#end






