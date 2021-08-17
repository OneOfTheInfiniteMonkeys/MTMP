# MTMP (MagTag MacroPad)
## Introduction
MagTag MacroPad (MTMP) is a <a href="https://circuitpython.org/" target="_blank">CircuitPython</a> macro pad implementation. Based on Adafruit example code with the addition of a graphic for the e-ink display of the <a href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a> device. The MagTag's inbuilt LED's are sparingly used to indicate MacroPad modes.

Whilst the MagTag inbuilt buttons lack the feel of dedicated key switches, such as the Cherry MX&trade; for example. There are no additional modules or wiring etc. required. Functional clarity benefits from the Magtag's clear e-ink graphic display and LED's which give improved indication of intended button function and macro pad mode(s), whilst being easy on the eye. Functions are kept to a minimum where simplicity is dovetailed with functionality to maintain clarity and ease of operation.

The implementation is intended to allow Zoom&trade; and Teams&trade; user Audio & Video mode toggling in conference usage scenarios. Additionally, via a "Shift" mode the "Consumer Control" function is intended to permit adjustment of the system volume. The "Shift" mode employs a time delay feature which automatically returns functionality to the normal mode following a short peroid of no key press activity.

The Magtag is small and light enough to be held comfortably in the hand during use throughout meetings if desired. Whilst the buttons can be operated readily by the hand holding the unit. Alternatively the unit can be left on the desk as the MagTag's small space claim accommodates the busiest of desks and is readily "parked" for instant access when needed during a meeting for that necessary interjection.

<img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTMP/main/images/MagTag-MacroPad-00.png" width="300px" alt="Adafruit Magtag MacroPad in custom case. Imgage copyright (c) 17 Aug 2021 OneOfTheInfiniteMonkeys All Rights Reserved">


## Installation
Requirements
- Adafruit Magtag
- USB cable connection to host computer
- CicruitPython 6.3.0

Copy the files located in the dist folder to the CIRCUITPY folder of the Adafruit MagTag.

Note the implementation does not use WiFi and thus a secrets.py file should not typically be located on the CIRCUITPY drive.


## Notes
The system was implemented for use under with Microsoft Windows&trade; and may function with other operating environments, though this has not been evaluated.

Registered trademarks are owned by their respective registrants.
