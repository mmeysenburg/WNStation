class BingNewsAPIReader:
    """
    Class for getting random news content from the Bing News Search API.
    Searches at the free tier are limited to 1000 per month, <= 3 per second.

    Mark M. Meysenburg
    12/29/2020
    """

    def __init__(self, apiKey):
        """
        Construct a new BingNewsAPIReader parameterized with the specified key.

        parameters
        ----------
        apiKey : str
            API key allowing access to the Bing News Search API.
        """
        self.__apiKey = apiKey
        self.__results = { }

    def updateContent(self):
        """
        Update the set of headlines / partial contents persisting in this object.
        This method should be called no more than hourly, so as to not exhaust the
        number of queries allowed by the Bing News Service API.
        """
        results = self.__queryAPI()
        self.__results.clear()

        for i, (headline, content) in enumerate(results):
            self.__results[i] = (headline, content)


    def getRandomContent(self, n):
        """
        Get up to n random pieces of content from the API. Returns results from the
        persistent set, which is updated no more than hourly by calling updateContent.

        parameters
        ----------
        n : int
            Maximum number of content pieces to return
        
        returns
        -------
            List of up to n tuples, each of the form ("headline", "abbr. content")
        """
        import random

        returnList = [(x[0], x[1]) for x in self.__results.values()]
        random.shuffle(returnList)

        return returnList[:n]

    def __queryAPI(self):
        """
        Query the API and return list of headlines and contents
        """
        import http.client
        import json

        conn = http.client.HTTPSConnection("bing-news-search1.p.rapidapi.com")

        headers = {
            'x-bingapis-sdk': "true",
            'x-rapidapi-key': self.__apiKey,
            'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
        }

        conn.request("GET", "/news?safeSearch=Off&textFormat=Raw", headers=headers)

        res = conn.getresponse()
        data = res.read()

        eData = json.loads(data.decode("utf-8"))

        news = [(x.get('name'), x.get('description') + '...') for x in eData.get('value')]

        return news


# stand-alone test code
# bnAPIr = BingNewsAPIReader('8934f57711msh999750e1c845c6dp161cdejsn6cb28b671346')
# bnAPIr.updateContent()
# print(bnAPIr.getRandomContent(3))