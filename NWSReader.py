class NWSReader:
    """Class for reading NWS weather data from the Web."""

    def __init__(self, NWSOffice, NWSGridX, NWSGridY, NWSStation):
        """NOAAReader constructor."""
        self.__NWSOffice__ = NWSOffice
        self.__NWSGridX__ = NWSGridX
        self.__NWSGridY__ = NWSGridY
        self.__NWSStation__ = NWSStation

    def getCurrendObsJSON(self):
        """Get most current weather info for the specified location."""
        import urllib.request

        url = 'https://api.weather.gov/stations/{0:s}/observations/latest'.format(self.__NWSStation__)
        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

    def getForecast(self):
        """Get forecast for the specified location."""
        import urllib.request
        
        url = 'https://api.weather.gov/gridpoints/{0:s}/{1:s},{2:s}/forecast'.format(self.__NWSOffice__, 
            self.__NWSGridX__, self.__NWSGridY__)

        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        return jsonString

NWSStation = 'KLNK'
NWSOffice = 'OAX'
NWSGridX = '47'
NWSGridY = '30'
nws = NWSReader(NWSOffice, NWSGridX, NWSGridY, NWSStation)
print(nws.getCurrendObsJSON())
print('*************************')
print(nws.getForecast())
