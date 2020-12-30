class NWSReader:
    """Class for reading NWS weather data from the Web."""

    def __init__(self, NWSOffice, NWSGridX, NWSGridY, NWSStation):
        """NOAAReader constructor.
        
        NWSOffice - code of NWS forecast office for forecast queries
        NWSGridX - NWS Grid X coordinate for forecast
        NWSGridY - NWS Grid Y coordinate for forecast
        NWSStation - code of NWS weather station for condition queries
        """
        self._NWSOffice = NWSOffice
        self._NWSGridX = NWSGridX
        self._NWSGridY = NWSGridY
        self._NWSStation = NWSStation

    def _degreesToCardinal(self, degrees):
        """Get the string cardinal direction closest to the specified degrees.
        
        degrees - wind direction angle in degrees
        """
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

    def _getCurrentObsString(self):
        """Get most current weather info for the specified location."""
        import urllib.request

        url = 'https://api.weather.gov/stations/{0:s}/observations/latest'.format(self._NWSStation)
        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

    def _getForecastString(self):
        """Get forecast for the specified location."""
        import urllib.request
        
        url = 'https://api.weather.gov/gridpoints/{0:s}/{1:s},{2:s}/forecast'.format(self._NWSOffice, 
            self._NWSGridX, self._NWSGridY)

        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

    def getForecast(self):
        """Get the current forecast as a list of dictionaries."""
        import json
        import urllib.error

        forecasts = []

        try:
            forecasts = json.loads(self._getForecastString())['properties']['periods']
        except urllib.error.HTTPError:
            print('trapped HTTPError')

        return forecasts

    def getCurrentConditions(self):
        """Get the most current weather conditions as a list of dictionaries."""

        import json
        obsDict = json.loads(self._getCurrentObsString())

        temp = obsDict['properties']['temperature']['value']
        if temp is not None:
            temp = int((temp * 9.0 / 5.0) + 32.0)

        deg = obsDict['properties']['windDirection']['value']

        speed = obsDict['properties']['windSpeed']['value']
        if speed is not None:
            speed /= 1.609

        ret = {}
        ret['temp'] = str(temp) + '°'
        ret['windDirection'] = self._degreesToCardinal(deg)
        ret['windSpeed'] = speed
        ret['text'] = obsDict['properties']['textDescription']

        return ret


# standalone test code
# NWSStation = 'KLNK'
# NWSOffice = 'OAX'
# NWSGridX = '47'
# NWSGridY = '30'
# nws = NWSReader(NWSOffice, NWSGridX, NWSGridY, NWSStation)
# print(nws.getCurrentConditions())
# print(nws.getForecast())
