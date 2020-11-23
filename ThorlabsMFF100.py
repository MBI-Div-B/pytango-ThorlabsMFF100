#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: / Email:

import thorpy.flipmount.flipmount as fm

from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, command, device_property

    
class ThorlabsMFF100(Device):
    serial_num = attribute(label="Serialnumber",
                           dtype=str,
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ,
                           doc="Serial number of device")

    serial_number = device_property(dtype=str)

    def init_device(self):
        Device.init_device(self)
        self.info_stream('Thorlabs Flip Mirror Mount with serial {:s}'.format(self.serial_number))
        self.mount = fm.flipMount(self.serial_number)
        self.set_state(DevState.ON)

    def dev_state(self):
        if self.mount.is_moving():
            self.set_status("Thorlabs Flip Mirror is: MOVING")
            self.debug_stream("Thorlabs Flip Mirror is: MOVING")
            return DevState.MOVING
        elif self.mount.is_open():
            self.set_status("Thorlabs Flip Mirror is: OPEN")
            self.debug_stream("Thorlabs Flip Mirror is: OPEN")
            return DevState.OPEN
        elif self.mount.is_close():
            self.set_status("Thorlabs Flip Mirror is: CLOSED")
            self.debug_stream("Thorlabs Flip Mirror is: CLOSED")
            return DevState.CLOSE
        else:
            self.set_status("Thorlabs Flip Mirror is: UNKOWN")
            self.debug_stream("Thorlabs Flip Mirror is: UNKOWN")
            return DevState.UNKNOWN

    def read_serial_num(self):
        return self.serial_number

    def read_info(self):
        return 'Information', dict(manufacturer='Thorlabs',
                                   model='MFF101',
                                   version_number=self.__serial_num)

    @command
    def Flip(self):
        self.mount.flip()

    @command
    def Close(self):
        self.mount.close()

    @command
    def Open(self):
        self.mount.open()

    @command
    def Identify(self):
        self.mount.identify()


if __name__ == "__main__":
    ThorlabsMFF100.run_server()
