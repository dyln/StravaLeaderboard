import json
import urllib2
import operator
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'

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
        
#print ('##########################################')
#print ('############ ENDPOINT 1 ##################')
#sorted_x = sorted(x.items(), key=operator.itemgetter(1))
sorted_results = sorted(result.items(), key=lambda x: x[1],reverse=True)
#print(sorted_results)
#for a in sorted_results:
#    print ("Name: "+ a[0] + " Count: "+str(a[1])) ##### ENDPOINT 1

LeaderBoard = {}
for x in names:
    LeaderBoard[x]=[]

for y in pairs:
    for x in pairs[y]['entries']:
        #for y in names:
            #if x['athlete_name'] == y:
                #updateLeaderboard(LeaderBoard,x['athlete_name'],x['rank'])
                #print(y)
                if x['rank'] > 39:
                    #print x['rank']
                    #LeaderBoard.update({x['athlete_name'] : 1 })
                    LeaderBoard[x['athlete_name']].append(1)
                    #LeaderBoard[x['athlete_name']].append(x['rank'])
                if x['rank']<40:
                    LeaderBoard[x['athlete_name']].append(41-x['rank'])

#for x in LeaderBoard:
FinalStandings = {}
for x in LeaderBoard:
    temp=[]
    score=0
    temp = LeaderBoard[x]
    for a in temp:
        score=score + a
    FinalStandings[x] = score

#print ('##########################################')
#print ('############ ENDPOINT 2 ##################')
FinalStanding = sorted(FinalStandings.items(), key=lambda x: x[1],reverse=True)
#print(sorted_results)
#for a in FinalStanding:
#    if a[1]>1:
#        print ("Name: "+ a[0] + " Score: "+str(a[1])) ##### ENDPOINT 1

#print ('##########################################')


@app.route("/")
def hello():
    return "<p>Hello</p> <p>To see the Endpoint 1 <a href = 'http://127.0.0.1:5000/endpoint1'>click here</a></p> <p>To see the Endpoint 2 <a href = 'http://127.0.0.1:5000/endpoint2'>click here</a></p> "

@app.route("/endpoint1")
def e1():
    output1 = "<style>table {border-collapse: collapse;}th, td {border: 2px solid;}</style>##########################################</br>############ ENDPOINT 1 ##################</br>"
    output1 = output1 + "<table><tr><th>Name</th><th>Count</th></tr>"
    for a in sorted_results:
        #print ("Name: "+ a[0] + " Count: "+str(a[1]))
        output1=output1 + ("<tr><td>"+ a[0] + "</td><td>"+str(a[1])) + "</td></tr>"
    output1 =output1 + "##########################################"
    return output1

@app.route("/endpoint2")
def e2():
    output2 = "<style>table {border-collapse: collapse;}th, td {border: 2px solid;}</style>##########################################</br>Best ranking athlete of a segment gets 40 points and point acquired is decreased by one.</br> Last 10 athlete gets 1 points each.</br> Athletes with only one point in total will not be in the final leaderboard.</br>############ ENDPOINT 2 ##################</br>"
    output2 = output2 + "<table><tr><th>Name</th><th>Score</th></tr>"
    for a in FinalStanding:
        if a[1]>1:
            #print ("Name: "+ a[0] + " Score: "+str(a[1]))
            output2 = output2 + ("<tr><td>"+ a[0] + "</td><td>"+str(a[1])) + "</td></tr>"
    output2 =output2 + "</table>##########################################"
    return output2
