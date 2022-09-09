import streamlit as st
st.title("Comment Analyzer & Visualizer")
with st.container():
    st.dataframe()
    #analyses of top 10 videos based on views

with st.container():
    st.write('---')
    st.dataframe()
    #analyses of top 10 videos based on likes