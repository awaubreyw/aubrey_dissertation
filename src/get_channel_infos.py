#import creds
#put confidential api key in environment variable or secret configuration file
#api_key = creds.api_key

import json
#to grab public info of youtube channels
from googleapiclient.discovery import build

import os
api_key = os.environ.get('YOUTUBE_DATA_API_KEY')
#CREDITS https://www.youtube.com/watch?v=IolxqkL7cD8


youtube = build('youtube', 'v3', developerKey=api_key)

with open('constants/channel_2_id.json', 'r') as f:
    channel_dict = json.load(f)
    print(channel_dict)

channel_infos = []
for channel_title, channel_id in channel_dict.items():
    print(f'getting channel info for {channel_title}: {channel_id}')
    #loop through key, value from dict

    #to get channel info, request with parameters
    #request = youtube.channels().list(part='brandingSettings, snippet, contentDetails, statistics', forUsername=channelusername)
    request = youtube.channels().list(
        part="brandingSettings,statistics,snippet,contentDetails",
        id=channel_id
    )

    response = request.execute()

    #print(response['items'][0])
    channel_info={}
    for item in response['items']:

        channelId = item['id']

        # get the snippet, statistics & content details from the video response
        snippet         = item["snippet"]
        statistics      = item["statistics"]
        content_details = item["contentDetails"]
        channel = item["brandingSettings"]["channel"]


        # get infos from the snippet
        channel_title = snippet["title"]
        description   = snippet["description"]
        joined_date  = snippet["publishedAt"]
        #country = snippet["country"]
            #sometimes channel doesnt have default language so language = snippet["defaultLanguage"] would error

        subscriberCount = statistics["subscriberCount"]
        numOfVideos = statistics["videoCount"]

        keywords = channel["keywords"]
        keywords = keywords.replace('"', '') #removes double quotes from each keyword iteration in array/list

        #print(channel_title, joined_date, country, subscriberCount, numOfVideos, keywords)
        channel_info = {'channel_id': channel_id,
        'channel_title': channel_title, 
        'joined': joined_date,
        'keywords': keywords,
        'subs': subscriberCount,
        'total_videos': numOfVideos}

        print(f"""\
            Channel ID: {channel_id}
            Channel Title: {channel_title}
            Joined: {joined_date}
            Keywords: {keywords}
            Subs: {subscriberCount}
            Total videos: {numOfVideos}
            """)
        channel_infos.append(channel_info) #dict inside list

with open("constants/channel_info.json", 'w') as f:
    
    f.write(json.dumps(channel_infos))

