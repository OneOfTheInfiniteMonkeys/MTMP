"""><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><-->
# --------------------------------------
# Project          : MacroPad
# Version          : 0.1
# Date             : 10 Aug 2021
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
#import microcontroller                  # Allow access to internal temperature
import board                             # Allow access to DISPLAY
import alarm                             # NV Ram access and wakeup alarm types
#import rtc                              # For the system clock setting
import time                              # access sleep function
#import wifi                             # Access to MAC id for a unique id
#import socketpool                       # Used to access network sockets
#import ssl                              # Secure Socket Layer protocol support
# import adafruit_requests               # Requests-like library for web interfacing
#import json                             # Support for json handling
import displayio                         # For bitmap image display
import adafruit_imageload                # Support for bitmap image loading of icons
import sys                               # System version information
from adafruit_magtag.magtag import MagTag # Wrapper for lower level board features - Network Graphics Peripherals
#
# --------------------------------------
# function list
# --------------------------------------
# nv_store_write_str(StrToStore, Location)
# nv_store_read_str(Location)

# count_neopixel(sel_mode, ldclr, lbl)
# mode_to_text(sel_mode)
# test_to_mode(sel_text)
# mode_to_lrg_icon_file
# wif_icon_load()
# button_read(ntg)
# average_light(magtag)
# light_boost_level(LightLevel)
# pause_or_press(magtag, delay_period)
# battery_check(sv)
# while_display_busy(delay_period)
# current_battery_level(sv)
# interpreter_ver():
# interpreter_nam():
# --------------------------------------


# ------------------------------------------------------------------------------
def interpreter_ver():
    """
    # --------------------------------------
    # Return CirctuitPython interpreter version as a string with decimal seperators
    # --------------------------------------
    """
    return ".".join(map(str, sys.implementation[1]))
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def interpreter_nam():
    """
    # --------------------------------------
    # Return CirctuitPython interpreter name as a string
    # --------------------------------------
    """
    return "".join(map(str, sys.implementation[0]))
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def nv_store_write_str(StrToStore, Location):
    """
    # --------------------------------------
    # Store a string to the battery backed memory (not EEPROM)
    """
    i = 0
    byteArray = bytes(StrToStore, 'ascii')
    # We only need to write length bytes of the string
    for i in range(len(StrToStore)):
        alarm.sleep_memory[Location + i] = byteArray[i]
    # <-- End of iteration transferring data into sleep memory

    # We need to terminate the string in the storage with a zero
    i += 1
    alarm.sleep_memory[Location + i] = 0
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def nv_store_read_str(Location):
    """
    # --------------------------------------
    # Retrieve a string from the battery backed memory (not EEPROM)
    # The string is zero (null) terminated in the memory
    # The input parameter is a memory location previously written
    """
    # Read from the specified location and return the string obtained
    i = 0                         # Initialise a counter
    StrToStore = ""               # Initialise string storage
    while (alarm.sleep_memory[Location + i] != 0):
        StrToStore += chr(alarm.sleep_memory[Location + i])  # build the string
        i += 1                    # Increment the counter to point at next byte
    # <-- End of loop reading from sleep memory
    return StrToStore  # return the string read from the memory location
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def count_neopixel(sel_mode, ldclr, lbl, magtag):
    """
    # --------------------------------------
    # Set the LED's at the top of the MagTag to show the binary value of the
    # integer parameter sel_mode. The range is 0 to 0x0F or 16 decimal
    # Accomodates LED numbering from right to left
    # 3 parameters:
    #   sel_mode - integer, range 0 to 0x0F or 16 decimal
    #   ldclr    - integer, range 0x000001 to 0x0F0000
    #   lbl      - integer, range 0 to 16 representing light boost level
    """
    magtag.peripherals.neopixels.fill(0x000000)
    if (ldclr == 0):
        ldclr = 0x000800  # Default to green where no colour selected
    if (ldclr > 0x0F0000):
        ldclr = 0x0F0000  # Accomodate colour and light level boost feature
    if (lbl < 1):
        lbl = 1    # Always have at least some boost so as not to multiply by 0
    if (sel_mode > 0):  #  Don't write a colour if sel_mode is zero
        if (sel_mode & 1):
            magtag.peripherals.neopixels[3] = (ldclr) * lbl  # colour * brightness
        if (sel_mode & 2):
            magtag.peripherals.neopixels[2] = (ldclr) * lbl
        if (sel_mode & 4):
            magtag.peripherals.neopixels[1] = (ldclr) * lbl
        if (sel_mode & 8):
            magtag.peripherals.neopixels[0] = (ldclr) * lbl
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_vlt_icon(lvl, magtag):
    sv = Current_Battery_Level(lvl)
    load_small_icon("bat0" + str(sv) + ".bmp", 274, magtag)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_wif_icon(lvl, magtag):
    sv = 6
    load_small_icon("wif0" + str(sv) + ".bmp", 258, magtag)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_small_icon(icon_file_name, xpos, magtag):
    # uses small_icon_class
    icons_small_bmp, icons_small_pal = adafruit_imageload.load("/bmps/" + icon_file_name)
    small_icon_class = displayio.TileGrid(
                                    icons_small_bmp,
                                    pixel_shader=icons_small_pal,
                                    x=xpos,
                                    y=0,
                                    width=1,
                                    height=1,
                                    tile_width=16,
                                    tile_height=16,
                                   )

    small_ico_class = displayio.Group(max_size=1)
    small_ico_class.append(small_icon_class)
    magtag.splash.append(small_ico_class)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def button_read(magtag):
    """
    # --------------------------------------
    # Reads the MagTag buttons and returns an integer representing the
    # combination of buttons pressed
    # combination of buttons pressed
    # No buttons pressed = 0 all buttons pressed = 15
    """
    # bpv = Button Pressed Value
    bpv = int(not magtag.peripherals.buttons[0].value)
    bpv += int(not magtag.peripherals.buttons[1].value)*2
    bpv += int(not magtag.peripherals.buttons[2].value)*4
    bpv += int(not magtag.peripherals.buttons[3].value)*8

    return bpv                 # return a value representing the buttons pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def average_light(magtag):
    """
    # --------------------------------------
    # Reads the MagTag light sensors and returns an integer representing the
    # average light level over a sample period
    """
    NoOfIterations = 2                              # Number of iterations to perform
    i = 0                                           # loop counter
    oll = magtag.peripherals.light                  # oll = Old Light Level
    lla = 0                                         # lla = Light Level Average
    while (i < NoOfIterations):
        # Exponential filter
        lla = (0.7 * magtag.peripherals.light) + (0.3 * oll)
        oll = lla
        i += 1
        time.sleep(0.05)
    # <-- End Of While loop
    # print("Light Level Average:" + str(lla))
    # return an integer value representing the averaged light level
    return int(lla)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def light_boost_level_factor(LightLevel):
    """
    # --------------------------------------
    # Calculate the Light boost level based on the provided Light Level
    # taken from a light sensor, or possibly derived from time of day etc.
    # Colours can be multiplied by the boost level to increase the brightness
    # such that RGB 00 00 08 becomes RGB 00 00 10 when multiplied by 2
    # Note:
    #   Values shown above in hex
    #   The boost points are empiricaly selected
    """
    # bl = Boost Level
    bl = 1
    if (LightLevel >= 500):
        bl = 2
    if(LightLevel >= 750):
        bl = 4
    if(LightLevel >= 2000):
        bl = 6
    if(LightLevel >= 3000):
        bl = 8
    if(LightLevel >= 5000):
        bl = 10
    if(LightLevel >= 6000):
        bl = 16
    # print("Light Boost Level  :" + str(bl))
    return int(bl)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def light_boost_level(LightLevel):
    """
    # --------------------------------------
    # Wraps measuring the light level and scaling to an integer boost level
    """
    return light_boost_level_factor(LightLevel)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def pause_or_press(magtag, delay_period):
    """
    # --------------------------------------
    # Pauses unless key pressed returns key pressed value
    # Flashing one of the NEOPIXEL LED's
    # The delay period shold be at least 1 second
    """
    # Allow the user chance to press any button on the front of the MagTag
    i = 0                                                     # Loop counter
    b = 0                                                     # Will be button pressed value
    end_period = delay_period * 10                            # Convert delay_period to sleep counts
    while ((i <= end_period) & (b == 0)):
        i += 1                                                # Increment the counter
        b = button_read(magtag)                                  # Read all buttons and return a value
        time.sleep(0.1)                                       # We don't need to sample too quickly
    return int(b)                                             # return the button pressed 0 if none pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def while_display_busy(delay_period):
    """
    # --------------------------------------
    # Monitor the display, as it might complete early otherwise exit if the delay period expires
    # normally the returned value will reflect that the display completed updating sooner than
    # the allowed delay_period
    """
    display = board.DISPLAY                                   # permit access to the display device (e-ink)
    i = 0                                                     # Loop counter
    d = 1                                                     # Will be display status returned
    if (delay_period < 2):                                    # Ensure display_period is at least 2 seconds
        delay_period = 2
    end_period = delay_period * 10                            # Convert delay_period to sleep counts
    while ((i <= end_period) & (d == 1)):                     # Loop until display completes or count expires
        i += 1                                                # Increment the counter
        time.sleep(0.1)                                       # We don't need to sample too quickly
        d = display.busy                                      # Read display status
    return d                                                  # return the display status
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def battery_check(sv, lpsp, mt_idx, magtag):
    """
    # --------------------------------------
    # Checks the battery level and display a warning if too low.
    # Voltage cut off for:
    # PKCELL LP402025  150 mAh 3.7 V Li.Poly - No Applicable
    # PKCELL LP503035  500 mAh 3.7 V Li.Poly
    # PKCELL LP503562 1200 mAh 3.7 V Li.Poly
    # PKCELL LP803860 2000 mAh 3.7 V Li.Poly - No Applicable
    # PKCELL LP605080 3000 mAh 3.7 V Li.Poly - No Applicable
    # Voltage range from 4.2 Volts fully charged to 3.7 Volts
    # We are working to just above 88% of 4.2 Volts based on acquired data
    # To permit the power LED not to fully exhaust the battery
    """
    # sv = SystemVoltage
    if (sv <= 3.72):
        magtag.graphics.set_background("/bmps/magtag-pl-01.bmp")  # Show Power on graphic - battery empty
        magtag.set_text("Battery Low!     " + "{:.2f}".format(sv) + " Volts", mt_idx, auto_refresh=True )
        d = while_display_busy(3)                                 # Allow display to complete update
        d = pause_or_press(magtag, 5)                             # Pause and allow a key press

    # If battery really low then sleep to protect the battery
    if (sv < 3.7):                                                # 83% of 3.7 Volts - Assume Power LED draws 40 uA
        magtag.graphics.set_background("/bmps/magtag-pl-01.bmp")  # Show a Power on graphic - battery empty
        magtag.set_text("Recharge now!     " + "{:.2f}".format(sv) + " Volts", mt_idx, auto_refresh=True )
        d = while_display_busy(3)                                 # Allow display to complete update
        magtag.exit_and_deep_sleep(lpsp)                          # Basiclly don't wake again - well ~ 1 month
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def Current_Battery_Level(sv):
    """
    # --------------------------------------
    # Assign a battery level to the voltage
    # Returns an integer  level classification
    # e.g. for battery icon selection
    # Approximation for the PKCELL 500 mAh battery
    # sv = System Voltage
    # bl = Battery Level
    # 4.20 Volts a battery is charged - 4.30 volts no battery fitted
    # --------------------------------------
    """

    if (sv >= 4.2):
        bl = 6
    if (sv < 4.2):
        bl = 5
    if (sv < 4.10):
        bl = 4
    if (sv < 3.90):
        bl = 3
    if (sv < 3.81):
        bl = 2
    if (sv < 3.74):
        bl = 1
    if (sv < 3.71):
        bl = 0
    print("System voltage     :" + "{:.1f}".format(sv) +
          " Volts " + " Bat. Level " + str(bl))
    return int(bl)                           # Return the assessed battery level
# ------------------------------------------------------------------------------
