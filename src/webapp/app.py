import streamlit as st
# import json
# import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon=":female-detective:") #page_icon="🕵️‍♀️"

def main():
    st.title("Project CAV²R")
    st.subheader("Welcome!")

    st.sidebar.info("Select an educational channel or a category for recommendations of videos with the most positive sentiment.")
    
    st.sidebar.success("Select a page above.")
    
    channels = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']

    choice = st.sidebar.selectbox(channels, key='channelkey')
    #or choice = st.sidebar.radio(channels, key='channelkey')

    if 'channelkey' not in st.session_state:
        st.session_state['channelkey'] = channels[0]

    st.session_state['channelkey'] = choice

    # for channel_name in channels:
    #     if choice == channel_name: 
    if choice:
        st.subheader(f"You have selected {choice}")
    #         channel = choice.replace(' ', '_').lower()
    #         st.session_state.channelkey = channel

    

if __name__ == '__main__':
    main()
#MAIN PAGE

#Comment Analyzer, Visualizer & Video Recommender

#USER INTERFACE

# with st.sidebar:
#     selected = option_menu(
#         menu_title="Main Menu",
#         menu_icon="map",
#         options=["Home", "About", "Sentiment Analysis", "Recommendations"],
#         icons=["door-open", "file-ruled", "clipboard-data", "clipboard2-check"],
#         default_index=0,
#     ) 

# with st.sidebar:
#     selected = option_menu(
#         menu_title=None,
#         options=["Home", "About", "Sentiment Analysis", "Recommendations"],
#         icons=["door-open", "file-ruled", "clipboard-data", "clipboard2-check"],
#         default_index=0,
#         orientation="horizontal"
#     ) #https://icons.getbootstrap.com/

#     if selected == "Home":
#         st.title(f"You have selected {selected}")
#     if selected == "About":
#         st.title(f"You have selected {selected}")
#     if selected == "Sentiment Analysis":
#         st.title(f"You have selected {selected}")
#     if selected == "Recommendations":
#         st.title(f"You have selected {selected}")
#     #what about session state input containing user input channel name?




#https://www.webfx.com/tools/emoji-cheat-sheet/

#USER INTERFACE






# st.sidebar.info("Select an educational channel or a category for recommendations of videos with the most positive sentiment.")

# with st.sidebar:
#     #drop down menu of channel options
#     channel_names = ['Crashcourse', 'Khan Academy', 'MinutePhysics', 'Deep Look', 'VSauce', '3Blue1Brown', 'Everyday Astronaut', 'SciShow', 'Physics Girl', 'Primer', 'ASAPScience', 'TKOR', 'Kurzgesagt', 'SmarterEveryday', 'Science Channel', 'Veritasium', 'NileRed']
#     channel_name = st.radio('Pick one', channel_names)
#     channel_name_chosen = channel_name.replace(' ', '_').lower()
    #AUTOMATE
    #change code in these notebooks to use {channel_name} user chose as input
    #run these ipynb files and display dataframe with st.dataframe()
    #get_sentiment_vader.ipynb 
    #get_top10_sentiment.ipynb 

# jsonfile = f'video_ids_{channel_name_chosen}.json'
# df = pd.DataFrame(f'video_ids_{channel_name_chosen}.json')
# st.dataframe(df) 
# #or 
# for video_id in jsonfile:
#     df = pd.read_json(f'results/{channel_name_chosen}/{video_id}.json')
#     st.dataframe(df) 











# with st.sidebar:
#     #recommender = st.write("[Top Video Recommendations](C:\xampp\htdocs\aubrey_dissertation\src\webapp\recommender.ipynb)")
#     #analyzer = st.write("[Comments Analyses & Visualizations](C:\xampp\htdocs\aubrey_dissertation\src\webapp\analyzer.py)")
#     section = st.radio('Pick one', ('Recommendations', 'Visualizations'))

#     if section == 'Recommendations':
#         st.write("[Top Video Recommendations](C:\xampp\htdocs\aubrey_dissertation\src\webapp\recommender.py)")

#     if section == 'Visualizations':
#         st.write("[Comments Analyses & Visualizations](C:\xampp\htdocs\aubrey_dissertation\src\webapp\analyzer.py)")














# with st.sidebar:
#     #drop down menu of category names
#     categories = ["biology", "how-to", "chemistry", "coding"] #from keywords under channel_info.json or tags under videos in {channelname}.json?
#     options = st.multiselect('Pick one or more', categories) 

#     st.write('you selected: ', options) #options datatype is list with indexes

#     for channel in channel_names:
#       channel = channel.replace(' ', '_').lower()
      
#       with open(f'results/{channel}.json', 'r') as f:
#           data = json.load(f)

#       for channel_id in data:
#           for video_id, video_data in data[channel_id]["video_data"].items():
#               tags = video_data['tags']
#               title = video_data['title']
#     #but some channels' videos do not have tags, so throw an exception

#     # mylist = list(dict.fromkeys(categories)) #no duplicates method

#     for option in options:
#         if option.casefold() in tags.casefold():
#             st.video(f'https://www.youtube.com/watch?v={video_id}')
#             #or
#             st.write(f'[{title} >](https://www.youtube.com/watch?v={video_id})')




    