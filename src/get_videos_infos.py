#https://www.knowledgehut.com/blog/programming/python-exception-handling
#CREDITS FOR CODE
#https://www.youtube.com/watch?v=5qtC-tsQ-wE&t=828s
#https://www.youtube.com/watch?v=4FwXqOT4-FM
#https://www.youtube.com/watch?v=1lxrb_ezP-g

#import creds
#API_KEY = creds.api_key

import json
import requests
from tqdm import tqdm #progress bar
from googleapiclient.discovery import build


import os
API_KEY = os.environ.get('YOUTUBE_DATA_API_KEY')
#CREDITS https://www.youtube.com/watch?v=IolxqkL7cD8

youtube = build('youtube', 'v3', developerKey=API_KEY)

class YTstats:

#constructor
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None
        

    def get_channel_statistics(self):
        #go to https://developers.google.com/youtube/v3/docs#Channels
        #and https://developers.google.com/youtube/v3/docs/channels/list?apix_params=%7B%22part%22%3A%5B%22statistics%22%5D%2C%22forUsername%22%3A%22crashcourse%22%7D&apix=true#usage
        #HTTP GET request show code
        #GET https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forUsername=crashcourse&key=[YOUR_API_KEY] 
        #GET https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id=abc123&key=[YOUR_API_KEY] HTTP/1.1


        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'

        #print(f'{self.channel_id} = {url}')
        #print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0]['statistics']
        except KeyError:
            print('Could not get channel stats')
            data = {}

        self.channel_statistics = data
        return data



    def get_channel_video_data(self):
        channel_videos = self._get_channel_videos(limit=50)

        #print(channel_videos)
        #print(len(channel_videos))

        parts = ['snippet', 'statistics', 'contentDetails']

        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)

                channel_videos[video_id].update(data)

        self.video_data = channel_videos
        return channel_videos
                

    def _get_single_video_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'

        json_url = requests.get(url)

        data = json.loads(json_url.text)

        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data

    def _get_channel_videos(self, limit=None):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"

        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

            #print(url)
        
        vid, npt = self._get_channel_videos_per_page(url)

        index = 0

        while(npt is not None and index < 10):
            nexturl = url + "&pageToken=" + npt

            next_vid, npt = self._get_channel_videos_per_page(nexturl)

            vid.update(next_vid)

            index += 1

        return vid


    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)

        data = json.loads(json_url.text)

        channel_videos = dict()

        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, None

        

        item_data = data['items']

        nextPageToken = data.get("nextPageToken", None)

        for item in item_data:
            try:
                kind = item['id']['kind']

                if kind == 'youtube#video':
                    video_id = item['id']['videoId']

                    channel_videos[video_id] = dict()

            except KeyError as e:
                #print('error')
                print('Error! Could not extract data from item:\n', item)

        return channel_videos, nextPageToken



    def dump(self):
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics, "video_data": self.video_data}}
        

        request = youtube.channels().list(
                part="snippet",
                id=self.channel_id
            )
        response = request.execute()
        
        for item in response['items']:
            snippet = item["snippet"]
            channel_title = snippet["title"]




            channel_title = channel_title.replace(' ', '_').lower()


            filename = 'results/' + channel_title + '.json'

            with open(filename, 'w') as f:
                json.dump(fused_data, f, indent=4)
                
            print('file dumped to', filename)

        with open(filename, 'r') as f:
            data = json.load(f)
            
        video_ids = []
        for channel_id in data:
            for video_id, video_data in data[channel_id]['video_data'].items():
                video_ids.append(video_id)
                #maybe get comments with the video id keys under here instead of another py file?
                #then dont need to manually type json filename in that other py file to grab comments
                
        filename = 'results/video_ids_' + channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(video_ids, f)
            


if __name__ == "__main__":

    with open('constants/channel_2_id.json', 'r') as f:
        data = json.load(f)
    
    #slice list of data items and skip the first three channel name and id tuples
    #for channelname, channelid in list(data.items())[3:]:
    for channelname, channelid in list(data.items())[13:]:

        #print(channelid)
        #manually
        #YT = YTstats(API_KEY, "UCUHW94eEFW7hkUMVaZz4eDg") #second is khan academy id
        YT = YTstats(API_KEY, channelid)
        YT.get_channel_statistics()
        YT.get_channel_video_data()
        YT.dump()


    #with open('constants/channel_info.json', 'r') as f:
        #channels_list = json.load(f)
    
    #for each_channel_dict in channels_list:
        
        #channel_id_value = each_channel_dict['channel_id']
        #print(channel_id_value)
        #YT = YTstats(API_KEY, channel_id_value)















