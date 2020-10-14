class NWSReader:
    """Class for reading NWS weather data from the Web."""

    def __init__(self, NWSOffice, NWSGridX, NWSGridY, NWSStation):
        """NOAAReader constructor."""
        self.__NWSOffice__ = NWSOffice
        self.__NWSGridX__ = NWSGridX
        self.__NWSGridY__ = NWSGridY
        self.__NWSStation__ = NWSStation

    def __degreesToCardinal__(self, degrees):
        """Get the cardinal direction closest to the specified degrees."""
        import sys

        values = [[0, 'N'], [22.5, 'NNE'], [45, 'NE'], [67.5, 'ENE'],
            [90, 'E'], [112.5, 'ESE'], [135, 'SE'], [157.5, 'SSE'],
            [180, 'S'], [202.5, 'SSW'], [225, 'SW'], [247.5, 'WSW'],
            [270, 'W'], [292.5, 'WNW'], [315, 'NW'], [337.5, 'NNW']]

        min = sys.float_info.max
        minIdx = -1
        for i, val in enumerate(values):
            if val[0] < min:
                min = val[0]
                minIdx = i
        return values[i][1]

    def __getCurrentObsString__(self):
        """Get most current weather info for the specified location."""
        import urllib.request

        url = 'https://api.weather.gov/stations/{0:s}/observations/latest'.format(self.__NWSStation__)
        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

    def __getForecastString__(self):
        """Get forecast for the specified location."""
        import urllib.request
        
        url = 'https://api.weather.gov/gridpoints/{0:s}/{1:s},{2:s}/forecast'.format(self.__NWSOffice__, 
            self.__NWSGridX__, self.__NWSGridY__)

        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

    def getCurrentConditions(self):
        """Get the most current weather conditions in a list."""

        import json
        obsDict = json.loads(self.__getCurrentObsString__())

        temp = obsDict['properties']['temperature']['value']
        temp = int((temp * 9.0 / 5.0) + 32.0)

        deg = obsDict['properties']['windDirection']['value']

        speed = obsDict['properties']['windSpeed']['value']
        speed /= 1.609

        ret = {}
        ret['temp'] = temp
        ret['windDirection'] = self.__degreesToCardinal__(deg)
        ret['windSpeed'] = speed
        ret['text'] = obsDict['properties']['textDescription']

        return ret

NWSStation = 'KLNK'
NWSOffice = 'OAX'
NWSGridX = '47'
NWSGridY = '30'
nws = NWSReader(NWSOffice, NWSGridX, NWSGridY, NWSStation)
print(nws.getCurrentConditions())
