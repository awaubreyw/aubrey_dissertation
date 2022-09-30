import streamlit as st


st.set_page_config(layout="wide", page_title="Project CAV²R", page_icon="🎓") 

# back = st.button('Go back', on_click=st.experimental_rerun)
# # st.markdown(f"[{back}](https://github.com/awaubreyw/aubrey_dissertation/blob/main/src/webapp/app.py)", unsafe_allow_html=True)
# if st.button():
#     raise 

st.title("🌄Project CAV²R⛏️")
st.text("The acronym stands for Comment Analyzer, Visualizer & Video Recommender. Analyzer and Recommender are this app's main features")
# st.header("Want to know more?")
# st.subheader("This web page explains the purpose and functions of the website and what all of the sections in the navigation are for")

with st.expander("Purpose"):
    st.write("""
    Project CAV²R is a Python-based and visualization-heavy web app, built on the open-source framework called Streamlit, that analyzes previously extracted YouTube channel data and video data (focused on comments) with simple, suitable visual graphs. Another purpose of building this software is to find and recommend the best videos of each and every channel based on what their viewers had to say in the comments section. The belief here is that sentiment should be a significant influencing factor in recommendation algorithms. High numbers of likes, and especially views of YouTube videos, do not always mean high positive sentiments on the quality of those videos' content.\n\n
    """)
with st.expander("App"):
    st.write("""
    In the main page, users are introduced to an overview of 17 educational YouTube channels' dataset and below are bar charts which give a clearer display of differences in their subscriberCount and total number of videos. Then, users can select one YouTube channel in the drop down menu to navigate to recommender page for recommendations of videos starting from the video with the most positive sentiment or if they click on the analyzer, they will be brought to a page of sentiment analyses and visualizations of their chosen channel.\n\n
    """)
with st.expander("Recommender"):
    st.write("""
    In the recommender section, videos of all subjects/genres with the most positive sentiment scores are embedded first. The underlying structure implements code from analyzer. Recommendations are decided on the strengths of videos' normalized positive sentiment scoring which is a result of summing up the frequency of mainly positive comments then comparing the averages on a fair scale. Added search bar functionality for users to be able to filter the recommendations of the chosen channel.\n\n
    """)
with st.expander("Analyzer"):
    st.write("""
    In the analyzer section, there are loads of data from comment json files being normalized and run through vader behind the scenes. For a cleaner look, users only see the sentiment analyses results and visualizations. CAV²R goes for the numeric approach which is why there are no emphasis on wordclouds or frequency of positive or negative words. Added a drop down menu to give users the option to choose on which individual videos to analyze and plot into a pie chart. There is no genre/category filter because channel keywords and video tags contained too many uncategorizeable terms.
    """)

st.subheader('Contact')
st.markdown(f"[👨‍💻️Github repo for code details👾](https://github.com/awaubreyw/aubrey_dissertation)")
st.write("[![Follow](https://www.linkedin.com/in/aubreyw/)](https://www.linkedin.com/in/aubreyw/)")
st.caption("Aubrey Widjaya - 2021/2022 QUB MSc Software Development - YouTube Sentiment Analysis Dissertation Individual Project")

st.subheader('Citations')
with st.expander("More"):
    st.text("""
    Google Developers. 2022. YouTube Data API (v3). [online] Available at: <https://developers.google.com/youtube/v3/> 
    
    Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in science & engineering, 9(03), 90-95.
    
    Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

    McKinney, W. (2010, June). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, No. 1, pp. 51-56).

    Satyanarayan, A., Moritz, D., Wongsuphasawat, K., & Heer, J. (2016). Vega-lite: A grammar of interactive graphics. IEEE transactions on visualization and computer graphics, 23(1), 341-350.

    The pandas development team. pandas-dev/pandas: Pandas [Computer software]. https://github.com/pandas-dev/pandas

    VanderPlas, J., Granger, B., Heer, J., Moritz, D., Wongsuphasawat, K., Satyanarayan, A., Lees, E., Timofeev, I., Welsh, B. & Sievert, S. (2018). Altair: interactive statistical visualizations for Python. Journal of open source software, 3(32), 1057.
    """)
# if st.session_state:
#     st.experimental_rerun()

# if st.cache():
#     st.experimental_rerun()

# if st.cache:
#     st.experimental_rerun()

# st.session_state.clear
