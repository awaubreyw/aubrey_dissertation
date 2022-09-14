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
st.warning(f'Tip: If there are no results with that title. Please search for another', icon="⚠️")


channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']

choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

if 'channelkey' not in st.session_state:
    choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey', index=0)
    st.session_state['channelkey'] = choice

with st.sidebar:
    st.success(f"You have chosen {choice}!")
    st.write('session state: ', st.session_state.channelkey)

channel = choice.replace(' ', '_').lower()    




#implement logic from C:/xampp/htdocs/aubrey_dissertation/src/webapp/recommender.ipynb






# file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 
file = os.path.relpath(f"C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json", "C:/xampp/htdocs/aubrey_dissertation/src/webapp/pages/_recommender.py")

data = None

with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

sub = st.subheader(f"{choice} videos that are considered to be more than 50% positive according to commenters")

sorted_vids = video_stats.items()

stats = []

for vid in sorted_vids:
    video_id = vid[0]
    title = vid[1]['title']
    
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


@st.cache(allow_output_mutation=True)
def recommend_videos(df_arg):
    overallpositivepercentage = []
    overallneutralpercentage = []
    overallnegativepercentage = []

    for videoID in df_arg['video_id']:
        # filepath = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json'
        filepath = os.path.relpath(f"C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json", "C:/xampp/htdocs/aubrey_dissertation/src/webapp/pages/_recommender.py")
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

            neutral.append(comments_analyzed["neu"])

            compound.append(comments_analyzed["compound"])

            sentiment.append(eachsentiment)


        dataframe["negative"] = negative 
        dataframe["neutral"] = neutral
        dataframe["positive"] = positive
        dataframe["compound"] = compound
        dataframe["sentiment"] = sentiment
        

        totalrows = len(dataframe['sentiment'])

        if dataframe['sentiment'].str.contains('positive').any():
            totalpositivesentiment = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100
            overallpositivepercentage.append(totalpositivesentiment)
        if dataframe['sentiment'].str.contains('negative').any():
            totalnegativesentiment = ((dataframe['sentiment'].value_counts()['negative'])/totalrows)*100
            overallnegativepercentage.append(totalnegativesentiment)
        if dataframe['sentiment'].str.contains('neutral').any():        
            totalneutralsentiment = ((dataframe['sentiment'].value_counts()['neutral'])/totalrows)*100
            overallneutralpercentage.append(totalneutralsentiment)


    df_arg["overallpositivepercentage"] = pd.Series(overallpositivepercentage)
    df_arg["overallneutralpercentage"] = pd.Series(overallneutralpercentage)
    df_arg["overallnegativepercentage"] = pd.Series(overallnegativepercentage)
    df_arg = df_arg.fillna(0)

    df_arg = df_arg.sort_values(by=['overallpositivepercentage'], ascending=False)




    top10 = df_arg.head(10)


    allvids = []
    alltitles=[]

    #CREDITS https://www.youtube.com/watch?v=clFrWjiwxL0 fake grid layout
    n_cols = 3
    n_rows = int(1 + len(df_arg[df_arg.overallpositivepercentage > 50]) // n_cols)



    for key, value in df_arg.iterrows():
        if value['overallpositivepercentage'] > 50:
            vid = f"https://www.youtube.com/watch?v={value['video_id']}"
            allvids.append(vid)
            alltitles.append(value['title'])


    rows = [st.columns(n_cols) for _ in range(n_rows)]

    cols = [column for row in rows for column in row]

    recvidtitles = []
    recvidthumbnails = []


    for thumbnail, title in zip(allvids, alltitles):
        url = f"https://www.youtube.com/watch?v={thumbnail}"
        recvidthumbnails.append(url)
        recvidtitles.append(title)


    if len(df_arg[df_arg.overallpositivepercentage > 50]) <= 5:
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
        recvidtitles = []
        recvidthumbnails = []
        # for col, thumbnail, title in zip(cols, allvids, alltitles):
        #     with col:
        for thumbnail, title in zip(allvids, alltitles):
            # st_player(f"https://www.youtube.com/watch?v={thumbnail}")
            # st.write(title)
            url = f"https://www.youtube.com/watch?v={thumbnail}"
            recvidthumbnails.append(url)
            recvidtitles.append(title)

    return recvidthumbnails, recvidtitles, cols
               





if userinput:

    userinput = userinput.casefold()
    df_result_search = pd.DataFrame()
    
    inputdict = {}
    idlist = []
    titlelist = []

    if userinput in df['title'].str.casefold().str.contains(userinput).any():
        for index, row in df.iterrows():
            if userinput.casefold() in str(row['title']).casefold():
                idlist.append(row['video_id'])
                titlelist.append(row['title'])
                inputdict = {
                    "video_id": idlist, 
                    "title": titlelist
                }
                df_result_search = pd.DataFrame(inputdict)

    else:
        st.warning(f'{choice} has no videos with that title. Please try again', icon="⚠️")
        e = KeyError('Please try again')
        st.exception(e)

    recvidthumbnails, recvidtitles, cols = recommend_videos(df_result_search)
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a)
            
            #   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

            st.write(b)

elif userinput == '':

    recvidthumbnails, recvidtitles, cols = recommend_videos(df)
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a)
   
            #   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

            st.write(b)

else:

    recvidthumbnails, recvidtitles, cols = recommend_videos(df)
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a) 
            
            #   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

            st.write(b)