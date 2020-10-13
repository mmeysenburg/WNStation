class NOAAReader:
    """Class for reading NOAA weather data from the Web. Currently non-functional."""

    def __init__(self, FIPS, token):
        """NOAAReader constructor."""
        self.__BASE_URL__ = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
        self.__FIPS__ = FIPS
        self.__token__ = token

    def __getDateString__(self):
        """Get the current date in YYYY-MM-DD format"""
        from datetime import datetime
        time = str(datetime.now())
        ymd = time.split()[0]
        return ymd

    def getWxJSON(self):
        """Get most current weather info for the specified location."""
        import urllib.parse
        import urllib.request

        url = self.__BASE_URL__ + "?locationid=FIPS:" + self.__FIPS__ #+ "&startdate=" + self.__getDateString__()
        values = {'Token' : self.__token__, 'Accept' : 'application/json'}

        data = urllib.parse.urlencode(values)

        req = urllib.request.Request(url + "?" + data)
        print(url + '&Token=' + self.__token__ + '&Accept=application/json')
        jsonString = ''
        with urllib.request.urlopen(url + '&Token=' + self.__token__ + '&Accept=application/json') as response:
            jsonString = response.read()

        return jsonString

FIPS = "31-11370"
TOKEN = "cCbLnBKBVLmTUHrhHYDcgubRmZctVEKf"
n = NOAAReader(FIPS, TOKEN)
print(n.getWxJSON())
