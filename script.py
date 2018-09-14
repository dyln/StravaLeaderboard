import json
import urllib2
import operator

access_token = '418172ed16941e70d4ad096e00315d49260aaa3a'
#The latitude and longitude for two points describing a rectangular boundary for the search: 
#[southwest corner latitutde,
#southwest corner longitude, 
#northeast corner latitude, 
#northeast corner longitude]
#ISTANBUL
bounds = [41.031471, 28.007190, 41.141815, 29.913041]

segments_url= 'https://www.strava.com/api/v3/segments/explore?bounds='+str(bounds[0])+','+str(bounds[1])+','+str(bounds[2])+','+str(bounds[3])+'&activity_type=riding&access_token='+access_token
segments_raw = urllib2.urlopen(segments_url)
segments = json.load(segments_raw)

pairs = {}
for x in segments['segments']:
    #print("Name: "+ x['name'] + " ID: "+ str(x['id']) )
    id=x['id']
    leaderboard_url = 'https://www.strava.com/api/v3/segments/'+str(id)+'/leaderboard?&per_page=50&access_token='+access_token    
    leaderboard_raw = urllib2.urlopen(leaderboard_url)
    pairs[x['id']]= json.load(leaderboard_raw)
    #print("")

#print (pairs)

#pairs[4146113]['entries'][0] --> first of the first segment
names = []
for x in pairs:
    for y in pairs[x]['entries']:
        names.append(y['athlete_name'])

#how many enteries per user    
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
    y=indices(names,x)
    if (y>1):
        result[x]=y


#sorted_x = sorted(x.items(), key=operator.itemgetter(1))
sorted_results = sorted(result.items(), key=lambda x: x[1],reverse=True)
#print(sorted_results)
for a in sorted_results:
    print ("Name: "+ a[0] + " Count: "+str(a[1]))
    


#!TODO;
#   -delete users with only one entry XXXXX
#   -make a point formula:
#       *based on entry count and/or efford and/or speed
#       *make dictionary sorted XXXXX
#   -is it done? or it should be in a framework or something like that?
#   -test
