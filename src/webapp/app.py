import streamlit as st
# import json
import pandas as pd
from streamlit_option_menu import option_menu
import os.path
import json
import urllib.request

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🕵️‍♀️") 

def main():

    with st.container():
        st.title("Project CAV²R⛏️")
        
        st.header("Welcome!")
        st.subheader("This web page presents to you 17 educational YouTube channels and their data.")
        st.info("For more info: check out other pages on the sidebar", icon="ℹ️")
    
    with st.container():
        # data = pd.read_json('C:/xampp/htdocs/aubrey_dissertation/src/constants/channel_info.json')
        # data = os.path.relpath("C:/xampp/htdocs/aubrey_dissertation/src/constants/channel_info.json", "C:/xampp\htdocs/aubrey_dissertation/src/webapp/app.py")
        # data = pd.read_json("../constants/channel_info.json")

        # with open("src/webapp/../constants/channel_info.json", "r") as f:
        #     data = json.loads(f.read())
        data = pd.read_json("src/webapp/../constants/channel_info.json")
        df = pd.DataFrame(data)
        
        

        # req = urllib.request.Request("https://github.com/awaubreyw/aubrey_dissertation/blob/main/src/constants/channel_info.json")
        # opener = urllib.request.build_opener()
        # f = opener.open(req)
        # jsonn = json.loads(f.read())
        
        
        # filename = "../constants/channel_info.json"
        # with open(filename) as f:
        #     df = pd.DataFrame([json.loads(l) for l in f.readlines()])
        # Shows data frame as expected

        # df = pd.DataFrame(data)
        st.dataframe(df.style.highlight_max(axis='rows', subset=['subs', 'total_videos']))
        
        with st.expander("Details"):
            st.write("""
                The dataframe above contains the (currently static) channel stats as an overview. The maximum number of subscribers and total video uploads are highlighted in yellow :yellow_heart:
            """)
            st.caption("Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.")
            st.caption("Copy to clipboard: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.")
    
    with st.container():
        st.write("---")
        st.subheader("Visualizations of numbers of subscribers and videos of every channel (numeric columns) in the dataframe above.")
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(df, y='subs', x='channel_title')
            with st.expander("Details"):
                st.write("""
                    The chart above shows the (currently static) total number of people that are subscribed to each educational YouTube channel but the subscriptions can increase and people can unsubcribe anytime. Data was extracted in August of 2022.
                """)
        with col2:
            st.bar_chart(df, y='total_videos', x='channel_title')
            with st.expander("Details"):
                st.write("""
                    The chart above shows the (currently static) total number of videos uploaded by each educational YouTube channel but the numbers can change if creators choose to private, delete or upload more videos. Data was collected in August of 2022.
                """)

    
    st.sidebar.info("Select a page above after choosing one channel.", icon="ℹ️")
    
    channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt_–_in_a_nutshell', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']

    choice = st.sidebar.selectbox(label='Pick one YouTube channel', options=channels, key='channelkey', index=0)


    if 'channelkey' not in st.session_state:
        st.session_state['channelkey'] = choice
    
    with st.sidebar:
        st.success(f"You have chosen {choice}!")
        st.write('session state: ', st.session_state.channelkey)

   

if __name__ == '__main__':
    main()

#MAIN PAGE

#Comment Analyzer, Visualizer & Video Recommender

#USER INTERFACE