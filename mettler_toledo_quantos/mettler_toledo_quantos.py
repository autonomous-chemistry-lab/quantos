#!/usr/bin/env python
#
# This is a module for mettler toledo quantos
#
# University of Liverpool
# Autonomous chemistry Lab
# (C) (2019) David Marquez-Gamez <dmarquez@liverpool.ac.uk>
# (C) (2019) Lewis Jones <lewis.jones@liverpool.ac.uk>

from __future__ import print_function, division
import serial
import time
import atexit
import platform
import os
try:
    from exceptions import Exception
except ImportError:
    pass

from serial_interface import SerialInterface, SerialInterfaces, find_serial_interface_ports, WriteFrequencyError

DEBUG = True
BAUDRATE = 9600

class MettlerToledoError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MettlerToledoDevice(object):
    '''
    This module (mettler_toledo_quantos) creates a class named MettlerToledoDevice, 
    to interface to Mettler Toledo Quantos using the Mettler Toledo
    Standard Interface Command Set for Quantos system (MT-SICS-Quantos).
    '''
    _TIMEOUT = 0.05
    _WRITE_WRITE_DELAY = 0.05
    _RESET_DELAY = 2.0

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        if 'baudrate' not in kwargs:
            kwargs.update({'baudrate': BAUDRATE})
        elif (kwargs['baudrate'] is None) or (str(kwargs['baudrate']).lower() == 'default'):
            kwargs.update({'baudrate': BAUDRATE})
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        if ('port' not in kwargs) or (kwargs['port'] is None):
            err_string = 'Specify port.\n'
            raise RuntimeError(err_string)
        else:
            self.port = kwargs['port']

        t_start = time.time()
        self._serial_device = SerialInterface(*args,**kwargs)
        atexit.register(self._exit_mettler_toledo_device)
        time.sleep(self._RESET_DELAY)
        t_end = time.time()
        self._debug_print('Initialization time =', (t_end - t_start))


    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _exit_mettler_toledo_device(self):
        pass

    def close(self):
        '''
        Close the device serial port.
        '''
        self._serial_device.close()

    def _args_to_request(self,*args):
        request = ''.join(map(str,args))
        request = request + '\r\n';MettlerToledoError
        return request

    def _send_request_get_response(self,*args):

        '''Sends request to device over serial port and
        returns response'''

        request = self._args_to_request(*args)
        self._debug_print('request', request)
        response = self._serial_device.write_read(request,use_readline=True,check_write_freq=True)
        response = response.decode().replace('"','')
        response_list = response.split()
        if 'L' in response_list:
            raise MettlerToledoError('Syntax Error!')
        return response_list

    def move_frontdoor_open(self):
        '''
        Opens the Quantos front door.
        '''
        response = self._send_request_get_response('QRA 60 7 3')
        if 'I' in response[3]:
            if '1' in response[4]:
                raise MettlerToledoError('Not mounted.')
            elif '2'in response[4]:
                self._debug_print('Another job is running -- retrying.')
                self.move_frontdoor_open()
                #raise MettlerToledoError('Another job is running.')
            elif '3'in response[4]:
                raise MettlerToledoError('Timeout.')
            elif '4'in response[4]:
                raise MettlerToledoError('Not selected.')
            elif '5'in response[4]:
                raise MettlerToledoError('Not allowed at the moment')
            else:
                raise MettlerToledoError('Stopped by external action.')
        return response

    def move_frontdoor_close(self):
        '''
        Close the Quantos front door.
        '''
        #response = self._send_request_get_response('QRA 60 2 4')
        response = self._send_request_get_response('QRA 60 7 2')
        if 'I' in response[3]:
            if '1' in response[4]:
                raise MettlerToledoError('Not mounted.')
            elif '2'in response[4]:
                self._debug_print('Another job is running -- retrying.')
                self.move_frontdoor_close()
                #raise MettlerToledoError('Another job is running.')
            elif '3'in response[4]:
                raise MettlerToledoError('Timeout.')
            elif '4'in response[4]:
                raise MettlerToledoError('Not selected.')
            elif '5'in response[4]:
                raise MettlerToledoError('Not allowed at the moment.')
            else:
                raise MettlerToledoError('Stopped by external action.')
        return response

    def move_to(self,position):
        '''
        Move Quantos sampler, taking the position as an argument.
        '''
        response = self._send_request_get_response('QRA 60 8 ' + str(position))
        return response

    def unlock_dosing_pin(self):
        '''
        Unlock dosing pin, allowing removal of dosing head.
        '''
        response = self._send_request_get_response('QRA 60 2 3')
        return response

    def lock_dosing_pin(self):
        '''
        Lock dosing pin, readying dosing head for dispensing.
        '''
        response = self._send_request_get_response('QRA 60 2 4')
        return response

    def set_target_value_mg(self, value):
        '''
        Sets the target dosing value in mg.
        Value must be between 0.1 and 250000. Simple error handling incorporated.
        '''
        if int(value) < 0.10:
            self._debug_print('The target value must be greater than 0.1 mg. -'
                              'Change the value and try again.')
        elif int(value) > 250000:
            self._debug_print('The target value must be less than 250,000 mg. -'
                              'Change the value and try again.')
        else:
            response = self._send_request_get_response('QRD 1 1 5 ' + str(value))
            return response

    def set_tolerance_value_pct(self, value):
        '''
        Sets the tolerance value as a percentage.
        Value must be between 0.1 and 40. Simple error handling incorporated.
        '''
        if int(value) < 0.10:
            self._debug_print('The tolerance must be greater than 0.1% -'
                              'Change the value and try again.')
        elif int(value) > 40:
            self._debug_print('The tolerance must be less than 40% -'
                              'Change the value and try again.')
        else:
            response = self._send_request_get_response('QRD 1 1 6 ' + str(value))
            return response

    def start_dosing(self):
        '''
        Starts dosing. Uses previously set parameters including:
        target, tolerance and powder dosing algorithm
        '''
        response = self._send_request_get_response('QRA 61 1')
        # Error handling
        if 'I' in response[3]:
            if '1' in response[4]:
                raise MettlerToledoError('Not mounted.')
            elif '2' in response[4]:
                self._debug_print('Another job is running -- retrying.')
                self.start_dosing()
            elif '3' in response[4]:
                raise MettlerToledoError('Timeout.')
            elif '4' in response[4]:
                raise MettlerToledoError('Not selected.')
            elif '5' in response[4]:
                raise MettlerToledoError('Not allowed at the moment.')
            elif '6' in response[4]:
                self._debug_print('Weight not stable - trying again in 5 seconds.')
                time.sleep(5)
                self.start_dosing()
            elif '7' in response[4]:
                raise MettlerToledoError('Powderflow error.')
            elif '8' in response[4]:
                raise MettlerToledoError('Stopped by external action.')
            elif '9' in response[4]:
                raise MettlerToledoError('Safe position error.')
            elif '10' in response[4]:
                raise MettlerToledoError('Head not allowed.')
            elif '11' in response[4]:
                raise MettlerToledoError('Head limit reached.')
            elif '12' in response[4]:
                raise MettlerToledoError('Head expiry date reached.')
            elif '13' in response[4]:
                raise MettlerToledoError('Sampler blocked.')
        return response

    def request_frontdoor_position(self):
        '''
        Requests the position of the front door.
        '''
        response = self._send_request_get_response('QRD 2 3 7')

        # return position as text
        if '2' in response[4]:
            return self._debug_print('Door is closed.')
        if '3' in response[4]:
            return self._debug_print('Door is opened.')
        if '8' in response[4]:
            return self._debug_print('Door is not detectable.')
        if '9' in response[4]:
            return self._debug_print('Running.')
        # Error handling
        if 'I' in response[4]:
            if '1' in response[5]:
                raise MettlerToledoError('Not mounted.')
            elif '2' in response[5]:
                self._debug_print('Another job is running - waiting 5 seconds and trying again.')
                time.sleep(5)
                self.request_frontdoor_position()
            elif '3' in response[5]:
                raise MettlerToledoError('Timeout.')
            elif '4' in response[5]:
                raise MettlerToledoError('Not selected.')
            elif '5' in response[5]:
                raise MettlerToledoError('Not allowed at the moment.')
            elif '8' in response[5]:
                raise MettlerToledoError('Stopped by external action.')
        return response

    def request_autosampler_position(self):
        '''
        Requests the position of the autosampler.

        !!! This is currently not working - throwing up 'Syntax error',
        command is understood but not executable. !!!
        '''
        response = self._send_request_get_response('QRD 2 3 8')

        # Return position as text
        if 'I' in response[4]:
            if '1' in response[5]:
                raise MettlerToledoError('Not mounted.')
            elif '2' in response[5]:
                self._debug_print('Another job is running - waiting 5 seconds and trying again.')
                time.sleep(5)
                self.request_frontdoor_position()
            elif '3' in response[5]:
                raise MettlerToledoError('Timeout.')
            elif '4' in response[5]:
                raise MettlerToledoError('Not selected.')
            elif '5' in response[5]:
                raise MettlerToledoError('Not allowed at the moment.')
            elif '8' in response[5]:
                raise MettlerToledoError('Stopped by external action.')
        else:
            return response


    def quantos_test(self):
        '''
        Close the Quantos front door.
        '''
        response = self._send_request_get_response('QRD 1 1 2 1')
        #response = self._send_request_get_response('QRA 60 2 3')
        '''
        if 'I' in response[3]:
            if '1' in response[4]:
                raise MettlerToledoError('Not mounted.')
            elif '2'in response[4]:
                self._debug_print('Another job is running -- retrying.')
                self.move_frontdoor_close()
                #raise MettlerToledoError('Another job is running.')
            elif '3'in response[4]:
                raise MettlerToledoError('Timeout.')
            elif '4'in response[4]:
                raise MettlerToledoError('Not selected.')
            elif '5'in response[4]:
                raise MettlerToledoError('Not allowed at the moment.')
            else:
                raise MettlerToledoError('Stopped by external action.')
        '''
        return response
    
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = MettlerToledoDevice(debug=debug)
