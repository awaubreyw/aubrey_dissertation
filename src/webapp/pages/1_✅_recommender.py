import streamlit as st
import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_player import st_player

analyzer = SentimentIntensityAnalyzer()

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🕵️‍♀️") 
st.title("Project CAV²R⛏️")
st.header("Video Recommender")

choice = st.session_state.channelkey
channel = choice.replace(' ', '_').lower()
#implement logic from C:/xampp/htdocs/aubrey_dissertation/src/webapp/recommender.ipynb

#for loop:
#   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")





file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 

data = None

with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

st.subheader(f"Most positively acclaimed {choice} videos")

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
df.drop(df.loc[df['comments']==0].index, inplace=True)

overallpositivepercentage = []

# filter = df['comments'] == 0
# df = df.drop(index=df[filter].index)

for videoID in df['video_id']:

    dataframe = pd.read_json(f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json')
    
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
    if value['overallpositivepercentage'] >= 70: 
        #60 is rather low in terms of positive probability/scale and 50% indicates half positive and half negative. Has to be more positive than negative
        

        #st.video(f"https://www.youtube.com/watch?v={value['video_id']}")
        
        # Embed a youtube video
        st_player(f"https://www.youtube.com/watch?v={value['video_id']}")

    # if value['overallpositivepercentage'] >= 70 not in value['overallpositivepercentage']:
    #     top10 = df.head(10)
    #     for index, row in top10.iterrows():
    #         video_file = open(f"https://www.youtube.com/watch?v={row['video_id']}", 'rb')
    #         video_bytes = video_file.read()
    #         st.video(video_bytes)
