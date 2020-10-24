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

# create and show newspaper name and headline fonts
newsPaperFont = ImageFont.truetype('./Chomsky.woff', 40)
headlineFont = ImageFont.truetype('./old-news.ttf', 20)

Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
Other = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
  
napir = NewsAPIReader.NewsAPIReader('ae277ae39eb84b0eb01efeae417fe724')
headlines = napir.getRandomHeadlines(5)
hlString = ''
for hl in headlines:
    hlString += '{0:s}\n'.format(hl)
    
hostname = socket.gethostname()
ipAddress = socket.gethostbyname(hostname)
                
headlineImage = ImageDraw.Draw(Himage)
timeAndIPImage = ImageDraw.Draw(Other)
    
headlineImage.text((5, 5), 'Meysenburg Press', font=newsPaperFont, fill=0)
timeAndIPImage.text((750, 460), ipAddress, font=headlineFont, fill=0)
    
epd.display(epd.getbuffer(Himage) ,epd.getbuffer(Other))


time.sleep(10)
    
epd.init()
epd.Clear()
epd.sleep()
epd.Dev_exit()