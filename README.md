# MTMP (MagTag MacroPad)
![Language](https://img.shields.io/static/v1?label=CircuitPython&message=6.3.0&color=blueviolet&style=flat-square)
[![MagTag](https://img.shields.io/badge/gadget-MagTag-blueviolet.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMTIgMTIgNDAgNDAiPjxwYXRoIGZpbGw9IiMzMzMzMzMiIGQ9Ik0zMiwxMy40Yy0xMC41LDAtMTksOC41LTE5LDE5YzAsOC40LDUuNSwxNS41LDEzLDE4YzEsMC4yLDEuMy0wLjQsMS4zLTAuOWMwLTAuNSwwLTEuNywwLTMuMiBjLTUuMywxLjEtNi40LTIuNi02LjQtMi42QzIwLDQxLjYsMTguOCw0MSwxOC44LDQxYy0xLjctMS4yLDAuMS0xLjEsMC4xLTEuMWMxLjksMC4xLDIuOSwyLDIuOSwyYzEuNywyLjksNC41LDIuMSw1LjUsMS42IGMwLjItMS4yLDAuNy0yLjEsMS4yLTIuNmMtNC4yLTAuNS04LjctMi4xLTguNy05LjRjMC0yLjEsMC43LTMuNywyLTUuMWMtMC4yLTAuNS0wLjgtMi40LDAuMi01YzAsMCwxLjYtMC41LDUuMiwyIGMxLjUtMC40LDMuMS0wLjcsNC44LTAuN2MxLjYsMCwzLjMsMC4yLDQuNywwLjdjMy42LTIuNCw1LjItMiw1LjItMmMxLDIuNiwwLjQsNC42LDAuMiw1YzEuMiwxLjMsMiwzLDIsNS4xYzAsNy4zLTQuNSw4LjktOC43LDkuNCBjMC43LDAuNiwxLjMsMS43LDEuMywzLjVjMCwyLjYsMCw0LjYsMCw1LjJjMCwwLjUsMC40LDEuMSwxLjMsMC45YzcuNS0yLjYsMTMtOS43LDEzLTE4LjFDNTEsMjEuOSw0Mi41LDEzLjQsMzIsMTMuNHoiLz48L3N2Zz4%3D)](https://github.com/adafruit/Adafruit_MagTag_PCBs)
[![GitHub Release](https://img.shields.io/github/v/release/OneOfTheInfiniteMonkeys/MTMP?include_prereleases&style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/MTMP/releases)
[![GitHub License](https://img.shields.io/github/license/OneOfTheInfiniteMonkeys/MTMP?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/MTMP/blob/main/LICENSE) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/moreinfo/graphs/commit-activity)
![GitHub repo size](https://img.shields.io/github/repo-size/OneOfTheInfiniteMonkeys/MTMP?style=flat-square)

## Introduction
MagTag MacroPad (MTMP) is a <a href="https://circuitpython.org/" target="_blank">CircuitPython</a> macro pad implementation. Based on Adafruit example code with the addition of a graphic for the e-ink display of the <a href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a> device. The MagTag's inbuilt LED's are sparingly used to indicate MacroPad modes.

<img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTMP/main/images/MagTag-MacroPad-00.png" width="300px" alt="Adafruit Magtag MacroPad in custom case. Imgage copyright (c) 17 Aug 2021 OneOfTheInfiniteMonkeys All Rights Reserved">

Whilst the MagTag inbuilt buttons lack the feel of dedicated key switches, such as the Cherry MX&trade; for example. There are no additional modules or wiring etc. required. Functional clarity benefits from the Magtag's clear e-ink graphic display and LED's which give improved indication of intended button function and macro pad mode(s), whilst being easy on the eye. Functions are kept to a minimum where simplicity is dovetailed with functionality to maintain clarity and ease of operation.

The implementation is intended to allow Zoom&trade; and Teams&trade; user Audio & Video mode toggling in conference usage scenarios. Additionally, via a "Shift" mode the "Consumer Control" function is intended to permit adjustment of the system volume. The "Shift" mode employs a time delay feature which automatically returns functionality to the normal mode following a short peroid of no key press activity.

The Magtag is small and light enough to be held comfortably in the hand during use throughout meetings if desired. Whilst the buttons can be operated readily by the hand holding the unit. Alternatively the unit can be left on the desk as the MagTag's small space claim accommodates the busiest of desks and is readily "parked" for instant access when needed during a meeting for that necessary interjection.


## Installation
Requirements
- <a href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a>
- <a href="https://en.wikipedia.org/wiki/USB-C" target="_blank">USB cable connection to host computer</a>
- <a href="https://downloads.circuitpython.org/bin/adafruit_magtag_2.9_grayscale/en_GB/adafruit-circuitpython-adafruit_magtag_2.9_grayscale-en_GB-6.3.0.uf2" target="_blank">CicruitPython 6.3.0</a>

Copy the files located in the dist folder to the CIRCUITPY folder of the Adafruit MagTag.

Note 
- The implementation does not use WiFi and thus a secrets.py file should not typically be located on the CIRCUITPY drive.
- Following release of <a href="https://github.com/adafruit/circuitpython/releases" target="_blank">CircuitPython 7</a> to stable, the code will implement switch off of HID disk and serial ports via boot.py

## Notes
The system was implemented for use under with Microsoft Windows&trade; and may function with other operating environments, though this has not been evaluated.

Registered trademarks are owned by their respective registrants.
