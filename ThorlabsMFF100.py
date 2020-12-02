#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: / Email:

import thorpy.flipmount.flipmount as fm

from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, command, device_property
from enum import IntEnum

class MirrorState(IntEnum):
    closed = 0
    open = 1
    moving = 2
    unknown = 3


class ThorlabsMFF100(Device):
    mffstate = attribute(label="Mirror State",
                         dtype=MirrorState,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="State can be 0=closed, 1=open, 2=moving, 3=unknown")

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
        self.__mff_state = 3

    def always_executed_hook(self):
        if self.mount.is_moving():
            self.set_status("Thorlabs Flip Mirror is MOVING")
            self.__mff_state = 2
            self.set_state(DevState.MOVING)
        elif self.mount.is_open():
            self.set_status("Thorlabs Flip Mirror is OPEN")
            self.__mff_state = 1
            self.set_state(DevState.OPEN)
        elif self.mount.is_close():
            self.set_status("Thorlabs Flip Mirror is CLOSED")
            self.__mff_state = 0
            self.set_state(DevState.CLOSE)
        else:
            self.set_status("Thorlabs Flip Mirror is UNKOWN")
            self.__mff_state = 3
            self.set_state(DevState.UNKNOWN)

    def read_mffstate(self):
        return self.__mff_state
        if self.__mff_state == 0:
            return MirrorState.closed
        elif self.__mff_state == 1:
            return MirrorState.open
        if self.__mff_state == 2:
            return MirrorState.moving
        else:
            return MirrorState.unknown

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
