#CREDITS https://jackmckew.dev/sentiment-analysis-text-cleaning-in-python-with-vader.html
#on code for consolidating top videos with highest overall positive sentiments
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import pd

analyzer = SentimentIntensityAnalyzer()

text_data = pd.read_table('original_rt_snippets.txt',header=None) 




def get_sentiment(text:str, analyserobj,desired_type:str='pos'):
    # Get sentiment from text
    sentiment_score = analyserobj.polarity_scores(text)
    return sentiment_score[desired_type]





# Get Sentiment scores
def get_sentiment_scores(df,data_column):
    df[f'{data_column} Positive Sentiment Score'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'pos'))
    df[f'{data_column} Negative Sentiment Score'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'neg'))
    df[f'{data_column} Neutral Sentiment Score'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'neu'))
    df[f'{data_column} Compound Sentiment Score'] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,analyzer,'compound'))
    return df





text_sentiment = get_sentiment_scores(text_data,0)





def print_top_n_reviews(df,data_column,number_of_rows):
    for index,row in df.nlargest(number_of_rows,data_column).iterrows():
        print(f"Score: {row[data_column]}, Review: {row[0]}")

print_top_n_reviews(text_sentiment,'0 Positive Sentiment Score',5)


