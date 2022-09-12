import streamlit as st
import pandas as pd
import json
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

analyzer = SentimentIntensityAnalyzer()

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🕵️‍♀️") 
st.title("Project CAV²R⛏️")
st.header("Comment Analyzer & Visualizer")

choice = st.session_state.channelkey
channel = choice.replace(' ', '_').lower()
    #st.write(channel)


    

file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 
# channel_data = pd.read_json(file)
# st.write(channel_data.head(10))

data = None

with open(file, 'r') as f:
    data = json.load(f)
    #st.json(data)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

#opt = st.radio('Analyses of top 10 videos based on: ', ['viewCount', 'likeCount'])













#function for first set of cola and colb
#order=viewCount | col=views
def visualize_before_sentiment(order: str, col:str):
    st.subheader(f"{choice} videos ordered by {order}")
    sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1][order]), reverse=True)
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

    topten = df.head(10)
  
    
    #st.dataframe(topten)
    
    #topten = topten.drop(index=df[filter].index)
    #st.dataframe(topten.style.highlight_max(axis='rows', subset=['views']))

    topten = topten.sort_values(by=[col], ascending=False)
    st.dataframe(topten.style.highlight_max(axis='columns', subset=[col]))
    st.caption("Fig. 1: videos that have comments disabled (comments == 0) were filtered out")
   
   
    

    likes_avg = topten['likes'].mean()
    comments_avg = topten['comments'].mean()
    views_avg = topten['views'].mean()
    st.markdown(f""" 
    Average number of views under a {choice} top 10 video : **{int(views_avg)} views**\n
    Average number of likes under a {choice} top 10 video : **{int(likes_avg)} likes**\n
    Average number of comments under a {choice} top 10 video : **{int(comments_avg)} comments**""")

    st.subheader("Data Correlations")
    st.write(topten.corr())
    st.caption("Fig. 2")
    
    # filter = topten['comments'] == 0
    # st.write(filter, "these selected indexes are videos that have disabled comments")
    #topten = topten[topten.comments != 0]
    return topten










#second set of cola and colb
def visualize_after_sentiment(top10, by: str):
    with st.spinner('Please wait... analyzing'):
        time.sleep(20)

    top10.drop(top10.loc[top10['comments']==0].index, inplace=True)

    overallpositivepercentage = []
    overallneutralpercentage = []
    overallnegativepercentage = []

    for index, row in top10.iterrows():
        videoID = row['video_id']
        video_title = row['title']
        #st.write(videoID, video_title)
        dataframe = pd.read_json(f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json')
        #st.dataframe(dataframe)
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

        totalpositivesentiment = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100
        
        totalneutralsentiment = ((dataframe['sentiment'].value_counts()['neutral'])/totalrows)*100

        totalnegativesentiment = ((dataframe['sentiment'].value_counts()['negative'])/totalrows)*100

        #averagedsentiments = pd.Series({"positive%": topten, "neutral%": totalneutralsentiment, "negative%": totalnegativesentiment})
        overallpositivepercentage.append(totalpositivesentiment)
        overallneutralpercentage.append(totalneutralsentiment)
        overallnegativepercentage.append(totalnegativesentiment)


    top10["overallpositivepercentage"] = overallpositivepercentage
    top10["overallneutralpercentage"] = overallneutralpercentage
    top10["overallnegativepercentage"] = overallnegativepercentage

    st.write(alt.Chart(top10).mark_bar().encode(
    x=alt.X('title', sort=None),
    y=by))
    st.caption("Fig. 3")

    st.write(alt.Chart(top10).mark_bar().encode(
    x=alt.X('title', sort=None),
    y='overallpositivepercentage'))
    st.caption("Fig. 4")

    top10 = top10.sort_values(by=['overallpositivepercentage'], ascending=False)
    st.subheader(f"{choice} videos sorted by highest positive sentiment score")
    #st.dataframe(topten)
    st.dataframe(top10.style.highlight_max(axis='columns', subset=['overallpositivepercentage']))
    st.caption("Fig. 5: videos that have comments disabled (comments == 0) were filtered out")
    

    
    
    # st.write(alt.Chart(topten).mark_bar().encode(
    # x=alt.X('title', sort=None),
    # y='overallpositivepercentage'))
    # st.bar_chart(topten, x='title', y='overallpositivepercentage')
    # st.bar_chart(topten, y='views', x='title')
    #st.line_chart(topten, x='views', y='overallpositivepercentage')
    #st.line_chart(topten, x='title', y=['views', 'likes', 'comments'])
    st.line_chart(top10, x='title', y=['overallpositivepercentage', 'overallneutralpercentage', 'overallnegativepercentage'])
    st.caption("Fig. 6")

# making the scatter plot on latitude and longitude 
    fig = alt.Chart(top10).mark_point().encode(x='overallpositivepercentage',y=by) 
    st.altair_chart(fig)
    st.caption("Fig. 7")
# making the regression line using transform_regression  
# function and add with the scatter plot 
    # final_plot = fig + fig.transform_regression('overallpositivepercentage','views').mark_line()
    # st.altair_chart(final_plot) 
# saving the scatter plot with regression line 



    st.subheader("Data Correlations")
    st.write(top10.corr())
    st.caption("Fig. 8")















cola, colb = st.columns(2)

with cola:
    top10a = visualize_before_sentiment('viewCount', 'views')
    
with colb:
    top10b = visualize_before_sentiment('likeCount', 'likes')
   



with cola:
    visualize_after_sentiment(top10a, 'views')

with colb:
    visualize_after_sentiment(top10b, 'likes')





















