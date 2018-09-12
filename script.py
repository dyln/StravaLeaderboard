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


segments_url = 'https://www.strava.com/api/v3/segments/explore?bounds=41.031471,28.007190,41.141815,29.913041&activity_type=riding&access_token=418172ed16941e70d4ad096e00315d49260aaa3a'
segments_raw = urllib2.urlopen(segments_url)
segments = json.load(segments_raw)


#print (data['segments'])
pairs = {}
for x in segments['segments']:
    #print("Name: "+ x['name'] + " ID: "+ str(x['id']) )
    id=x['id']
    leaderboard_url = 'https://www.strava.com/api/v3/segments/'+str(id)+'/leaderboard?&per_page=50&access_token=418172ed16941e70d4ad096e00315d49260aaa3a'    
    leaderboard_raw = urllib2.urlopen(leaderboard_url)
    pairs[x['id']]= json.load(leaderboard_raw)
    #print("")

print (pairs)

#pairs[4146113]['entries'][0] --> first of the first segment
names = []
for x in pairs:
    for y in pairs[x]['entries']:
        names.append(y['athlete_name'])

def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return len(result)
        result.append(offset)

result = {}
for x in names:
    result[x]=indices(names,x)

for a in result:
    print ("Name: "+ a + " Count: "+str(result[a]))

#!TODO;
#   -delete users with only one entry
#   -make a point formula:
#       *based on entry count and/or efford and/or speed
#       *make dictionary sorted
#   -is it done? or it should be in a framework or something like that?
#   -test
