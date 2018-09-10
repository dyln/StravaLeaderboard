#from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token = '418172ed16941e70d4ad096e00315d49260aaa3a'

# create an instance of the API class
api_instance = swagger_client.SegmentsApi()
id = 789 # Long | The identifier of the segment leaderboard.
gender = gender_example # String | Filter by gender. (optional)
ageGroup = ageGroup_example # String | Summit Feature. Filter by age group. (optional)
weightClass = weightClass_example # String | Summit Feature. Filter by weight class. (optional)
following = true # Boolean | Filter by friends of the authenticated athlete. (optional)
clubId = 789 # Long | Filter by club. (optional)
dateRange = dateRange_example # String | Filter by date range. (optional)
contextEntries = 56 # Integer |  (optional)
page = 56 # Integer | Page number. (optional)
perPage = 56 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

try: 
    # Get Segment Leaderboard
    api_response = api_instance.getLeaderboardBySegmentId(id, gender=gender, ageGroup=ageGroup, weightClass=weightClass, following=following, clubId=clubId, dateRange=dateRange, contextEntries=contextEntries, page=page, perPage=perPage)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SegmentsApi->getLeaderboardBySegmentId: %s\n" % e)