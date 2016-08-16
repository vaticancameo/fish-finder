import requests
import json
import urllib
import os

# token = os.environ['NOAA_API_TOKEN']
token = "izzTBSCJqNwpKXnGuotVSePytUlvIUXY"


def retrieve_tides_json(stations):
    """ Retrieve high and low tides for specific station within date range """

    url = "http://tidesandcurrents.noaa.gov/api/datagetter"
# http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20160803%2010:00
# &end_date=20170802%2017:00&station=9415020&product=predictions&datum=navd
# &units=metric&interval=h&time_zone=gmt&format=json
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

    res = requests.get(url, params=params)
    print res.content
    # print res.json()


def retrieve_tides_soap():
    """ Retrieve high and low tides for specific station within date range """

    stations = [9410170, 9410230, 9410580, 9410680, 9410660, 9410840, 9411340, 9411399, 9411406, 9412110, 9412802, 9413450, 9413663, 9414131, 9414290, 9414317, 9414764, 9414750, 9414746, 9414358, 9414688, 9414458, 9414523, 9414509, 9414575, 9414863, 9415218, 9415143, 9415102, 9415265, 9415144, 9414811, 9415112, 9415064, 9415316, 9415056, 9415338, 9414958, 9415020, 9416409, 9416841, 9417426, 9418767, 9418723, 9418817, 9419750, 9419945]

    url = "http://opendap.co-ops.nos.noaa.gov/axis/webservices/highlowtidepred/response.jsp"
# http://opendap.co-ops.nos.noaa.gov/axis/webservices/highlowtidepred/
# response.jsp?stationId=9414958&beginDate=20160810&endDate=20160812
# &datum=MLLW&unit=0&timeZone=0&format=xml&Submit=Submit
    for station in stations:
        params = {"stationId": station,
                  "beginDate": "20160801",
                  "endDate": "20160803",
                  "timeZone": "1",
                  "unit": "0",
                  "format": "text",
                  "datum": "MLLW",
                  "Submit": "Submit"
                  }

        res = requests.get(url, params=params)
        data = res.content.split('<pre>')[-1]
        data = data.replace('</pre>', '')

        f = open(str(station), 'w')

        f.write(data)

        f.close()

def check_api():

    url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    header = {"token": token}
    p = {}

    resp = requests.get(url, params=p, headers=header)
    print resp.json()


if __name__ == "__main__":
    retrieve_tides_soap()