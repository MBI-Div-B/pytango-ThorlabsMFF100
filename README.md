# pytango-ThorlabsMFF100

PyTango Device Server to control motorized flip mirrors from Thorlabs: MFF101/102

# Installation

Clone/download adapted `thorpy` package

`git clone https://github.com/felix92/thorpy.git`

and install 

`python3 setup.py install`

## udev rule

Create a new udev rule

    > sudo nano /etc/udev/rules.d/99-thorlabs.rules
    
    ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", MODE="0666"

Relaod and apply the udev rule by

    sudo udevadm control --reload
    sudo udevadm trigger --action=add
