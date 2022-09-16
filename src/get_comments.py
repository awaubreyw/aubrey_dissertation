# CREDITS https://datanice.wordpress.com/2015/09/09/sentiment-analysis-for-youtube-channels-with-nltk/
# CREDITS https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/

from googleapiclient.discovery import build

#import creds
#api_key = creds.api_key
# then put confidential api key in environment variable or secret configuration file

from tqdm import tqdm #progress bar

import os
api_key = os.environ.get('YOUTUBE_DATA_API_KEY')
#CREDITS https://www.youtube.com/watch?v=IolxqkL7cD8

youtube = build("youtube", "v3", developerKey=api_key)

import json


#with open("results/video_ids_crashcourse.json", "r") as f:
    #video_ids_list = json.load(f)
# with open("results/veritasium.json", "r") as f: 
with open("results/video_ids_asapscience.json", "r") as f: #⚠️ asapscience tkor  kurzgesagt_–_in_a_nutshell  smartereveryday  crashcourse veritasium
    data = json.load(f)



# for channel_id in data:
#     for video_id, video_data in tqdm(data[channel_id]["video_data"].items()): 
#         #only getting first 3 items (called list slicing [:number]) (while [] is for index)

#         comments_contents = []

#         video_title = video_data['title']
        

       
# for index, video_id in enumerate(data):
for video_id in data[214:]:
    
    try:
        #request = youtube.commentThreads().list(
                #part="snippet,replies",
                #videoId=video_id,
                #maxResults=5,
                #order="time")

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

                #comment_content = {video_id: { video_title: {
                    #"channel_id": channel_id,
                    #"comment_by": comment_info["authorDisplayName"],
                    #"comment_text": comment_info["textDisplay"],
                    #"comment_date": comment_info["publishedAt"],
                    #"likes_count":  comment_info["likeCount"],
                #}}}

                comments_contents.append(comment_content) #dict inside list

            #comments_contents.append({
                #'comment_by': comment_info["authorDisplayName"],
                #'comment_text': comment_info["textDisplay"],
                #'comment_date': comment_info["publishedAt"],
                #'likes_count':  comment_info["likeCount"],
            #})
            

            # Again repeat
            if "nextPageToken" in response:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response["nextPageToken"]  # get 100 comments
                ).execute()

            #df = pd.DataFrame(comments_contents, columns=('comment_by', 'comment_text', 'comment_date', 'likes_count'))
            
            else:
                break
                

        with open(f"results/asapscience/{video_id}.json", 'w') as f: #⚠️ asapscience tkor  kurzgesagt_–_in_a_nutshell  smartereveryday  crashcourse    veritasium
            
            f.write(json.dumps(comments_contents))
            #f.write(df.to_json(orient='records', lines=True))


        # print('last video to have its comments extracted: ', video_id, ' of index: ', index) 
        #⚠️for index, video_id in data[index:] sliced 
        print(video_id, data.index(video_id))

    except Exception as e:
        print(f'failed to get comments with exception {e}')
print('index of last video extracted', data.index(video_id))
    






        #ignore replies to comments because most of the time, they are about the comment not the video quality
        #replies = []
        #reply = {}
        #replies.append(reply)







