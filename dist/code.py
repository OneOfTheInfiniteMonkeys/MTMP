"""><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><-->
# --------------------------------------
# Project          : MacroPad
# Version          : 0.2
# Date             : 18 Aug 2021
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTMP
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by OneOfTheInfiniteMonkeys
# Hardware         : Addafruit MagTag
# --------------------------------------
#                  :
# From             : CircuitPython Essentials HID Keyboard example
# --------------------------------------
# Trademarks       : As owned by the respective registrants
# -------><--------><--------><--------><--------><--------><--------><-------->
"""
import time  #                          To enable pause operations e.g. key debounce
import board  #                         Board level functions
import displayio  #                     Graphics functions access
import usb_hid  #                       Access tu USB device emulation
from adafruit_magtag.magtag import MagTag  # Wrapper for lower level board features - Display, Network Graphics Peripherals

from adafruit_hid.keyboard import Keyboard  # Keyboard device emulation
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # import keycode definitions
from adafruit_hid.consumer_control import ConsumerControl  # Volume control
from adafruit_hid.consumer_control_code import ConsumerControlCode

import helper as hlp  #                 Helper routines for Macropad

# ------------------------------------------------------------------------------
def set_mt_leds(ldclr, lbl):
    """
    # --------------------------------------
    # Set LED's to colour and intensity 
    # --------------------------------------
    """
    if (lbl == 0):  #  Ensure light booster level is non zero so LED is active
        lbl = 4
    magtag.peripherals.neopixels[3] = (ldclr) * lbl  # colour * brightness
    magtag.peripherals.neopixels[2] = (ldclr) * lbl
    magtag.peripherals.neopixels[1] = (ldclr) * lbl
    magtag.peripherals.neopixels[0] = (ldclr) * lbl

    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def button_read(magtag):
    """
    # --------------------------------------
    # Reads the MagTag buttons and returns an integer representing the
    # combination of buttons pressed
    # No buttons pressed = 0 all buttons pressed = 15
    """
    # bpv = Button Pressed Value
    bpv = 0

    for digits in magtag.peripherals.buttons:  #                 Iterate through digitalio
        bpv = (bpv << 1) | (digits.value==0)  #                  Acquire i/o bit pattern

    return bpv                 # return a value representing the buttons pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Main code starts here
# ------------------------------------------------------------------------------
# As this has a delay intended to follow power up, it is placed here
# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
#  kbd = Keyboard(usb_hid.devices)
#  cc = ConsumerControl(usb_hid.devices)

# intantiate the magtag object
magtag = MagTag(rotation=0)
magtag.peripherals.neopixels_disable = True  # Ensure the LED's are off

DISPLAY_UPDATE_PERIOD = 3  #                                    Default delay period for display re-draws

KbdLayer = 0  #                                                 Which key layer use e.g. Zoom -> Teams and so on
KbdShift = 0  #                                                 Flag indicating Shift active
KbdShiftTmr = 0  #                                              Allows for time out of Shift functions

magtag.set_background("/bmps/magtag-macro-00.bmp")  #  Load default background graphic
# Main display text for user messages
mt_idx = magtag.add_text(
    text_font = "/fonts/Arial-Bold-12.bdf",
    text_position = (10, 8)
    )
magtag.set_text("Zoom", mt_idx, auto_refresh = True)
d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD) #            Allow display to complete update

# Neopixel Colours - Order R G B
RED = 0xFF0000
AMBER = 0xAA9900
BLUE = 0x0066FF
MAGENTA = 0xFF00FF
PURPLE = 0x3B0F85
ORANGE = AMBER
BLACK = 0x000000
LOW_RED = 0x040000
LOW_GREEN = 0x000400
LOW_BLUE = 0x000004
LOW_WHITE = 0X020202


LBL = 4  #                                                 Default Light Booster Level
LBL = hlp.light_boost_level(hlp.average_light(magtag))  #  Get current light level
magtag.peripherals.neopixel_disable = False  #             Permit writing to the Neopixels
x = set_mt_leds(BLACK, 0)  #                               Led's off
magtag.peripherals.neopixels[0] = LOW_BLUE * LBL  #        Blue Power On lighting level

print("Waiting for button press...")
while True:  #                                             Infinite loop - look at buttons - generate keys
    bpv = button_read(magtag)  #                               Read the state of the MagTag buttons
    if (bpv != 0):  #                                          Has a MagTag button aka a key been pressed
        if (bpv > 15):  #                                      Manage overflows
            bpv &= bpv
        time.sleep(0.02)  #                                    Debounce period
        try:  #                                                Allow for USB busy error
            if (button_read(magtag) == bpv):  #                Debounce read
                print("button pressed " + str(bpv))  #         Debug print key press value
                magtag.peripherals.neopixels[0] = LOW_GREEN * LBL  #   Green

                KbdShiftTmr = 0  #                                   Restart the KbdShiftTmr if a key is pressed
                # "Type" the Keycode or string
                if (KbdLayer == 0):  #                               Zoom Meeting Mode
                    if (KbdShift == 0):  #                           No Shift modifier active - basic functions
                        if (bpv == 1):  #                            Mode change
                            KbdShift = 1  #                          Activate shift mode
                            x = set_mt_leds(LOW_WHITE, 4)
                        elif (bpv == 4):
                            keyboard.press(Keycode.ALT, Keycode.V)  #    "Press"...Video
                        elif (bpv == 8):
                            keyboard.press(Keycode.ALT, Keycode.A)  #    "Press"...Audio
                    elif (KbdShift == 1):  #                         Shift modifier active
                        if (bpv == 1):
                            KbdLayer += 1  #                         Increment to next keyboard leyer
                            KbdShift = 0  #                          Cancel shift modifier
                            x = set_mt_leds(BLACK, 0)  #             Led's off as we are busy
                            # Note next mode graphic shown
                            magtag.graphics.set_background("/bmps/magtag-macro-01.bmp")  # Load background graphic
                            magtag.set_text("Teams", mt_idx, auto_refresh=True)
                            d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD)  #           Allow display to complete update
                            magtag.peripherals.neopixels[0] = LOW_BLUE *LBL #              Ready
                        elif (bpv == 4):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_INCREMENT)
                        elif (bpv == 8):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_DECREMENT)

                elif (KbdLayer == 1):
                    if (KbdShift == 0):  #                           No Shift modifier active - basic functions
                        if (bpv == 1):  #                            Mode change
                            KbdShift = 1  #                          Activate shift mode
                            x = set_mt_leds(LOW_WHITE, 4)
                        elif (bpv == 4):
                            keyboard.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.O)  # "Press"...
                        elif (bpv == 8):
                            keyboard.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)  # "Press"...
                    elif (KbdShift == 1):  #                         Shift modifier active
                        if (bpv == 1):  #                            Mode change
                            KbdLayer = 0  #                          Reset keyboard layer
                            KbdShift = 0  #                          Cancel shift modifier
                            # Note next mode graphic shown
                            x = set_mt_leds(BLACK, 0)  #             Led's off as we are busy
                            magtag.graphics.set_background("/bmps/magtag-macro-00.bmp")  # Load background graphic
                            magtag.set_text("Zoom", mt_idx, auto_refresh=True)
                            d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD)  #           Allow display to complete update
                            magtag.peripherals.neopixels[0]= LOW_BLUE * LBL  #             Ready
                        elif (bpv == 4):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_INCREMENT)
                        elif (bpv == 8):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_DECREMENT)

                keyboard.release_all()  #                    ..."Release"!
                LBL = hlp.light_boost_level(hlp.average_light(magtag))  #  Get current light level

        except:
            x = set_mt_leds(BLACK, 0)  #                       All LED's off
            magtag.peripherals.neopixels[0] = ORANGE  #        Orange alert colour
            time.sleep(0.75) #                                 Signal error

    bpv = 0  #                                                 Clear the button press value

    # Shift modifer time out feature
    if (KbdShift == 1):  #                                     Is keyboard Shift active
        KbdShiftTmr += 1  #                                    Shift timer expiry rate increment
        if (KbdShiftTmr >= 14):  #                             At least n times the run period below ~ 1.5 sconds
            KbdShiftTmr = 0  #                                 Reset Shift timer
            KbdShift = 0  #                                    Reset Shift mode

            x = set_mt_leds(BLACK, 4)  #                       All LED's off
            magtag.peripherals.neopixels[0]= LOW_BLUE * LBL  # Low Blue

    time.sleep(0.10) # Repeat rate
