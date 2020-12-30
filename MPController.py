"""
Controller for the Meysenburg Press ePaper application.

Usage: python MPController.py [w|r]
"""
import sys
from model import BingNewsAPIReader, GenInfo, ImageMaker, NWSReader

# construct reader objects
newsReader = BingNewsAPIReader.BingNewsAPIReader('8934f57711msh999750e1c845c6dp161cdejsn6cb28b671346')
NWSStation = 'KLNK'
NWSOffice = 'OAX'
NWSGridX = '47'
NWSGridY = '30'
wxReader = NWSReader.NWSReader(NWSOffice, NWSGridX, NWSGridY, NWSStation)
genReader = GenInfo.GenInfo(sys.argv[1].lower())

# construct object for making image layers
imageMaker = ImageMaker.ImageMaker()

# construct the ePaper display object
ePaper = None
if sys.argv[1].lower() == 'r':
    from view import EPDView
    ePaper = EPDView.EPDView()

# counter that restricts news, forecast updates to once an hour
numMinutesSinceLastUpdate = 0

forecast = [] 
while True:
    # if it has been an hour, update news & forecast
    if numMinutesSinceLastUpdate % 60 == 0:
        # TODO: remove print from update code
        print('*** update ***')

        newsReader.updateContent()
        forecast = wxReader.getForecast()
        
        numMinutesSinceLastUpdate = 0

    # update the display image, first black layer
    news = newsReader.getRandomContent(3)
    blackImageLayer = imageMaker.makeBlackImage(news, wxReader.getCurrentConditions(), forecast)

    # then red layer
    ipAddress = genReader.getIPAddress()
    dayDate = genReader.getDayDate()
    currTime = genReader.getCurrentTime()
    currentConditions = wxReader.getCurrentConditions()
    redImageLayer = imageMaker.makeRedImage(ipAddress, dayDate, currTime, currentConditions)

    if sys.argv[1].lower() == 'w':
        # graphic windows test; create and save images, then exit
        blackImageLayer.save('bl.bmp')
        redImageLayer.save('rl.bmp')

        exit()
    elif sys.argv[1].lower() == 'r':
        ePaper.draw(blackImageLayer, redImageLayer)
    else:
        for (headline, content) in news:
            print(numMinutesSinceLastUpdate, headline)
            print('\t', content)
            print(forecast)
            print(wxReader.getCurrentConditions())


    # tick the update counter, sleep for 10 minutes
    numMinutesSinceLastUpdate += 10
    import time
    time.sleep(60 * 10)
    if sys.argv[1].lower() == 'r':
        ePaper.clear()
