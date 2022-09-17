
from audioop import mul
from email.policy import default
import streamlit as st
import pandas as pd
import numpy as np
import json
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import os.path
import matplotlib.pyplot as plt



analyzer = SentimentIntensityAnalyzer()
st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🎓") 

# back = st.button('Go back', on_click=st.experimental_rerun)
# st.markdown(f"[{back}](https://github.com/awaubreyw/aubrey_dissertation/blob/main/src/webapp/app.py)", unsafe_allow_html=True)
st.title("🌄Project CAV²R⛏️")
st.header("Comment Analyzer & Visualizer")

channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']

# choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')

# if 'channelkey' not in st.session_state:
#     choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey', index=0)

# choice = st.session_state['channelkey']
st.session_state.update(st.session_state)
# if 'channelkey' not in st.session_state:
#     st.session_state['channelkey'] = choice
choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey')


with st.sidebar:
    st.success(f"You have chosen {choice}!")
    st.write('session state: ', st.session_state.channelkey)

channel = choice.replace(' ', '_').lower()

data = None

# file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 
file = f'src/webapp/pages/../../results/{channel}.json' 

with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']


#function for first set of cola and colb
# @st.cache(allow_output_mutation=True)
def visualize_before_sentiment(order: str, col:str):
    st.subheader(f"""{choice} Top 10 Videos\n\nordered by {order}""")

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
    df = df.sort_values(by=[col], ascending=False)
    df.drop(df.loc[df['comments']==0].index, inplace=True)
    df = df.reset_index(drop=True)

    topten = df.head(10)
  
    topten = topten.sort_values(by=[col], ascending=False)
    st.dataframe(topten.style.highlight_max(axis='columns', subset=[col]))
    st.caption("videos that have comments disabled were filtered out for sentiment analysis purposes")
    # st.caption("Fig. 1: videos that have comments disabled (comments == 0) were filtered out")
 
    likes_avg = topten['likes'].mean()
    comments_avg = topten['comments'].mean()
    views_avg = topten['views'].mean()

    st.subheader('Averages')
    
    rad = st.radio(f'{choice} stats averages', ['views', 'likes', 'comments'], key={order})
    if rad == 'views':
        st.markdown(f""" 
        Average number of views under a {choice} top 10 video : **{int(views_avg)} views**""")
    elif rad == 'likes':
        st.markdown(f""" 
        Average number of likes under a {choice} top 10 video : **{int(likes_avg)} likes**""")
    else:
        st.markdown(f""" 
        Average number of comments under a {choice} top 10 video : **{int(comments_avg)} comments**""")

    st.subheader("Data Correlations")
    st.write(topten.corr())
    # st.caption("Fig. 2")

    return topten




@st.cache(allow_output_mutation=True)
def read_video_data_loop(top10):

    overallpositivepercentage = []
    overallneutralpercentage = []
    overallnegativepercentage = []

    
    for videoID in top10['video_id']:
        
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
    
    # return dataframe, overallpositivepercentage, overallneutralpercentage, overallnegativepercentage
    return overallpositivepercentage, overallneutralpercentage, overallnegativepercentage



# @st.cache(allow_output_mutation=True)
@st.cache(suppress_st_warning=True)
def individual_vid_pie(onevidchoice):

    filepath = f'src/webapp/pages/../../results/{channel}/{onevidchoice}.json'
    if os.path.exists(filepath):
        onedataframe = pd.read_json(filepath)   

        positive = []
        negative = []
        neutral = []
        compound = []
        sentiment = []

        for line in range(onedataframe.shape[0]): 

            comments = onedataframe.iloc[line, 1] 
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

        onedataframe["negative"] = negative 
        onedataframe["neutral"] = neutral
        onedataframe["positive"] = positive
        onedataframe["compound"] = compound
        onedataframe["sentiment"] = sentiment

        totalrows = len(onedataframe['sentiment'])

        if onedataframe['sentiment'].str.contains('positive').any():
            totalpositivesentiment = ((onedataframe['sentiment'].value_counts()['positive'])/totalrows)*100
            
        if onedataframe['sentiment'].str.contains('negative').any():
            totalnegativesentiment = ((onedataframe['sentiment'].value_counts()['negative'])/totalrows)*100
            
        if onedataframe['sentiment'].str.contains('neutral').any():        
            totalneutralsentiment = ((onedataframe['sentiment'].value_counts()['neutral'])/totalrows)*100
    else:
        st.warning("Choose another one. The comment file for that video was not extracted/is not in directory")
        
    return onedataframe, totalpositivesentiment, totalnegativesentiment, totalneutralsentiment

#second set of cola and colb


def visualize_after_sentiment(top10, by: str):
    with st.spinner('Please wait... analyzing'):
        time.sleep(5)      
    
    overallpositivepercentage, overallneutralpercentage, overallnegativepercentage = read_video_data_loop(top10)
    
    st.subheader(f'Normalized Sentiment Scoring\n\nof each {choice} video')
    vididlist = []
    for onevidid in top10['video_id']:
        if os.path.exists(f'src/webapp/pages/../../results/{channel}/{onevidid}.json'):
            vididlist.append(onevidid)
    # onevidopt = st.selectbox(f'Pick one {choice} video id to see its sentiment analysis results', top10['video_id'])
    onevidopt = st.selectbox(f'Pick one {choice} video id to see its sentiment analysis results', vididlist)
    st.caption("if options do not include all of top 10 video ids, some video comment json files were not extracted due to API quota")
    dataframe, totalpositivesentiment, totalnegativesentiment, totalneutralsentiment = individual_vid_pie(onevidopt)
    
    
    picker = st.radio('Pick one visual', ['dataframe', 'pie chart'], key={by})
    if picker == 'dataframe':
        with st.expander("Dataframe of chosen video's comments"):
            secondpicker = st.multiselect('Pick any comment sentiment(s)',
            options=dataframe['sentiment'].unique(), key={by+'firstkey'}, default=dataframe['sentiment'].unique())
            modifieddataframe = dataframe.query('sentiment == @secondpicker')
            modifieddataframe = modifieddataframe.sort_values(by=['compound'], ascending=False)
            st.dataframe(modifieddataframe)

    # st.dataframe(dataframe.style.highlight_max(axis='rows', subset='positive'))

    # st.caption("An example of what one YouTube video's comments dataframe after vaderSentiment looks like")
    else:
        labels = ['😃', '☹️', "😐"]
        sizes = [totalpositivesentiment, totalnegativesentiment, totalneutralsentiment]
        # colors = ['blue', 'red', 'purple']
        #patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        #plt.legend(patches,labels,loc="best")
        fig = plt.figure(figsize=(10, 4))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        # ax.axis('equal')
        st.pyplot(fig)
    # st.caption("Normalized sentiment scoring of the above YouTube video comments")
    # plt.tight_layout()
    # plt.show()

    st.write('---')
    


    top10["overallpositivepercentage"] = pd.Series(overallpositivepercentage)
    top10["overallneutralpercentage"] = pd.Series(overallneutralpercentage)
    top10["overallnegativepercentage"] = pd.Series(overallnegativepercentage)
    top10 = top10.fillna(0)
    
    top10 = top10.sort_values(by=['overallpositivepercentage'], ascending=False)
    
    st.subheader(f"Overall Sentiments of {choice} Videos\n\n from most positive to least (similar logic used in recommender)")
    
    st.dataframe(top10.style.highlight_max(axis='columns', subset=['overallpositivepercentage']))
    st.caption("if there are missing sentiment scores for some videos, some video comment json files were not extracted due to API quota")
    
    # st.caption("Fig. 5")
    with st.expander('Comparisons with bar charts📊'):
        # st.write(alt.Chart(top10).mark_bar().encode(x=alt.X('title', sort=None),y=by))
        # st.caption("Fig. 3")
        # st.altair_chart(alt.Chart(top10).mark_bar().encode(
        # x=alt.X('title', sort=None),
        # y=by), use_container_width=True)

        st.write('Filters for comparisons with bar charts📊')
        sentimentpercentageopt = st.radio('Pick one overall video sentiment', ['positive', 'neutral', 'negative'], key={by+by})
        if sentimentpercentageopt == 'positive':
            # st.write(alt.Chart(top10).mark_bar().encode(
            # x=alt.X('title', sort=None),
            # y='overallpositivepercentage'))
            # st.caption("Fig 4")
            st.altair_chart(alt.Chart(top10).mark_bar().encode(
            x=alt.X('title', sort=None),
            y='overallpositivepercentage'), use_container_width=True)
        elif sentimentpercentageopt == 'neutral':
            # st.write(alt.Chart(top10).mark_bar().encode(
            # x=alt.X('title', sort=None),
            # y='overallneutralpercentage'))
            st.altair_chart(alt.Chart(top10).mark_bar().encode(
            x=alt.X('title', sort=None),
            y='overallneutralpercentage'), use_container_width=True)
        else:
            # st.write(alt.Chart(top10).mark_bar().encode(
            # x=alt.X('title', sort=None),
            # y='overallnegativepercentage'))
            st.altair_chart(alt.Chart(top10).mark_bar().encode(
            x=alt.X('title', sort=None),
            y='overallnegativepercentage'), use_container_width=True)
        # st.write(alt.Chart(top10).mark_bar().encode(x=alt.X('title', sort=None),y=by))
        # st.caption("Fig. 3")
        st.altair_chart(alt.Chart(top10).mark_bar().encode(
        x=alt.X('title', sort=None),
        y=by), use_container_width=True)

    with st.expander('Comparisons with line chart📈'):
        st.write('Filters for comparisons with line chart📈')
        multisentimentpercentageopt = st.multiselect('Pick any video sentiment(s)',
        options=['overallpositivepercentage', 'overallneutralpercentage', 'overallnegativepercentage'], key={by+'secondkey'}, default=['overallpositivepercentage', 'overallneutralpercentage', 'overallnegativepercentage'])
        # multiselecttop10 = top10.query("top10.columns==@multisentimentpercentageopt")
        st.line_chart(top10, x='title', y=list(multisentimentpercentageopt), use_container_width=True)
        

        
        # st.caption("Fig. 6")

    with st.expander('Correlation using scatter plot🔵'):
    # making the scatter plot on latitude and longitude 
        st.write('Filters for correlation using scatter plot🔵')
        scattersentimentpercentageopt = st.radio('Pick one overall video sentiment', ['positive', 'neutral', 'negative'], key={by+by+by})
        if scattersentimentpercentageopt == 'positive':
            fig = alt.Chart(top10).mark_point().encode(x='overallpositivepercentage',y=by)
        elif scattersentimentpercentageopt == 'neutral':
            fig = alt.Chart(top10).mark_point().encode(x='overallneutralpercentage',y=by)
        else:
            fig = alt.Chart(top10).mark_point().encode(x='overallnegativepercentage',y=by)
        st.altair_chart(fig, use_container_width=True)
    # st.caption("Fig. 7")
# making the regression line using transform_regression  
# function and add with the scatter plot 
    # final_plot = fig + fig.transform_regression('overallpositivepercentage','views').mark_line()
    # st.altair_chart(final_plot) 
# saving the scatter plot with regression line 


    st.subheader("Data Correlations")
    st.write(top10.corr())
    # st.caption("Fig. 8")
        

cola, colb = st.columns(2)


with cola:
    st.write('---')
    top10a = visualize_before_sentiment('viewCount', 'views')
    
with colb:
    st.write('---')
    top10b = visualize_before_sentiment('likeCount', 'likes')
   

with cola:
    st.write('---')
    visualize_after_sentiment(top10a, 'views')

with colb:
    st.write('---')
    visualize_after_sentiment(top10b, 'likes')


# st.session_state.clear
del st.session_state['channelkey']
