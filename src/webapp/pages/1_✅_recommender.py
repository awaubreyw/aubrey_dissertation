
import streamlit as st
import pandas as pd
import numpy as np
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_player import st_player
import os.path
import time


@st.cache
def search(search_string, inverted_index):
    """
    This function takes a string as the first parameter and an inverted index as the second parameter.
    It then searches the string in the inverted index
    It will always try to return at least one result
    This is an example of a very simple search algorithm
    """
    # Its important to lowercase so that we can match things like "Visual" and "visual"
    tokens = search_string.lower().split() # Split on spaces e.g. ['How', 'to', 'lie', 'using', 'visual', 'proofs']

    document_set = {}
    for token in tokens:
        if token in inverted_index.keys():
            if document_set == {}:
                document_set = inverted_index[token]
            else:
                intersect = set.intersection(document_set, inverted_index[token])
                document_set = intersect if len(intersect) > 0 else document_set
            
    return document_set



st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🎓") 
analyzer = SentimentIntensityAnalyzer()

# back = st.button('Go back', on_click=st.experimental_rerun)
# st.markdown(f"[{back}](https://github.com/awaubreyw/aubrey_dissertation/blob/main/src/webapp/app.py)", unsafe_allow_html=True)
st.title("🌄Project CAV²R⛏️")
st.header("Video Recommender")

userinput = st.text_input("Search here")
# with open("src/webapp/title_inverted_index.json", "r") as f:
#     loaded_index = json.load(f)
#     TITLE_INVERTED_INDEX = {k : set(v) for k, v in loaded_index.items()}
# if 'title_inverted_index' not in st.session_state:
#     st.session_state['title_inverted_index'] = TITLE_INVERTED_INDEX
st.warning(f'Tip: If there are no results with that title. Please search for another', icon="⚠️")


channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']


# choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

# if 'channelkey' not in st.session_state:
    # choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

# choice = st.session_state['channelkey'] 

# choice = st.session_state['channelkey']

st.session_state.update(st.session_state)
# if 'channelkey' not in st.session_state:
#     st.session_state['channelkey'] = choice
choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

with st.sidebar:
    st.success(f"You have chosen {choice}!")
    st.write('session state: ', st.session_state.channelkey)

channel = choice.replace(' ', '_').lower()    




#implement logic from C:/xampp/htdocs/aubrey_dissertation/src/webapp/recommender.ipynb






# file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 
#file = os.path.relpath(f"C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json", "C:/xampp/htdocs/aubrey_dissertation/src/webapp/pages/_recommender.py")
file = f'src/webapp/pages/../../results/{channel}.json'

data = None

with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

# sub = st.subheader(f"{choice} most enjoyed videos")
with st.spinner('Please wait... processing'):
    time.sleep(5) 

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


# @st.cache(allow_output_mutation=True)
@st.cache(suppress_st_warning=True)
def recommend_videos_part_1(df_arg):
    overallpositivepercentage = []
    overallneutralpercentage = []
    overallnegativepercentage = []

    for videoID in df_arg['video_id']:
        # filepath = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json'
        #filepath = os.path.relpath(f"C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json", "C:/xampp/htdocs/aubrey_dissertation/src/webapp/pages/_recommender.py")
        filepath = f'src/webapp/pages/../../results/{channel}/{videoID}.json'
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

    return top10, df_arg





def recommend_videos_part_2(top10, df_arg):
    
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

        # sub = st.subheader(f"{choice} Top 10 videos based on positive sentiment score")

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

    return allvids, recvidthumbnails, recvidtitles, cols
            





if userinput:
    # top10val, df_val = recommend_videos_part_1(df)
    # allvids, recvidthumbnails, recvidtitles, cols = recommend_videos_part_2(top10val, df_val)
    # searchedresult = search(userinput, st.session_state['title_inverted_index'])
    # urls = []
    # for result, col in zip(searchedresult, cols):
    #     with col:
    #         url=f"https://www.youtube.com/watch?v={result}"
    #         st_player(url)

    # for result, col in zip(searchedresult, cols):
    #     for vidid in allvids:
    #         if result == vidid:
    #             with col:
    #                 st_player(f"https://www.youtube.com/watch?v={result}")

    
    # for vidid in allvids:
    #     for result in searchedresult:
    #         if result in vidid:
    #             for col in cols:
    #                 st.markdown(f"[{result}](https://www.youtube.com/watch?v={result})")
                    # st_player(f"https://www.youtube.com/watch?v={result}")
                    # st.write(result)
                


    # userinput = userinput.casefold()
    df_result_search = pd.DataFrame()
    
    inputdict = {}
    idlist = []
    titlelist = []

    # if userinput in df['title'].str.casefold().str.contains(userinput).any():
    for index, row in df.iterrows():
        if userinput.casefold() in str(row['title']).casefold():
            idlist.append(row['video_id'])
            titlelist.append(row['title'])
            inputdict = {
                "video_id": idlist, 
                "title": titlelist
            }
            df_result_search = pd.DataFrame(inputdict)

    # else:
    #     st.warning(f'{choice} has no videos with that title. Please try again', icon="⚠️")
    #     e = KeyError('Please try again')
    #     st.exception(e)

    top10val, df_val = recommend_videos_part_1(df_result_search)
    allvids, recvidthumbnails, recvidtitles, cols = recommend_videos_part_2(top10val, df_val)
    
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a)
            st.write(b)

elif userinput == '':
    top10val, df_val = recommend_videos_part_1(df)
    allvids, recvidthumbnails, recvidtitles, cols = recommend_videos_part_2(top10val, df_val)
    # allvids, recvidthumbnails, recvidtitles, cols = recommend_videos(df)
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a)
   
            #   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

            st.write(b)

else:
    top10val, df_val = recommend_videos_part_1(df)
    allvids, recvidthumbnails, recvidtitles, cols = recommend_videos_part_2(top10val, df_val)
    # allvids, recvidthumbnails, recvidtitles, cols = recommend_videos(df)
    for a, b, col in zip(recvidthumbnails, recvidtitles, cols):
        with col:
            st_player(a) 
            
            #   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")

            st.write(b)



# st.experimental_rerun()