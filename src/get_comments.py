# CREDITS https://datanice.wordpress.com/2015/09/09/sentiment-analysis-for-youtube-channels-with-nltk/
# CREDITS https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/

from googleapiclient.discovery import build
from tqdm import tqdm #progress bar

import os
api_key = os.environ.get('YOUTUBE_DATA_API_KEY')

youtube = build("youtube", "v3", developerKey=api_key)

import json

channelname = 'vsauce'

# with open("results/{channelname}.json", "r") as f: 
with open(f"results/video_ids_{channelname}.json", "r") as f: 
    #⚠️ tkor     kurzgesagt_–_in_a_nutshell  smartereveryday     crashcourse     veritasium[61:]    
    data = json.load(f)

# for channel_id in data:
#     for video_id, video_data in tqdm(data[channel_id]["video_data"].items()): 
#         #only getting first 3 items (called list slicing [:number]) (while [] is for index)

#         comments_contents = []

#         video_title = video_data['title']
        
for video_id in data[153:]:
    
    try:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="time")

        # execute the request
        response = request.execute()
        
        comments_contents = []
        comment_content = {}

        dfa = []
        
        while response:
        
            for item in response["items"]:
                item_info = item["snippet"]
                topLevelComment = item_info["topLevelComment"]
                comment_info = topLevelComment["snippet"]
                channel_id = item["id"]

                comment_content = {
                    "comment_by": comment_info["authorDisplayName"],
                    "comment_text": comment_info["textDisplay"],
                    "comment_date": comment_info["publishedAt"],
                    "likes_count":  comment_info["likeCount"],
                }

                comments_contents.append(comment_content) #dict inside list

            # Again repeat
            if "nextPageToken" in response:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response["nextPageToken"]  # get 100 comments
                ).execute()

            else:
                break
                

        with open(f"results/{channelname}/{video_id}.json", 'w') as f: 
            
            f.write(json.dumps(comments_contents))

        #⚠️to know from which index to slice
        # print(video_id, data.index(video_id))
        print('index of last video extracted', data.index(video_id))
    except Exception as e:
        print(f'failed to get comments with exception {e}')