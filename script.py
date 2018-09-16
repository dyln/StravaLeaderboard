#Designed and coded by Caner Eren

import json
import urllib2
import operator
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'

@app.route("/")
def hello():
    return "<p>Hello</p> <p>To see the Endpoint 1 <a href = 'http://127.0.0.1:5000/endpoint1'>click here</a></p> <p>To see the Endpoint 2 <a href = 'http://127.0.0.1:5000/endpoint2'>click here</a></p> "

#The latitude and longitude for two points describing a rectangular boundary for the search: 
#[southwest corner latitutde,
#southwest corner longitude, 
#northeast corner latitude, 
#northeast corner longitude]
#ISTANBUL
bounds = [41.031471, 28.007190, 41.141815, 29.913041]

## Getting top 10 riding segments in Istanbul in json format
access_token = '418172ed16941e70d4ad096e00315d49260aaa3a' #personal API access token 
segments_url= 'https://www.strava.com/api/v3/segments/explore?bounds='+str(bounds[0])+','+str(bounds[1])+','+str(bounds[2])+','+str(bounds[3])+'&activity_type=riding&access_token='+access_token
segments_raw = urllib2.urlopen(segments_url)
segments = json.load(segments_raw)

##Getting each segments leaderboard data, top 50 and store them in a dictionary keyed with segment id
pairs = {}
for x in segments['segments']:
    id=x['id']
    leaderboard_url = 'https://www.strava.com/api/v3/segments/'+str(id)+'/leaderboard?&per_page=50&access_token='+access_token    
    leaderboard_raw = urllib2.urlopen(leaderboard_url)
    pairs[x['id']]= json.load(leaderboard_raw)

##Seperating all the athlete names in all segments in a different list
names = []
for x in pairs:
    for y in pairs[x]['entries']:
        names.append(y['athlete_name'])

# Helper function for count of a list element
def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return len(result)
        result.append(offset)

#Checking the number of occurences in the list and save them in a dictionary keyed with name
result = {}
for x in names:
    y=indices(names,x)
    if (y>1):
        result[x]=y

#Sort the result
sorted_results = sorted(result.items(), key=lambda x: x[1],reverse=True)

#Serve the result as simple html in the web app
@app.route("/endpoint1")
def e1():
    output1 = "<style>table {border-collapse: collapse;}th, td {border: 2px solid;}</style>##########################################</br>############ ENDPOINT 1 ##################</br>"
    output1 = output1 + "<table><tr><th>Name</th><th>Count</th></tr>"
    for a in sorted_results:
        #print ("Name: "+ a[0] + " Count: "+str(a[1]))
        output1=output1 + ("<tr><td>"+ a[0] + "</td><td>"+str(a[1])) + "</td></tr>"
    output1 =output1 + "##########################################"
    return output1


#Initialize leaderboard with names
LeaderBoard = {}
for x in names:
    LeaderBoard[x]=[]

#Scoring formula is like below:
#1st=40pt , 2nd=39pt, 3th=38pt ..... 40th=1pt, 41th=1pt ..... 50=1pt
#Store rankings got by an athlete in a list in a dictionary keyed with name
for y in pairs:
    for x in pairs[y]['entries']:
        if x['rank'] > 39:
            LeaderBoard[x['athlete_name']].append(1)
        if x['rank']<40:
            LeaderBoard[x['athlete_name']].append(41-x['rank'])

#Initialize final standing dict; where all the scores will be summed up
#Athletes with only one point in total will not be in the final leaderboard.
FinalStandings = {}
for x in LeaderBoard:
    temp=[]
    score=0
    temp = LeaderBoard[x]
    for a in temp:
        score=score + a
    FinalStandings[x] = score

#Sort the final leaderboard
FinalStanding = sorted(FinalStandings.items(), key=lambda x: x[1],reverse=True)

#Serve the result as simple html in the web app
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
