@st.cache(allow_output_mutation=True)
def recommend_videos(df_arg):
    overallpositivepercentage = []
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



