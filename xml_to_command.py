#!/usr/bin/env python
#
# University of Liverpool
# Autonomous chemistry Lab
# (C) (2019) Lewis Jones <lewis.jones@liverpool.ac.uk>

from mettler_toledo_quantos import MettlerToledoDevice
import xml.etree.ElementTree as ET
import time

# load Values.xml file created in GUI_test.py
tree = ET.parse('Values.xml')
root = tree.getroot()

# initialise values
vials = range(0,20)
value_list = []

# find masses for dispensing from xml file, add to value_list
def find_values():
    for i in vials:
        value_list.append(int(root[i].text))

def initialise_quantos(tolerance=5):
    # Close door
    MettlerToledoDevice.move_frontdoor_close()
    time.sleep(5)

    # move to home position
    MettlerToledoDevice.move_to(0)
    time.sleep(10)

    # lock dosing pin
    MettlerToledoDevice.lock_dosing_pin()
    time.sleep(5)

    # set tolerance
    MettlerToledoDevice.set_tolerance_value_pct(tolerance)
    time.sleep(2)


def dosing():
    for i in vials:
        '''
        Rather than using wait times, would be more elegant to rely on the Quantos response to pass to next step...
        Something along the lines of:
        
        try MettlerToledoDevice.move_to(i):
            if response[x] == 'value':
                pass
            elif response[x] == 'error':
                print('There has been an error')
                break
    '''

        # Move to location
        MettlerToledoDevice.move_to(i)
        #print(response)
        time.sleep(10)

        # Set mass to be dispensed
        MettlerToledoDevice.set_target_value_mg(int(value_list[i]))
        #print(response)
        time.sleep(2)

        # start dispensing
        MettlerToledoDevice.start_dosing()
        #print(response)

        # print to terminal that dosing is complete
        print('Dosing number {} is complete.'.format(i))


# testing functions
initialise_quantos()
find_values()
dosing()

