"""><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><-->
# --------------------------------------
# Project          : MacroPad
# Version          : 0.5
# Date             : 05 Feb 2023
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTMP
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by OneOfTheInfiniteMonkeys
# Hardware         : Adafruit MagTag
# --------------------------------------
#                  :
# From             : CircuitPython Essentials HID Keyboard example
# --------------------------------------
# Trademarks       : As owned by the respective registrants
# -------><--------><--------><--------><--------><--------><--------><-------->
"""
import time  #                          To enable pause operations e.g. key debounce
import board  #                         Board level functions
import usb_hid  #                       Access to USB device emulation
from adafruit_magtag.magtag import MagTag  # Wrapper for lower level board features - Display, Network Graphics Peripherals

from adafruit_hid.keyboard import Keyboard  # Keyboard device emulation
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # Import keycode definitions
from adafruit_hid.consumer_control import ConsumerControl  # Volume control
from adafruit_hid.consumer_control_code import ConsumerControlCode

import helper as hlp  #                 Helper routines for Macropad

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

    for digits in magtag.peripherals.buttons:  #            Iterate through digitalio
        bpv = (bpv << 1) | (digits.value == 0)  #           Acquire i/o bit pattern

    return bpv  #   return a value representing the buttons pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Main code starts here
# ------------------------------------------------------------------------------
# instantiate the magtag object
magtag = MagTag(rotation = 0)

# --------------------------------------
# Colour definitions
# --------------------------------------
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
LOW_WHITE = 0x020202
LOW_YELLOW = 0x020200
# --------------------------------------

magtag.peripherals.neopixel_disable = False  #              Permit writing to the Neopixels
x = hlp.set_mt_leds(BLACK, 0, magtag)  #                    All LED's off
LBLPeriod = 15  #                                           Period between light intensity reads
LBLTm = time.monotonic() + LBLPeriod  #                     Update the intensity at this relative time
LBL = 4  #                                                  Default Light Booster Level
LBL = hlp.light_boost_level(hlp.average_light(magtag))  #   Get current light level
magtag.peripherals.neopixels[0] = LOW_YELLOW * LBL  #       Yellow - Busy Starting

# --------------------------------------
# As this has a delay intended to follow power up, it is placed here
# The keyboard object!
# --------------------------------------
time.sleep(2)  # Sleep for a bit to avoid a race condition on some systems
while True:
    try:
        keyboard = Keyboard(usb_hid.devices)
        keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
    except:
        x = hlp.set_mt_leds(BLACK, 0, magtag)  #                    All LED's off - LED pulse
        time.sleep(1.0)  #                                          Sleep for a bit
        magtag.peripherals.neopixels[0] = LOW_YELLOW * LBL  #       Yellow - Busy Starting
        time.sleep(1.0)  #                                          Sleep for a bit
        continue
    else:
        break
# --------------------------------------

DISPLAY_UPDATE_PERIOD = 3  #                                Default delay period for display re-draws

KbdLayer = 0  #                                             Which key layer use e.g. Zoom -> Teams and so on
KbdShift = 0  #                                             Flag indicating Shift active
KbdShiftTm = 0  #                                           Unreferenced time when Shift activated
ShiftHoldPeriod = 1.5  #                                    Period to keep Shift active 

magtag.set_background("/bmps/magtag-macro-00.bmp")  #       Load default background graphic
# Main display text for user messages
mt_idx = magtag.add_text(  #                                Allows for different text or messages
    text_font = "/fonts/Arial-Bold-12.bdf",
    text_position = (10, 8)
    )
magtag.set_text("Zoom", mt_idx, auto_refresh = True)  #     Default text for default mode
d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD)  #        Allow display to complete update

magtag.peripherals.neopixels[0] = LOW_BLUE * LBL  #         Blue ready power light at lighting level

print("Waiting for button press...")
# --------------------------------------
while True:  #                                              Infinite loop - look at buttons - generate keys
    bpv = button_read(magtag)  #                            Read the state of the MagTag buttons
    if (bpv != 0):  #                                       Has a MagTag button, aka as key, been pressed
        if (bpv > 15):  #                                   Manage overflows
            bpv &= 15  #                                    Limit value range
        time.sleep(0.075)  #                                Debounce period
        try:  #                                             Allow for USB busy error, file missing etc.
            if (button_read(magtag) == bpv):  #                       Debounce read
                bpv &= 15  #                                          Limit value range                                           
                # print("button pressed " + str(bpv))  #              Debug print key press value
                # magtag.peripherals.neopixels[0] = LOW_YELLOW * LBL  # Yellow - Busy - uncomment for visual press f/b

                KbdShiftTm = time.monotonic()  #                      Restart KbdShiftTmr if key pressed
                # "Type" the Keycode or string
                if (KbdLayer == 0):  #                                "Zoom" Meeting Mode
                    if (KbdShift == 0):  #                            No Shift modifier active - basic functions
                        if (bpv == 1):  #                             Mode change
                            KbdShift = 1  #                           Activate shift mode
                        elif (bpv == 4):
                            keyboard.press(Keycode.ALT, Keycode.V)  # "Press"...Video
                        elif (bpv == 8):
                            keyboard.press(Keycode.ALT, Keycode.A)  # "Press"...Audio
                    elif (KbdShift == 1):  #                          Shift modifier active
                        if (bpv == 1):
                            KbdLayer += 1  #                          Increment to next keyboard layer
                            KbdShift = 0  #                           Cancel shift modifier
                            x = hlp.set_mt_leds(BLACK, 0, magtag)  #  LED's off as we are busy
                            # Note - Next mode graphic shown
                            magtag.graphics.set_background("/bmps/magtag-macro-01.bmp")  # Load background graphic
                            magtag.set_text("Teams", mt_idx, auto_refresh = True)
                            d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD)  #           Allow display to complete update
                        elif (bpv == 4):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_INCREMENT)
                        elif (bpv == 8):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_DECREMENT)

                elif (KbdLayer == 1):  #                              "Teams" meeting mode
                    if (KbdShift == 0):  #                            No Shift modifier active - basic functions
                        if (bpv == 1):  #                             Mode change
                            KbdShift = 1  #                           Activate shift mode
                        elif (bpv == 4):
                            keyboard.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.O)  #  "Press"...
                        elif (bpv == 8):
                            keyboard.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)  #  "Press"...
                    elif (KbdShift == 1):  #                          Shift modifier active
                        if (bpv == 1):  #                             Mode change
                            KbdLayer = 0  #                           Reset keyboard layer
                            KbdShift = 0  #                           Cancel shift modifier
                            # Note - Next mode graphic shown
                            x = hlp.set_mt_leds(BLACK, 0, magtag)  #  LED's off as we are busy
                            magtag.graphics.set_background("/bmps/magtag-macro-00.bmp")  # Load background graphic
                            magtag.set_text("Zoom", mt_idx, auto_refresh = True)
                            d = hlp.while_display_busy(DISPLAY_UPDATE_PERIOD)  #           Allow display to complete update
                        elif (bpv == 4):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_INCREMENT)
                        elif (bpv == 8):
                            ConsumerControl(usb_hid.devices).send(ConsumerControlCode.VOLUME_DECREMENT)

                keyboard.release_all()  #                      ..."Release"!

                # Manage LED's for Shift modifier state
                if (KbdShift == 1):  #                                     Shift modifier active - set LEDs
                    x = hlp.set_mt_leds(LOW_WHITE, LBL, magtag)
                elif (KbdShift == 0):
                    x = hlp.set_mt_leds(BLACK, 0, magtag)  #               All LED's off
                    magtag.peripherals.neopixels[0] = LOW_BLUE * LBL  #    Blue ready power light at lighting level

        except:
            x = hlp.set_mt_leds(BLACK, 0, magtag)  #           All LED's off
            magtag.peripherals.neopixels[0] = ORANGE  #        Orange alert colour
            time.sleep(0.75) #                                 Signal error

    elif (bpv == 0):
        if (time.monotonic() > LBLTm):  #         Adjust LED brightness when no key
            LBL = hlp.light_boost_level(hlp.average_light(magtag))  #  Get current light level
            LBLTm =  time.monotonic() + LBLPeriod  #               Set new update time
        
    # Shift modifier time out feature
    if (KbdShift == 1):  #                                     Is keyboard Shift active
        if (time.monotonic() > (KbdShiftTm + ShiftHoldPeriod) ):  # Shift Hold period expired?
            KbdShift = 0  #                                    Reset Shift mode
            x = hlp.set_mt_leds(BLACK, 0, magtag)  #           All LED's off
            magtag.peripherals.neopixels[0] = LOW_BLUE * LBL  # Low Blue

    bpv = 0  #                                                 Clear the button press value
    time.sleep(0.05)  #                                        Repeat rate i.e. < 20/s
# --------------------------------------
#
# --------------------------------------
# End of code
# --------------------------------------
"""
# --------------------------------------
#
# --------------------------------------
2023-02-05 - 0.5 - Comment Typos corrected

2021-09-15 - 0.4 - Added error detect to USB HID creation to prevent occasional
                   USB detection error when connected to unpowered device
                   LED pulses yellow on off during loop
                   
2021-08-21 - 0.3 - Code clean up
                   Add power on Yellow busy LED indication
                   Modified LED handling through Shift state
                   Added optional key press event flash yellow
                   Commented out debug printing of button press value
                   Moved set_mt_leds to helper module
                   Use of timestamp for LED Shift timer as opposed to counter
                   Implemented button value range limit
2021-08-18 - 0.2 - Github functional release
                   Code tidy up, amend KbdDhiftTmr initialisation
2021-08-10 - 0.1 - Github release
# --------------------------------------
"""
