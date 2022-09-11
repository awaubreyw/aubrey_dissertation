import streamlit as st
import pandas as pd

data = pd.read_json('C:/xampp/htdocs/aubrey_dissertation/src/constants/channel_info.json')

# st.write(data)
    
df = pd.DataFrame(data)

st.dataframe(df.style.highlight_max(axis=0))

st.bar_chart(df, y='subs', x='channel_title')