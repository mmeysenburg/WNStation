class ImageMaker:
    """
    Class for making the black and red image layers for the 
    Meysenburg Press ePaper application.

    Mark M. Meysenburg
    12/29/2020
    """

    def __init__(self):
        """
        Construct the ImageMaker object.
        """
        from PIL import ImageFont

        # constants for positioning content
        self.__BASE_HEADLINE_Y = 70
        self.__COL_1_X = 5
        self.__COL_2_X = 298
        self.__COL_3_X = 592
        self.__NEWS_WIDTH = 280
        self.__WX_WIDTH = 176
        self.__BASE_WX_Y = 405

        # fonts for text on the image
        self.__headlineFont = ImageFont.truetype('./model/times.ttf', 22)
        self.__newsFont = ImageFont.truetype('./model/times.ttf', 18)
        self.__bigHeadlineFont = ImageFont.truetype('./model/times.ttf', 26)
        self.__bigNewsFont = ImageFont.truetype('./model/times.ttf', 22)

    def makeBlackImage(self, news, wxConditions, wxForecast):
        """
        Make the black part of the image to place on the display.

        parameters
        ----------
        news : list
            List of 3 (headline, contents) tuples with news items.
        wxConditions : list
            List of dictionaries with current weather conditions.
        wxForecast : list
            List of dictionaries with weather forecast.

        returns
        -------
            Single-channel image that will be the black layer in the
            display.
        """
        from PIL import Image, ImageDraw

        # create black layer for composite image
        blackLayer = Image.open('./model/blackLayer.bmp')
        blackLayer.load()
        blackLayerDraw = ImageDraw.Draw(blackLayer)

        # first news item
        (a, b) = news[0]
        (hl, height) = self.__formatJustifiedText(a, self.__NEWS_WIDTH, self.__bigHeadlineFont)
        blackLayerDraw.text((self.__COL_1_X, self.__BASE_HEADLINE_Y), hl, font=self.__bigHeadlineFont)
        (text, textHeight) = self.__formatJustifiedText(b, self.__NEWS_WIDTH, self.__bigNewsFont)
        blackLayerDraw.text((self.__COL_1_X, self.__BASE_HEADLINE_Y + height + 5), text, font=self.__bigNewsFont)

        # second news item
        (a, b) = news[1]
        (hl, height) = self.__formatJustifiedText(a, self.__NEWS_WIDTH, self.__bigHeadlineFont)
        blackLayerDraw.text((self.__COL_2_X, self.__BASE_HEADLINE_Y), hl, font=self.__bigHeadlineFont)
        (text, textHeight) = self.__formatJustifiedText(b, self.__NEWS_WIDTH, self.__bigNewsFont)
        blackLayerDraw.text((self.__COL_2_X, self.__BASE_HEADLINE_Y + height + 5), text, font=self.__bigNewsFont)

        # third news item
        (a, b) = news[2]
        (hl, height) = self.__formatJustifiedText(a, self.__NEWS_WIDTH, self.__bigHeadlineFont)
        blackLayerDraw.text((self.__COL_3_X, self.__BASE_HEADLINE_Y), hl, font=self.__bigHeadlineFont)
        (text, textHeight) = self.__formatJustifiedText(b, self.__NEWS_WIDTH, self.__bigNewsFont)
        blackLayerDraw.text((self.__COL_3_X, self.__BASE_HEADLINE_Y + height + 5), text, font=self.__bigNewsFont)

        # weather forecast
        for i, fc in enumerate(wxForecast):
            if i < 5:
                fcName = fc['name']
                fcTemp = str(fc['temperature'])
                fcFC = fc['shortForecast']

                (day, offset, dayHeight) = self.__formatCenteredText(fcName,
                    self.__WX_WIDTH, self.__headlineFont)
                blackLayerDraw.text((self.__WX_WIDTH * i + offset, self.__BASE_WX_Y),
                    day, font=self.__headlineFont)
                # (day, dayHeight) = self.__formatJustifiedText(fcName, self.__WX_WIDTH, self.__headlineFont)
                # blackLayerDraw.text((self.__WX_WIDTH * i + 5, self.__BASE_WX_Y), day, font=self.__headlineFont)

                (temp, offset, tempHeight) = self.__formatCenteredText(fcTemp,
                    self.__WX_WIDTH, self.__newsFont)
                blackLayerDraw.text((self.__WX_WIDTH * i + offset, self.__BASE_WX_Y + dayHeight + 5),
                    temp, font=self.__newsFont)
                # (temp, tempHeight) = self.__formatJustifiedText(fcTemp, self.__WX_WIDTH, self.__newsFont)
                # blackLayerDraw.text((self.__WX_WIDTH * i + 5, self.__BASE_WX_Y + dayHeight + 5), temp, font=self.__newsFont)

                # (fcText, offset, fcHeight) = self.__formatCenteredText(fcFC, 
                #     self.__WX_WIDTH, self.__newsFont)
                # blackLayerDraw.text((self.__WX_WIDTH * i + offset, 
                #     self.__BASE_WX_Y + dayHeight + tempHeight + 10), fcText, 
                #     font=self.__newsFont)
                (fcText, fcHeight) = self.__formatJustifiedText(fcFC, self.__WX_WIDTH, self.__newsFont)
                blackLayerDraw.text((self.__WX_WIDTH * i + 5, self.__BASE_WX_Y + dayHeight + tempHeight + 10), 
                    fcText, font=self.__newsFont)

        # send back the image
        return blackLayer

    def makeRedImage(self, ipAddress, dayDate, currTime, currentConditions):
        """
        Make the black part of the image to place on the display.

        parameters
        ----------
        ipAddress : str
            IP address of the display Pi
        dayDate : str
            Current day and date
        currTime : str
            Current time
        currentConditions : list
            List of dictionaries representing the current conditions

        returns
        -------
            Single-channel image that will be the red layer in the
            display.
        """
        from PIL import Image, ImageDraw

        # create red layer for composite image
        redLayer = Image.open('./model/redLayer.bmp')
        redLayer.load()
        redLayerDraw = ImageDraw.Draw(redLayer)

        # IP address
        redLayerDraw.text((5, 505), ipAddress, font=self.__newsFont)

        # day / date
        offset = (220 - self.__newsFont.getsize(dayDate)[0]) // 2
        redLayerDraw.text((offset, 7), dayDate, font=self.__newsFont)

        # current time
        redLayerDraw.text((790, 505), currTime, font=self.__newsFont)

        # current temperature / conditions
        text = currentConditions['temp'] + ' ' + currentConditions['text']
        offset = (220 - self.__newsFont.getsize(text)[0]) // 2
        redLayerDraw.text((660 + offset, 5), text, 
            font=self.__newsFont)

        # send back the image layer
        return redLayer

    def __formatCenteredText(self, text, width, font):
        """
        Format a string as centered in a given width for the display.

        parameters
        ----------
        text : str
            Text to center
        width : int
            Width, in pixels, to center in
        font : ImageFont
            Font used to display the text

        returns
        -------
            (text, offset, height) tuple: text is the text to be displayed
            (possibly stretched across multiple lines), offset
            is # of x-dimension pixels to offset by to center the 
            text, and height is the height of the chunk of text
        """
        returnText = text[:]
        offset = 0

        # single line or multi-line case?
        origWidth = font.getsize(text)[0]
        if origWidth <= width: 
            # don't split line, just center
            offset = (width - origWidth) // 2
        else:
            # hopefully a too-long line is multiple words
            splitText = text.split()
            if len(splitText) > 1:
                returnText = splitText[0][:]
                for word in splitText[1:]:
                    tempText = returnText + ' ' + word
                    if font.getsize(tempText)[0] <= width:
                        returnText += ' ' + word
                    else:
                        returnText += '\n' + word
                newWidth = font.getsize(returnText)[0]
                offset = (width - newWidth) // 2

        height = font.getsize(returnText)[1]
        return (returnText, offset, height)

    def __formatJustifiedText(self, text, maxWidth, font):
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
        height = font.getsize(text)[1]

        try:
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

        except IndexError:
            print('Trapped IndexError')

        # send back formatted headline and height as a tuple
        return (hl, height)
