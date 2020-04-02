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



def dosing():
    for i in vials:
        # print('{}'.format(i), value_list[i])

        #MettlerToledoDevice.move_to(i)
        #time.sleep(10)



# testing functions
#initialise_quantos()
find_values()
dosing()

