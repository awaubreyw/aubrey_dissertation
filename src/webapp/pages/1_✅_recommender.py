
import streamlit as st
import pandas as pd
import numpy as np
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_player import st_player
import os.path
# import time


st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🎓") 
analyzer = SentimentIntensityAnalyzer()


st.title("🌄Project CAV²R⛏️")
st.header("Video Recommender")

userinput = st.text_input("Search here")
# with open("src/webapp/title_inverted_index.json", "r") as f:
#     loaded_index = json.load(f)
#     TITLE_INVERTED_INDEX = {k : set(v) for k, v in loaded_index.items()}
# if 'title_inverted_index' not in st.session_state:
#     st.session_state['title_inverted_index'] = TITLE_INVERTED_INDEX
st.info(f'Tip: If there are no results with that title. Please search for another', icon="ℹ️")


channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']


st.session_state.update(st.session_state)

choice = st.sidebar.selectbox(label='Pick one YouTube channelarg', options=channels, key='channelkey')

with st.sidebar:
    st.success(f"You have chosen {choice}!")

channel = choice.replace(' ', '_').lower()    



#implement logic from C:/xampp/htdocs/aubrey_dissertation/src/webapp/recommender.ipynb
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def process(channelarg):
    file = f'src/webapp/pages/../../results/{channelarg}.json'

    data = None

    with open(file, 'r') as f:
        data = json.load(f)

    channel_id, stats = data.popitem()

    channel_stats = stats['channel_statistics']

    video_stats = stats['video_data']


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

    dfplaceholder = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'comments','duration'])
    dfplaceholder.drop(dfplaceholder.loc[dfplaceholder['comments']==0].index, inplace=True)
    for identifier in dfplaceholder['video_id']:
        filename = f"src/webapp/pages/../../results/{channelarg}/{identifier}.json"
        if os.path.exists(filename):
            pass
        else:
            dfplaceholder.drop(dfplaceholder.index[dfplaceholder['video_id'] == identifier], inplace = True)
    dfplaceholder = dfplaceholder.reset_index(drop=True)

    overallpositivepercentage = []
    overallneutralpercentage = []
    overallnegativepercentage = []

    for videoID in dfplaceholder['video_id']:
        # filepath = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channelarg}/{videoID}.json'
        #filepath = os.path.relpath(f"C:/xampp/htdocs/aubrey_dissertation/src/results/{channelarg}/{videoID}.json", "C:/xampp/htdocs/aubrey_dissertation/src/webapp/pages/_recommender.py")
        filepath = f'src/webapp/pages/../../results/{channelarg}/{videoID}.json'
        # if os.path.exists(filepath):
        #     dataframe = pd.read_json(filepath)
        # else:
        #     continue
        dataframe = pd.read_json(filepath)
        
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


    dfplaceholder["overallpositivepercentage"] = pd.Series(overallpositivepercentage)
    dfplaceholder["overallneutralpercentage"] = pd.Series(overallneutralpercentage)
    dfplaceholder["overallnegativepercentage"] = pd.Series(overallnegativepercentage)
    dfplaceholder = dfplaceholder.fillna(0)

    dfplaceholder = dfplaceholder.sort_values(by=['overallpositivepercentage'], ascending=False)

    return dfplaceholder


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def recommend(df_arg):
    # allvids = []
    # alltitles=[]
    # notpositivelist = []
    # if df_arg.index[df_arg.overallpositivepercentage > 50].any():
    # if len(df_arg[df_arg['overallpositivepercentage'] > 50]) == 0:
    #     st.warning("There are no highly positive videos to recommend", icon="⚠️")
        
    # else:
    

    for key, value in df_arg.iterrows():
        # if value['overallpositivepercentage'] > 50:
        #     vid = f"https://www.youtube.com/watch?v={value['video_id']}"
        #     allvids.append(vid)
        #     alltitles.append(value['title'])
        if value['overallpositivepercentage'] <= 50:
            # notpositivelist.append(value['video_id'])
            df_arg.drop(df_arg.index[df_arg['overallpositivepercentage'] == value['overallpositivepercentage']], inplace = True)

    # for notpositivevid in notpositivelist:
    #     df_arg.drop(df_arg.index[df['video_id'] == notpositivevid], inplace = True)
        
    return df_arg







df = process(channel)
# top10 = df.head(10)

if len(df[df['overallpositivepercentage'] > 50]) == 0:
    st.warning("There are no highly positive videos to recommend", icon="⚠️")
else:
    st.success(f"Here are the recommendations based on highly positive sentiments of {choice} videos")
    moddf = recommend(df)
    # st.dataframe(moddf)

    n_cols = 3
    n_rows = int(1 + len(moddf[moddf.overallpositivepercentage > 50]) // n_cols)
    rows = [st.columns(n_cols) for _ in range(n_rows)]
    cols = [column for row in rows for column in row]

    # for col, vid, title in zip(cols, recvids, rectitles):
    #     with col:
    #         st_player(vid)
    #         st.write(title)
    for col, vid, title, score in zip(cols, moddf['video_id'], moddf['title'], moddf['overallpositivepercentage']):
        with col:
            url = f"https://www.youtube.com/watch?v={vid}"
            st_player(url)
            st.write(title)
            score = round(score)
            score = str(score)+'%'
            st.success(score)

    if userinput:
        # if userinput.casefold() in moddf['title'].str.casefold().str.contains(userinput):
        # if [any(userinput.lower() in s.lower()) for s in list(moddf['title'])]:
        # if moddf['title'].str.contains(userinput, case=False):
        if userinput.casefold() in moddf['title'].str.casefold():
            st.success('Found match(es)', icon="✅")
            matches = moddf.loc[moddf['title'].str.contains(userinput, case=False)]
            n_cols = 3
            n_rows = int(1 + len(matches[matches.overallpositivepercentage > 50]) // n_cols)
            rows = [st.columns(n_cols) for _ in range(n_rows)]
            columns = [column for row in rows for column in row]
            for matchvid, matchtitle, matchscore, col in zip(matches['video_id'], matches['title'], matches['overallpositivepercentage'], columns):
                with col:
                    url = f"https://www.youtube.com/watch?v={matchvid}"
                    st_player(url)
                    st.write(matchtitle)
                    matchscore = round(matchscore)
                    matchscore = str(matchscore)+'%'
                    st.success(matchscore)
        else:
            st.warning(f'{choice} has no videos with that title. Please try again', icon="⚠️")


