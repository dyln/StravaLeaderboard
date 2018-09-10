import json
import urllib2

access_token = '418172ed16941e70d4ad096e00315d49260aaa3a'

#The latitude and longitude for two points describing a rectangular boundary for the search: 
#[southwest corner latitutde,
#southwest corner longitude, 
#northeast corner latitude, 
#northeast corner longitude]
#ISTANBUL
bounds = [41.031471, 28.007190, 41.141815, 29.913041]
url = 'https://www.strava.com/api/v3/segments/explore?bounds=41.031471,28.007190,41.141815,29.913041&activity_type=riding&access_token=418172ed16941e70d4ad096e00315d49260aaa3a'

#http = urllib3.PoolManager()
#response = http.request('GET', url)

json_obj = urllib2.urlopen(url)

data = json.load(json_obj)

print (data[])