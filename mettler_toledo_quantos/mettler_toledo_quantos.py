#!/usr/bin/env python
#
# This is a module for mettler toledo quantos
#
# University of Liverpool
# Autonomous chemistry Lab
# (C) (2019) David Marquez-Gamez <dmarquez@liverpool.ac.uk>

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
            print('The dosing amount must be greater than 0.10 mg.')
        elif int(value) > 250000:
            print('The dosing amount must be less than 250,000 mg.')
        else:
            response = self._send_request_get_response('QRD 1 1 5 ' + str(value))
            return response

    def set_tolerance_value_pct(self, value):
        '''
        Sets the tolerance value as a percentage.
        Value must be between 0.1 and 40. Simple error handling incorporated.
        '''
        if int(value) < 0.10:
            print('The tolerance must be greater than 0.1%.')
        elif int(value) > 40:
            print('The tolerance must be less than 40%.')
        else:
            response = self._send_request_get_response('QRD 1 1 6 ' + str(value))
            return response

    def quantos_test(self):
        '''
        Close the Quantos front door.
        '''
        response = self._send_request_get_response('QRA 60 8 ')
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
    
# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = MettlerToledoDevice(debug=debug)
