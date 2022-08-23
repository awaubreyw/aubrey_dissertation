# CREDITS https://datanice.wordpress.com/2015/09/09/sentiment-analysis-for-youtube-channels-with-nltk/
# CREDITS https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/

from googleapiclient.discovery import build

api_key = "AIzaSyBhZfAuqxNwPbkGon-mLaEI62Y78dxAJyM"
# then put confidential api key in environment variable or secret configuration file
youtube = build("youtube", "v3", developerKey=api_key)

import json


#with open("results/video_ids_crashcourse.json", "r") as f:
    #video_ids_list = json.load(f)
with open("results/crashcourse.json", "r") as f:
    data = json.load(f)

comments_contents = []

for channel_id in data:
    for video_id, video_data in data[channel_id]["video_data"].items():



#for video_id in video_ids_list:
        #print(video_id)

        video_title = video_data['title']
        #print(video_title)

    try:
        #request = youtube.commentThreads().list(
                #part="snippet,replies",
                #videoId=video_id,
                #maxResults=5,
                #order="time")

        request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                order="time")

        # execute the request
        response = request.execute()
        
        comment_content = {}
        
        while response:
        
            for item in response["items"]:
                item_info = item["snippet"]
                topLevelComment = item_info["topLevelComment"]
                comment_info = topLevelComment["snippet"]
                channel_id = item["id"]

                ## comment_content = {
                # "channel_id": channel_id,
                # "video_title": video_title,
                # "video_id": video_id,
                # "comment_by": comment_info["authorDisplayName"],
                # "comment_text": comment_info["textDisplay"],
                # "comment_date": comment_info["publishedAt"],
                # "likes_count":  comment_info["likeCount"],
                #}

                comment_content = {video_id: { video_title: {
                    "channel_id": channel_id,
                    "comment_by": comment_info["authorDisplayName"],
                    "comment_text": comment_info["textDisplay"],
                    "comment_date": comment_info["publishedAt"],
                    "likes_count":  comment_info["likeCount"],
                }}}

                comments_contents.append(comment_content) #dict inside list

        

            # Again repeat
            if "nextPageToken" in response:
                response = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response["nextPageToken"]  # get 100 comments
                ).execute()
            else:
                break
            
    except:
        print('video disabled comments')
        





        #ignore replies to comments because most of the time, they are about the comment not the video quality
        #replies = []
        #reply = {}
        #replies.append(reply)







with open("results/video_comments_crashcourse.json", 'w') as f:
    f.write(json.dumps(comments_contents))


