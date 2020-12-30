class GenInfo:
    """
    Class to gather and return general information for the 
    Meysenburg Press ePaper application.

    Mark M. Meysenburg
    12/30/2020
    """

    def __init__(self, winOrPi):
        """
        Construct the GenInfo object, parameterized for the 
        proper operating system.

        parameters
        ----------
        winOrPi : str
            'w' or 'r', for Windows (test / development) or Raspberry
            Pi ("production") environment
        """
        self.__winOrPi = winOrPi

    def getDayDate(self):
        """
        Return the current day and date, formatted like
        'Wed, 30 Dec 20'
        """
        import datetime
        today = datetime.datetime.today()
        dayDate = today.strftime('%a, %d %b %y')
        return dayDate

    def getCurrentTime(self):
        """
        Return the current time, formatted like 
        '09:55:21'
        """
        import datetime
        today = datetime.datetime.today()
        currTime = today.strftime('%H:%M:%S')
        return currTime

    def getIPAddress(self):
        """
        Return the IP address of the display system.
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP