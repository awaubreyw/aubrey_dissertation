import streamlit as st
import pandas as pd
import json
import emoji
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

st.title("Comment Analyzer & Visualizer")

channel = st.session_state.channelkey
channel = channel.replace(' ', '_').lower()
st.write(channel)



file = f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}.json' 
data = None

with open(file, 'r') as f:
    data = json.load(f)
    st.json(data)

channel_id, stats = data.popitem()

channel_stats = stats['channel_statistics']

video_stats = stats['video_data']

opt = st.radio('Analyses of top 10 videos based on: ', ['viewCount', 'likeCount'])

if opt == 'viewCount':
    sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse=True)
else:
    sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['likeCount']), reverse=True)

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


top10 = df.head(10)
st.dataframe(top10)

# with st.container():
#     if opt == 'viewCount':
#         ax = top10.plot.bar(x='title', y='views', figsize=(12,8), fontsize=14)
#     else:
#         ax = top10.plot.bar(x='title', y='likes', figsize=(12,8), fontsize=14)

# likes_avg = top10['likes'].mean()
# comments_avg = top10['comments'].mean()
# views_avg = top10['views'].mean()

# overallpositivepercentage = []
# overallneutralpercentage = []
# overallnegativepercentage = []

# filter = top10['comments'] == 0
# top10 = top10.drop(index=df[filter].index)

# for index, row in top10.iterrows():
# #for videoID in top10['video_id']:
#     videoID = row['video_id']
#     video_title = row['title']

#     dataframe = pd.read_json(f'C:/xampp/htdocs/aubrey_dissertation/src/results/{channel}/{videoID}.json')
# #     text_data = pd.read_json(f'../results/crashcourse/{video_id}.json')

# # def get_sentiment(text:str, analyserobj,desired_type:str='pos'):
# #     # Get sentiment from text
# #     sentiment_score = analyserobj.polarity_scores(text)
# #     return sentiment_score[desired_type]


# # # Get Sentiment scores
# # def get_sentiment_scores(df,data_column):
# #     sentimentlist = [] #empty list should be here because if looped through all videos of a channel, sentimentlist should renew
    
# #     #df[f'{data_column} negative'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'neg'))
# #     df['negative'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'neg'))
# #     df['neutral'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'neu'))
# #     df['positive'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'pos'))
# #     df['compound'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'compound'))
    
# #     for comp in df['compound']:
# #         if comp >= 0.05:
# #             sentiment = 'positive'
# #         elif comp <= -0.05:
# #             sentiment = 'negative'
# #         else:
# #             sentiment = 'neutral'
            
# #         sentimentlist.append(sentiment)

# #     df['sentiment'] = sentimentlist
    
# #     return df
    
# # text_sentiment = get_sentiment_scores(text_data, 'comment_text')
    
#     positive = []
#     negative = []
#     neutral = []
#     compound = []
#     sentiment = []

#     for line in range(dataframe.shape[0]): 

#         comments = dataframe.iloc[line, 1] 
#         comments_analyzed = analyzer.polarity_scores(comments)

    
#         if comments_analyzed["compound"] >= 0.05:
#             eachsentiment = 'positive'
#         elif comments_analyzed["compound"] <= -0.05:
#             eachsentiment = 'negative'
#         else:
#             eachsentiment = 'neutral'
    

# #RUN ONCE
#         negative.append(comments_analyzed["neg"])

#         positive.append(comments_analyzed["pos"])
      

#         neutral.append(comments_analyzed["neu"])
      

#         compound.append(comments_analyzed["compound"])
   

#         sentiment.append(eachsentiment)


#     dataframe["negative"] = negative 
#     dataframe["neutral"] = neutral
#     dataframe["positive"] = positive
#     dataframe["compound"] = compound
#     dataframe["sentiment"] = sentiment

#     with st.container():
#         st.dataframe(dataframe)
    


#     totalrows = len(dataframe['sentiment'])

#     totalpositivesentiment = ((dataframe['sentiment'].value_counts()['positive'])/totalrows)*100
    
#     totalneutralsentiment = ((dataframe['sentiment'].value_counts()['neutral'])/totalrows)*100

#     totalnegativesentiment = ((dataframe['sentiment'].value_counts()['negative'])/totalrows)*100

#     with st.container():
    
#     # averagedsentiments = pd.Series({"positive%": totalpositivesentiment, "neutral%": totalneutralsentiment, "negative%": totalnegativesentiment})

#     # averagedsentiments.plot(kind='bar', rot=0, color=['blue', 'purple', 'red'], title='Normalized sentiments of df1 _O2sg-PGhEg.json', ylim=[0, 100], ylabel='scale', xlabel='sentiment percentages')

#         averagedsentiments = pd.Series({emoji.emojize(':smiling_face:'): totalpositivesentiment, emoji.emojize(':neutral_face:'): totalneutralsentiment, emoji.emojize(':frowning_face:'): totalnegativesentiment})

#         averagedsentiments.plot(kind='bar', rot=0, color=['blue', 'purple', 'red'], title=f'{video_title}', ylim=[0, 100], ylabel='scale', xlabel='sentiment percentages')


#         labels = ['Positive ['+str(totalpositivesentiment)+'%]', 'Negative ['+str(totalnegativesentiment)+'%]', 'Neutral ['+str(totalneutralsentiment)+'%]']
#         sizes = [totalpositivesentiment, totalnegativesentiment, totalneutralsentiment]
#         colors = ['blue','red', 'purple']
#         patches, texts = plt.pie(sizes, colors=colors, startangle=90)
#         plt.legend(patches,labels,loc="best")

#         plt.title(f"{video_title}") 

#         plt.axis('equal')
#         plt.tight_layout()
#         plt.show()










#     overallpositivepercentage.append(totalpositivesentiment)
#     overallneutralpercentage.append(totalneutralsentiment)
#     overallnegativepercentage.append(totalnegativesentiment)


# top10["overallpositivepercentage"] = overallpositivepercentage
# top10["overallneutralpercentage"] = overallneutralpercentage
# top10["overallnegativepercentage"] = overallnegativepercentage

# top10 = top10.sort_values(by=['overallpositivepercentage'], ascending=False)

# with st.container():
#     st.write('---')
#     barr = top10.plot.bar(x='title', y='overallpositivepercentage')

# #df1.nlargest(5, ['positive'])
# #df1.nlargest(5, ['compound'])

# with st.container():
#     st.dataframe(top10)
















