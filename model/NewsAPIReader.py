class NewsAPIReader:
    """Class for reading NewsAPI headlines from the Web."""

    def __init__(self, apiKey):
        """Constructor for the NewsAPIReader class.

        apiKey - API key for accessing headlines from newsapi.org
        """

        self.__apiKey = apiKey

    def _getNewsAPIJSON(self):
        """Get headline data from newsapi.org as a JSON object."""
        import urllib.request

        url = 'http://newsapi.org/v2/top-headlines?country=us&apiKey=' + self.__apiKey

        jsonString = ''
        with urllib.request.urlopen(url) as response:
            jsonString = response.read()

        import json
        return json.loads(jsonString)

    def getRandomHeadlines(self, n):
        """Get n random headlines from newsapi.org."""
        
        json = self._getNewsAPIJSON()
        nH = json['totalResults']
        if n > nH:
            n = nH
        articles = json['articles']

        import random
        headlines = []
        for i in range(n):
            headlines.append(articles.pop(random.randint(0, len(articles) - 1))['title'])

        return headlines

    def getAllHeadlines(self):
        """Get all of the current headlines from newsapi.org."""

        json = self._getNewsAPIJSON()
        aritcles = json['articles']
        headlines = [a['title'] for a in aritcles]
        return headlines

'''
# standalone test code
napir = NewsAPIReader('ae277ae39eb84b0eb01efeae417fe724')
print(napir.getRandomHeadlines(5))
print(napir.getAllHeadlines())
'''