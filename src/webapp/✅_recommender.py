import streamlit as st
st.title("Video Recommender")

channel = st.session_state.channelkey
channel = channel.replace(' ', '_').lower()
#implement logic from C:\xampp\htdocs\aubrey_dissertation\src\webapp\recommender.ipynb

#for loop:
#   st.markdown(f"[Recommend...](https://www.youtube.com/watch?v={id})")