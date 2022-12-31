#
# Want to be sent a name and return their top ten donations
#
# Be tweeted a name and check if it is a name
# and search for that name in the FEC doners list
#
# Open FEC: https://api.open.fec.gov/developers/#/receipts/get_schedules_schedule_a_
#
# List top 10 doners and dolllor amounts from this doner to individuals or commities

import config
import tweepy
import requests
import copy

FECAPI = config.openFECAPIkey

def getTwitterName():
    def bearerOauth(r):
        r.headers["Authorization"] = f"Bearer {bearer_token[0]}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r
    auth = tweepy.OAuth2BearerHandler(config.tBearerToken)
    api = tweepy.API(auth)
    

def getFECresponse(name):
    urlStart = "https://api.open.fec.gov/v1/schedules/schedule_a/?sort=-contribution_receipt_amount&sort_hide_null=false&contributor_type=individual&contributor_name="
    urlEnd = "&api_key="+confic.openFECAPIkey+"&per_page=50&sort_null_only=false&is_individual=true"
    urlName = name.strip().replace(" ", %20)
    urlAPI = urlStart + urlName + urlEnd
    FECresponse = request(urlAPI)
    if FECresponse.status_code == 200:
        FECjson = FECresponse.json()
    else:
        FECjson = "Not good query"

    return FECjson


def parseFECjson(FECjson):
    results = FECjson["results"]
    donations = []    
    for (i=0; i<10; i++):
        donation = {}
        donation["name"] = results[i]["contributer_name"]
        donation["amount"] =  results[i]["contribution_receipt_amount"]
        if (results[i]["candidate_id"] == null):
            donation["receiver"] = results[i]["committee"]["name"]
            donation["groupType"] = results[i]["committee"]["committee_label"]
        else:
            donation["receiver"] = results[i]["candidate_id"]
        donations.append(copy.deepcopy(donation))
        # return list with donation info dictionaries to create tweet
    return donations
        

def createTweet(information):
    

        
def main ():
    donorName = getTwitterName
    # donations is a list of donation dictionaries
    donations = parseFECjson(getFECresponse(donorName))
    for dons in donations:
        createTweet(dons);
    

if __name__=="__main__":
    main()
