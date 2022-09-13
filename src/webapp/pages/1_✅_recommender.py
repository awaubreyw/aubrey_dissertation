from re import I
import streamlit as st
import pandas as pd
import numpy as np
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_player import st_player
import os.path


analyzer = SentimentIntensityAnalyzer()

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🕵️‍♀️") 
st.title("Project CAV²R⛏️")
st.header("Video Recommender")
userinput = st.text_input("Search here")


channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']
choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')
if 'channelkey' not in st.session_state:
    choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey', index=0)
    st.session_state['channelkey'] = choice
with st.sidebar:
    st.success(f"You have chosen {choice}!")
    st.write('session state: ', st.session_state.channelkey)
# choice = st.session_state.channelkey

# for i in range(len(channels)):
#     if choice == channels[i]:
#         indexint = i


#     #or choice = st.sidebar.radio(channels, key='channelkey')

# if 'channelkey' not in st.session_state:
#     st.session_state['channelkey'] = choicer

# choice = st.session_state['channelkey']


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

#st.subheader(f"Most positively acclaimed {choice} videos")
sub = st.subheader(f"{choice} videos that are considered to be more than 50% positive according to commenters")

sorted_vids = video_stats.items()
#sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1].get('viewCount')), reverse=True)
#sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse=True)
stats = []

for vid in sorted_vids:
    video_id = vid[0]
    title = vid[1]['title']
    #views = int(vid[1]['viewCount'])
    #likes = int(vid[1]['likeCount'])
    
    key = "commentCount"
    if key in vid[1].keys():
        comments = int(vid[1]["commentCount"]) 
    else:
        comments = 0

    key = "viewCount"
    if key in vid[1].keys():
        views = int(vid[1]["viewCount"]) 
    else:
        views = 0

    key = "likeCount"
    if key in vid[1].keys():
        likes = int(vid[1]["likeCount"]) 
    else:
        likes = 0

    duration = vid[1]['duration']
    stats.append([video_id, title, views, likes, comments, duration])

df = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'comments','duration'])
df.drop(df.loc[df['comments']==0].index, inplace=True)
df = df.reset_index(drop=True)
# df.drop(df.loc[df['views']==0].index, inplace=True)
# df.drop(df.loc[df['likes']==0].index, inplace=True)


overallpositivepercentage = []

# filter = df['comments'] == 0
# df = df.drop(index=df[filter].index)

for videoID in df['video_id']:
    filepath = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json'
    if os.path.exists(filepath):
        dataframe = pd.read_json(filepath)
    else:
        continue
    
    
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
    #st.write(dataframe['sentiment'].value_counts()['positive'])
    #totalpositivesentiment1 = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100
    if (dataframe['sentiment'].value_counts()['positive']) > 0:
        totalpositivesentiment1 = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100
    if (dataframe['sentiment'].value_counts()['positive']) == 0:
        totalpositivesentiment1 = 0

    overallpositivepercentage.append(totalpositivesentiment1)


df["overallpositivepercentage"] = pd.Series(overallpositivepercentage)
df = df.fillna(0)
#df = df.replace(np.nan, 0)

#st.dataframe(df)

df = df.sort_values(by=['overallpositivepercentage'], ascending=False)




top10 = df.head(10)


allvids = []
alltitles=[]

#CREDITS https://www.youtube.com/watch?v=clFrWjiwxL0 fake grid layout
n_cols = 3
n_rows = int(1 + len(df[df.overallpositivepercentage > 50]) // n_cols)



for key, value in df.iterrows():
    if value['overallpositivepercentage'] > 50:
        vid = f"https://www.youtube.com/watch?v={value['video_id']}"
        allvids.append(vid)
        alltitles.append(value['title'])
# range(len(value['overallpositivepercentage']))

rows = [st.columns(n_cols) for _ in range(n_rows)]

cols = [column for row in rows for column in row]

for col, thumbnail, title in zip(cols, allvids, alltitles):
    with col:
        st_player(f"https://www.youtube.com/watch?v={thumbnail}")
        st.write(title)
        # if userinput.casefold() in title.casefold():



        
       
        #col.video(f"https://www.youtube.com/watch?v={thumbnail}")


        
        #60 is rather low in terms of positive probability/scale and 50% indicates half positive and half negative. Has to be more positive than negative
        

        #st.video(f"https://www.youtube.com/watch?v={value['video_id']}")
        
        # Embed a youtube video


if len(df[df.overallpositivepercentage > 50]) <= 5:
    allvids = []
    alltitles = []
    sub = st.subheader(f"{choice} Top 10 videos based on positive sentiment score")
    n_rows = int(1 + len(top10['overallpositivepercentage']) // n_cols)
    for k, v in top10.iterrows():
        vid = f"https://www.youtube.com/watch?v={v['video_id']}"
        
        allvids.append(vid)
        alltitles.append(v['title'])
    rows = [st.columns(n_cols) for _ in range(n_rows)]

    cols = [column for row in rows for column in row]

    for col, thumbnail, title in zip(cols, allvids, alltitles):
        with col:
            st_player(f"https://www.youtube.com/watch?v={thumbnail}")
            st.write(title)
            #if title.contains(userinput):
















        

    # if value['overallpositivepercentage'] >= 70 not in value['overallpositivepercentage']:
    #     top10 = df.head(10)
    #     for index, row in top10.iterrows():
    #         video_file = open(f"https://www.youtube.com/watch?v={row['video_id']}", 'rb')
    #         video_bytes = video_file.read()
    #         st.video(video_bytes)
