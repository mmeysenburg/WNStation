from PIL import Image, ImageDraw, ImageFont
import socket
import time
from model import NewsAPIReader, NWSReader
import netifaces as ni
import datetime

libDir = '/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib'

import os
import sys

if os.path.exists(libDir):
    sys.path.append(libDir)

from waveshare_epd import epd7in5b_HD


def formatDisplayText(text, maxWidth, font):
    """Format a string as a pseudo-justified text for the display.

    text - text to format
    maxWidth - maximum width, in pixels, for the text on the display
    font - ImageFont object used to display the text
    """
    import pyphen

    pyphen.language_fallback('en_US')
    dic = pyphen.Pyphen(lang='en_US')

    hlWords = text.split()
    lines = 0
    hl = ''
    hll = ''

    # place all the words in the headline
    for word in hlWords:
        # if the word fits, just add it
        if font.getsize(hll + word + ' ')[0] < maxWidth:
            hll = hll + word + ' '
        else:
            # if the word doesn't fit, try to hypenate
            hyphenatedWord = dic.inserted(word)
            if '-' in hyphenatedWord:
                brokenWord = hyphenatedWord.split('-')
                bwIdx = 0
                tempHll = hll[:]
                # see how many chunks we can add to the end of the line
                while font.getsize(tempHll + brokenWord[bwIdx] + '-')[0] < maxWidth:
                    tempHll += brokenWord[bwIdx]
                    bwIdx += 1
                # did we add any chunks?
                if bwIdx > 0:
                    if len(hl) == 0:
                        hl = tempHll + '-'
                    else:
                        hl += '\n' + tempHll + '-'
                    hll = ''.join(brokenWord[bwIdx:]) + ' '
                    lines += 1
                else:
                    if len(hl) == 0:
                        hl = hll[:]
                    else:
                        hl += '\n' + hll
                    hll = word + ' '
                    lines += 1
            else:
                # if we can't hyphenate, add word to next line
                if len(hl) == 0:
                    hl = hll[:]
                else:
                    hl += '\n' + hll
                hll = word + ' '
                lines += 1

    # add last line to the headline
    if len(hl) == 0:
        hl = hll[:]
    else:
        hl += '\n' + hll
    lines += 1

    # calculate height, in pixels, of the whole headline
    height = font.getsize(hl)[1] * lines

    # send back formatted headline and height as a tuple
    return (hl, height)
        

epd = epd7in5b_HD.EPD()
epd.init()
epd.Clear()

while True:
    # constants for positioning content
    BASE_HEADLINE_Y = 70
    COL_1_X = 5
    COL_2_X = 298
    COL_3_X = 592
    NEWS_WIDTH = 280

    # fonts for display
    headlineFont = ImageFont.truetype('./times.ttf', 22)
    newsFont = ImageFont.truetype('./times.ttf', 18)

    # get three random headlines
    napir = NewsAPIReader.NewsAPIReader('ae277ae39eb84b0eb01efeae417fe724')
    headlines = napir.getRandomHeadlines(3)

    # get weather info
    NWSStation = 'KLNK'
    NWSOffice = 'OAX'
    NWSGridX = '47'
    NWSGridY = '30'
    nwsr = NWSReader.NWSReader(NWSOffice, NWSGridX, NWSGridY, NWSStation)
    currentConditions = nwsr.getCurrentConditions()
    forecast = nwsr.getForecast()

    # look up wifi address of pi via ifconfig   
    ipAddress = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

    # create black layer for composite image
    blackLayer = Image.open('blackLayer.bmp')
    blackLayer.load()
    blackLayerDraw = ImageDraw.Draw(blackLayer)

    # first news item
    (hl, height) = formatDisplayText(headlines[0][0], NEWS_WIDTH, headlineFont)
    blackLayerDraw.text((COL_1_X, BASE_HEADLINE_Y), hl, font=headlineFont)
    (text, textHeight) = formatDisplayText(headlines[0][1], NEWS_WIDTH, newsFont)
    blackLayerDraw.text((COL_1_X, BASE_HEADLINE_Y + height + 5), text, font=newsFont)

    # second news item
    (hl, height) = formatDisplayText(headlines[1][0], NEWS_WIDTH, headlineFont)
    blackLayerDraw.text((COL_2_X, BASE_HEADLINE_Y), hl, font=headlineFont)
    (text, textHeight) = formatDisplayText(headlines[1][1], NEWS_WIDTH, newsFont)
    blackLayerDraw.text((COL_2_X, BASE_HEADLINE_Y + height + 5), text, font=newsFont)

    # third news item
    (hl, height) = formatDisplayText(headlines[2][0], NEWS_WIDTH, headlineFont)
    blackLayerDraw.text((COL_3_X, BASE_HEADLINE_Y), hl, font=headlineFont)
    (text, textHeight) = formatDisplayText(headlines[2][1], NEWS_WIDTH, newsFont)
    blackLayerDraw.text((COL_3_X, BASE_HEADLINE_Y + height + 5), text, font=newsFont)

    # create red layer for composite image
    redLayer = Image.open('redLayer.bmp')
    redLayer.load()
    redLayerDraw = ImageDraw.Draw(redLayer)

    # IP address to allow VNC access
    redLayerDraw.text((5, 505), ipAddress, font=newsFont)

    # day, date
    today = datetime.datetime.today()
    dayDate = today.strftime('%a, %d %b %y')
    redLayerDraw.text((10, 7), dayDate, font=newsFont)

    # time
    currTime = today.strftime('%H:%M:%S')
    redLayerDraw.text((790, 505), currTime, font=newsFont)

    # current temperature / conditions
    redLayerDraw.text((670, 5), currentConditions['temp'] + ' ' + currentConditions['text'], font=newsFont)

    # push to display
    epd.display(epd.getbuffer(blackLayer) ,epd.getbuffer(redLayer))
    
    import time
    epd.sleep()
    time.sleep(60*10)
    
    epd.Clear()