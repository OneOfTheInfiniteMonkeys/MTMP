"""
# --------------------------------------
# Project          : MacroPad
# Version          : 0.1
# Date             : 25 Aug 2021
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

    # For switch defitnions see PCB and https://learn.adafruit.com/assets/102127
    switch = digitalio.DigitalInOut(board.D11)  #     Switch near USB connector
    switch.direction = digitalio.Direction.INPUT  #   Enable reading of switch
    switch.pull = digitalio.Pull.UP  #      True = not pressed, False = pressed

    # Turn off the HID devices if button not pressed
    if (switch.value):  #                   Button pressed is FALSE i.e. active low
        # print("Normal Mode")
        storage.disable_usb_drive()  #      Turn off CIRCUITPY.
        usb_cdc.disable()  #                Turn off REPL.
#------------------------------------------------------------------------------
# Control handed over to code.py following hard reset

