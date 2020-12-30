#WNStation development notes

##National Weather Serivce data

To find NWS office and grid coordinates, based on lat / long: [https://api.weather.gov/points/40.62,-96.95](https://api.weather.gov/points/40.62,-96.95)

Data fetched from the above, for Crete, NE: Office = OAX, gridX = 47, gridY = 30

Forecast url should be [https://api.weather.gov/gridpoints/OAX/47,30/forecast](https://api.weather.gov/gridpoints/OAX/47,30/forecast)

Current conditions for closest station (Lincoln airport) [https://api.weather.gov/stations/KLNK/observations/latest](https://api.weather.gov/stations/KLNK/observations/latest)