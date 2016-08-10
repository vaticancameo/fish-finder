import requests
import json
import urllib
import os

token = os.environ['NOAA_API_TOKEN']


def retrieve_tides():
  """ Retrieve high and low tides for specific station within date range """

    base_url = "http://tidesandcurrents.noaa.gov/api/datagetter"

    params = {"station": "9414958",
              "begin_date": "20160707 00:00",
              "end_date": "20160708 00:00",
              # "date": "today",
              "time_zone": "gmt",
              "units": "english",
              "product": "high_low",
              "format": "json",
              "datum": "MLLW"
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
    retrieve_tides()