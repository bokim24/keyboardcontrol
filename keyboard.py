#!/usr/bin/env python

import usb.core
import usb.util
import explorerhat
import time

explorerhat.light.red.on()

USB_VENDOR  = 0x1997 # Rii
USB_PRODUCT = 0x2433 # Mini Wireless Keyboard

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_LEFT  = 80
BTN_RIGHT = 79
BTN_DOWN  = 81
BTN_UP    = 82
BTN_STOP  = 44 # Space
BTN_EXIT  = 41 # ESC

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

explorerhat.light.red.off()
explorerhat.light.green.on()

while True:
    control = None
    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        print(control)
    except:
        pass

    if control != None:
        if BTN_DOWN in control:
            explorerhat.motor.backwards()

        if BTN_UP in control:
            explorerhat.motor.forwards()

        if BTN_LEFT in control:
            explorerhat.motor.two.forwards()
            explorerhat.motor.one.backwards()

        if BTN_RIGHT in control:
            explorerhat.motor.two.backwards()
            explorerhat.motor.one.forwards()

        if BTN_STOP in control:
            explorerhat.motor.stop()

        if BTN_EXIT in control:
            exit()

    time.sleep(0.02)
