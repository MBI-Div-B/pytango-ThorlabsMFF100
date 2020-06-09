import time
import numpy
import thorpy.flipmount.flipmount as fm



from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

class ThorlabsFlipMount(Device):

    isMoving = attribute(label="Moving", dtype=bool,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="True if mount is moving")

    isOpen = attribute(label="Open", dtype=bool,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="True if mount is down")

    isClose = attribute(label="Close", dtype=bool,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="True if mount is up")

    serial_num = attribute(label="Serialnumber", dtype=str,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="Serial number of device")



    serial_number = device_property(dtype=str)

    def init_device(self):
        Device.init_device(self)
        self.mount = fm.flipMount(self.serial_number)
        self.set_state(DevState.ON)

    def read_isMoving(self):
        tmp_moving = self.mount.is_moving()
        if tmp_moving:
            self.set_state(DevState.MOVING)
        return tmp_moving

    def read_isOpen(self):
        tmp_open = self.mount.is_open()
        if tmp_open:
            self.set_state(DevState.OPEN)
        return tmp_open

    def read_isClose(self):
        tmp_close = self.mount.is_close()
        if tmp_close:
            self.set_state(DevState.CLOSE)
        return tmp_close

#    def set_serial_number(self):
#        return self.__serial_number

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
    ThorlabsFlipMount.run_server()




