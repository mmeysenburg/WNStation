import http.client

conn = http.client.HTTPSConnection("bing-news-search1.p.rapidapi.com")

headers = {
    'x-bingapis-sdk': "true",
    'x-rapidapi-key': "8934f57711msh999750e1c845c6dp161cdejsn6cb28b671346",
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
    }

conn.request("GET", "/news?safeSearch=Off&textFormat=Raw", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))