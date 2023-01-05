#
# Want to be sent a name and return their top ten donations
#
# Be tweeted a name and check if it is a name
# and search for that name in the FEC doners list
#
# Open FEC: https://api.open.fec.gov/developers/#/receipts/get_schedules_schedule_a_
#
# List top 10 doners and dolllor amounts from this doner to individuals or commities

from config import *
import copy
import tweepy
import time
import requests

null = None

def getFECresponse(name):
    urlStart = "https://api.open.fec.gov/v1/schedules/schedule_a/?sort=-contribution_receipt_amount&sort_hide_null=false&contributor_type=individual&contributor_name="
    urlEnd = "&api_key="+openFECAPIkey+"&per_page=50&sort_null_only=false&is_individual=true"
    urlName = name.strip().replace(" ", "%20")
    urlAPI = urlStart + urlName + urlEnd
    FECresponse = requests.get(urlAPI)
    if FECresponse.status_code == 200:
        return FECresponse.json()
    else:
        return "Not good query"


def parseFECjson(FECjson):
    results = FECjson["results"]
    donations = []
    index = len(results)-1 if len(results) < 10 else 10
    for i in range(index):
        donation = {}
        donation["name"] = results[i]["contributor_name"]
        donation["amount"] =  results[i]["contribution_receipt_amount"]
        if (not results[i]["candidate_id"]):
            donation["receiver"] = results[i]["committee"]["name"]
        else:
            donation["receiver"] = results[i]["candidate_id"]
        donation["groupType"] = results[i]["committee"]["committee_label"]
        donations.append(copy.deepcopy(donation))
        # return list with donation info dictionaries to create tweet
        
    return donations
    
def checkMentionsSendReply(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        print(new_since_id)
        print(tweet.id)
        if tweet.in_reply_to_status_id is not None:
            continue
        else:
            name = tweet._json["text"][14:].strip()

        donations = parseFECjson(getFECresponse(name))

#        if (len(donations) > 0):
        for donation in donations:
            tweeter = tweet._json["user"]["screen_name"]
            statusText = "@{tweeter}\n{name}\nGave: {amount}\nTo: {receiver}\nTYPE: {groupType}".format(
                tweeter = tweeter,
                name = donation["name"],
                amount = str(donation['amount']),
                receiver = donation['receiver'],
                groupType = donation['groupType'])
            
            api.update_status(status = statusText,
                              in_reply_to_status_id = tweet.id,)
        else:
            api.update_status(status = name + " has no record of donating.",
                              in_reply_to_status_id = tweet.id,)
                
    return new_since_id


def main():
    # sign in
    oauth = tweepy.OAuth1UserHandler(tAPIkey,tAPISecret,tAccessToken,tAccessSecret)
    api = tweepy.API(oauth)
    # start loop
    since_id = 1
    while(True):
        since_id = checkMentionsSendReply(api, since_id)
        time.sleep(10)
                    



if __name__=="__main__":
    main()
