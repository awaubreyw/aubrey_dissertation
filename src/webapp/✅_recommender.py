import streamlit as st
st.title("Video Recommender")

channel = st.session_state.channelkey
channel = channel.replace(' ', '_').lower()
#implement logic from C:\xampp\htdocs\aubrey_dissertation\src\webapp\recommender.ipynb

#for loop:
#   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


channel = st.session_state.channelkey
channel = channel.replace(' ', '_').lower()

import json

# with st.container():
#     st.dataframe()
#     analyses of top 10 videos based on views
file = f'../results/{channel}.json' 
data = None

with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse=True)

stats = []

for vid in sorted_vids:
    video_id = vid[0]
    title = vid[1]['title']
    views = int(vid[1]['viewCount'])
    likes = int(vid[1]['likeCount'])
    
    key = "commentCount"
    if key in vid[1].keys():
        comments = int(vid[1]["commentCount"]) 
    else:
        comments = 0

    duration = vid[1]['duration']
    stats.append([video_id, title, views, likes, comments, duration])

df = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'comments','duration'])


overallpositivepercentage = []

filter = df['comments'] == 0
df = df.drop(index=df[filter].index)

for videoID in df['video_id']:

    dataframe = pd.read_json(f'../results/crashcourse/{videoID}.json')
    
    positive = []
    negative = []
    neutral = []
    compound = []
    sentiment = []

    for line in range(dataframe.shape[0]): 

        comments = dataframe.iloc[line, 1] 
        comments_analyzed = analyzer.polarity_scores(comments)

    
        if comments_analyzed["compound"] >= 0.05:
            eachsentiment = 'positive'
        elif comments_analyzed["compound"] <= -0.05:
            eachsentiment = 'negative'
        else:
            eachsentiment = 'neutral'
    

#RUN ONCE
        negative.append(comments_analyzed["neg"])

        positive.append(comments_analyzed["pos"])
        #print(positive)

        neutral.append(comments_analyzed["neu"])
        #print(neutral)

        compound.append(comments_analyzed["compound"])
        #print(compound)

        sentiment.append(eachsentiment)


    dataframe["negative"] = negative 
    dataframe["neutral"] = neutral
    dataframe["positive"] = positive
    dataframe["compound"] = compound
    dataframe["sentiment"] = sentiment
    


    totalrows = len(dataframe['sentiment'])

    totalpositivesentiment1 = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100


    overallpositivepercentage.append(totalpositivesentiment1)


df["overallpositivepercentage"] = overallpositivepercentage

df = df.sort_values(by=['overallpositivepercentage'], ascending=False)

for key, value in df.iterrows():
    if value['overallpositivepercentage'] >= 70: #60 is rather low in terms of positive probability/scale and 50% indicates half positive and half negative. Has to be more positive than negative
        print(f"Score: {value['overallpositivepercentage']}, URL: https://www.youtube.com/watch?v={value['video_id']}")
#for loop:
    st.markdown(f"[{value['title']}](https://www.youtube.com/watch?v={id})")