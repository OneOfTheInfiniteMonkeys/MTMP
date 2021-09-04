"""
# --------------------------------------
# Project          : MacroPad
# Version          : 0.2
# Date             : 04 Sep 2021
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTMP
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by
#                  : OneOfTheInfiniteMonkeys
# Hardware         : Addafruit MagTag
# --------------------------------------
#                  :
# From             : N/A
# --------------------------------------
# Notes            :
#-------------------
# Runs once on sartup
# See boot_out.txt for any errors raised in this code
#
# According to notes on boot.py
# May be called one of settings.txt, settings.py, boot.py, boot.txt
# Ouptut direcetd to boot_out.txt
"""
# -------><--------><--------><--------><--------><--------><--------><--------
import board  #                         Access to
import digitalio  #                     Low level access to switches
import sys  #                           Access to CircuitPython version
import storage  #                       Access to HID usb driver to turn off USB disk
import usb_cdc #                        Access to Serial port to turn off REPL

# Only if operating system version 7 and above
if (sys.implementation.version[0] >= 7):

    # For switch definitions see PCB and https://learn.adafruit.com/assets/102127
    switch = digitalio.DigitalInOut(board.D11)  #     Switch near USB connector
    switch.direction = digitalio.Direction.INPUT  #   Enable reading of switch
    switch.pull = digitalio.Pull.UP  #  True = not pressed, False = pressed

    # This section allows override of HID device disable for update or debug etc.
    # 
    # When the button identified above as 'switch' is pressed whilst the reset
    # button is pressed. 'switch.value' will evaluate to False. The code fragment
    # below disabling the HID devices is bypassed. Leaving both USB file access
    # and REPL (serial port) enabled to support debug mode and updates
    if (switch.value):  #               When button not pressed returning TRUE
        # Turn off the HID devices if button not pressed i.e. 'Normal Running Mode'
        # print("Normal Running Mode")
        storage.disable_usb_drive()  #  Turn off CIRCUITPY drive.
        usb_cdc.disable()  #            Turn off REPL (Read-Evaluate-Print-Loop).
#------------------------------------------------------------------------------
# Control handed over to code.py following hard reset

"""
# --------------------------------------
#
# --------------------------------------
2021-08-18 - 0.2 - Comment format and update only
2021-08-25 - 0.1 - Github release
# --------------------------------------
"""
