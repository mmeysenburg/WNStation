"""
Class representing the ePaper display in the Meysenburg Press
ePaper application

Mark M. Meysenburg
12/30/2020
"""

# installation-specific code to find the ePaper module
libDir = '/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib'

import os
import sys

if os.path.exists(libDir):
    sys.path.append(libDir)

from waveshare_epd import epd7in5b_HD

class EPDView:
    """
    Class representing the ePaper display in the Meysenburg Press
    ePaper application

    Mark M. Meysenburg
    12/30/2020
    """
    def __init__(self):
        """
        Construct the EPDView object.
        """
        self.__epd = epd7in5b_HD.EPD()
        self.__epd.init()
        self.__epd.Clear()

    def draw(self, blackLayer, redLayer):
        """
        Draw the content to the ePaper display.

        parameters
        ----------
        blackLayer : PIL image
            Black layer for the display
        redLayer : PIL image
            Red layer for the display
        """
        self.__epd.display(self.__epd.getbuffer(blackLayer) ,self.__epd.getbuffer(redLayer))

    def clear(self):
        """
        Clear the display.
        """
        self.__epd.Clear()