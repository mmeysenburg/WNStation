"""E-Paper view for news / weather station."""
libDir = '/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib'

import os
import sys

if os.path.exists(libDir):
    sys.path.append(libDir)

import socket
import time
from model import NewsAPIReader
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd7in5b_HD

epd = epd7in5b_HD.EPD()
epd.init()
epd.Clear()

epd.Dev_exit()