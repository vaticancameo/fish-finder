import requests
import json
import urllib
import os

token = os.environ['NOAA_API_TOKEN']

stations = [9410170, 9410230, 9410660, 9410840, 9411340, 9411406, 9412110,
          9413450, 9414290, 9414750, 9414523, 9414575, 9414863, 9415102,
          9415144, 9414958, 9415020, 9416841, 9418767, 9419750]

# http://opendap.co-ops.nos.noaa.gov/axis/webservices/highlowtidepred/
# response.jsp?stationId=9414958&beginDate=20160810&endDate=20160812
# &datum=MLLW&unit=0&timeZone=0&format=xml&Submit=Submit
def retrieve_tides(stations):
    """ Retrieve high and low tides for specific station within date range """

    base_url = "http://tidesandcurrents.noaa.gov/api/datagetter"

    for station in stations:
        params = {"station": station,
                  # "begin_date": "20160731 00:00",
                  # "end_date": "20160802 00:00",
                  "date": "today",
                  "time_zone": "lst_ldt",
                  "units": "english",
                  "product": "predictions",
                  "format": "json",
                  "datum": "MLLW",
                  "interval": "h",
                  "application": "hackbright_academy"
                  }

        res = requests.get(base_url, params=params)
        print res.content
    # print res.json()



def check_api():

    url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    header = {"token": token}
    p = {}

    resp = requests.get(url, params=p, headers=header)
    print resp.json()


if __name__ == "__main__":
    retrieve_tides(stations)