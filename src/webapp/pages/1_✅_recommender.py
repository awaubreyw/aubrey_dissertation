#CREDITS https://www.youtube.com/watch?v=clFrWjiwxL0 fake grid layout

import streamlit as st
import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from streamlit_player import st_player
import os.path

analyzer = SentimentIntensityAnalyzer()

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🎓") 
st.title("🌄Project CAV²R⛏️")
st.header("Video Recommender")

userinput = st.text_input("Search here")

st.info(f'Tip: If there are no results with that title. Please search for another', icon="ℹ️")

channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']


st.session_state.update(st.session_state)
choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

with st.sidebar:
    st.success(f"You have chosen {choice}!")

channel = choice.replace(' ', '_').lower()    

#implement logic from aubrey_dissertation/src/webapp/recommender.ipynb

# categories = ["Film & Animation", "Autos & Vehicles", "Music", "Pets & Animals", "Sports", "Short Movies", "Travel & Events", "Gaming", "Videoblogging", "People & Blogs", "Comedy", "Entertainment", "News & Politics", "Howto & Style", "Education", "Science & Technology", "Nonprofits & Activism", "Movies", "Anime/Animation", "Action/Adventure", "Classics", "Comedy", "Documentary", "Drama", "Family", "Foreign", "Horror", "Sci-Fi/Fantasy", "Thriller", "Shorts", "Shows", "Trailers"]

categoriesdf = pd.read_json("src/webapp/pages/../../constants/categories.json")

# categoricalchoice = st.selectbox(label="Pick any video category", options=categories, index=14)

# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
@st.experimental_memo
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
        
        key = "commentCount"
        if key in vid[1].keys():
            comments = int(vid[1]["commentCount"]) 
        else:
            comments = 0

        duration = vid[1]['duration']
        categoryid = vid[1]['categoryId']
        

        stats.append([video_id, title, views, likes, comments, duration, categoryid])

    dfplaceholder = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'comments','duration', 'categoryid'])
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
        filepath = f'src/webapp/pages/../../results/{channelarg}/{videoID}.json'

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


# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
@st.experimental_memo
def recommend(df_arg):
    
    for key, value in df_arg.iterrows():
       
        if value['overallpositivepercentage'] <= 50:
            
            df_arg.drop(df_arg.index[df_arg['overallpositivepercentage'] == value['overallpositivepercentage']], inplace = True)

    return df_arg

df = process(channel)

if len(df[df['overallpositivepercentage'] > 50]) == 0:
    st.warning("There are no highly positive videos to recommend", icon="⚠️")
else:

    moddf = recommend(df)
    categorylist = []

    for id in moddf['categoryid']:
        id = int(id)
        for index, row in categoriesdf.iterrows():
            if id == row['id']:
                categorylist.append(row['category'])
    # categorylist = []
    # for index, row in categoriesdf.iterrows():
    #     for i, r in moddf.iterrows():
    #         if r['categoryid'] == row['id']:
    #             categorylist.append(row['category'])

    moddf['category'] = categorylist

    if userinput:
        
        userinputlist = userinput.split()
        moddf['OR'] = moddf['title'].str.contains('|'.join(userinputlist))
        
        # mask = moddf.applymap(type) != bool
        # d = {True: 'TRUE', False: 'FALSE'}

        # moddf = moddf.where(mask, moddf.replace(d))
        # st.dataframe(moddf)
        
        # if moddf['OR'].str.contains('FALSE', case=False).any() == True:
        #     st.warning(f'{choice} has no videos with that category. Please try again', icon="⚠️")
        # else: 
        st.success('Found match(es)', icon="✅")
        matches = moddf.loc[moddf['title'].str.contains('|'.join(userinputlist), case=False)]
        n_cols = 3
        n_rows = int(1 + len(matches[matches.overallpositivepercentage > 50]) // n_cols)
        rows = [st.columns(n_cols) for _ in range(n_rows)]
        columns = [column for row in rows for column in row]
        for cat, matchvid, matchtitle, matchscore, col in zip(matches['category'], matches['video_id'], matches['title'], matches['overallpositivepercentage'], columns):
            with col:
                # url = f"https://www.youtube.com/watch?v={matchvid}"
                url = f"https://youtu.be/{matchvid}"
                st.image("https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc")
                # st_player(url)
                # st.write(matchtitle)
                st.markdown(f"[{matchtitle}]({url})")
                st.caption(f"Category: {cat}")
                matchscore = round(matchscore)
                matchscore = str(matchscore)+'%'
                st.success(matchscore)
        
            
        
            
            

        # if moddf['title'].str.contains(userinput, case=False).any() == False:
        #     st.warning(f'{choice} has no videos with that category. Please try again', icon="⚠️")
        # else:
        #     st.success('Found match(es)', icon="✅")
        #     matches = moddf.loc[moddf['title'].str.contains(userinput, case=False)]
        #     n_cols = 3
        #     n_rows = int(1 + len(matches[matches.overallpositivepercentage > 50]) // n_cols)
        #     rows = [st.columns(n_cols) for _ in range(n_rows)]
        #     columns = [column for row in rows for column in row]
        #     for cat, matchvid, matchtitle, matchscore, col in zip(matches['category'], matches['video_id'], matches['title'], matches['overallpositivepercentage'], columns):
        #         with col:
        #             # url = f"https://www.youtube.com/watch?v={matchvid}"
        #             url = f"https://youtu.be/{matchvid}"
        #             st.image("https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc")
        #             # st_player(url)
        #             # st.write(matchtitle)
        #             st.markdown(f"[{matchtitle}]({url})")
        #             st.caption(f"Category: {cat}")
        #             matchscore = round(matchscore)
        #             matchscore = str(matchscore)+'%'
        #             st.success(matchscore)
        

        
        
    else:
        st.success(f"Here are the recommendations sorted by positive sentiment scoring of {choice} videos")

        n_cols = 3
        n_rows = int(1 + len(moddf[moddf.overallpositivepercentage > 50]) // n_cols)
        rows = [st.columns(n_cols) for _ in range(n_rows)]
        cols = [column for row in rows for column in row]

        for cat, col, vid, title, score in zip(moddf['category'], cols, moddf['video_id'], moddf['title'], moddf['overallpositivepercentage']):
            with col:
                url = f"https://youtu.be/{vid}"
                st.image("https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc")
                # st_player(f"https://youtu.be/{vid}")
                st.markdown(f"[{title}]({url})")
                st.caption(f'Category: {cat}')
                # st.caption(f"Category: {cat}")
                score = round(score)
                score = str(score)+'%'
                st.success(score)