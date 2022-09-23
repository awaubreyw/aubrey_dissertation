# my dissertation 
😣❗

**[[Web app](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://awaubreyw-aubrey-dissertation-srcwebappapp-0l7e2c.streamlitapp.com/) was built using [Streamlit](https://docs.streamlit.io/)**

## python interpreter: 3.9.13 ('.venv': venv)

1. `python -m venv .venv`
2. `pip freeze > requirements.txt` or `pip3 freeze | Out-File -FilePath requirements.txt`
3. `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
4. `.venv\Scripts\activate`
5. `.venv\Scripts\pip.exe install pandas (or another)`
6. powershell command to find number of files = `(ls src/results/crashcourse | Measure-Object -line).Lines`
7. shortcut to comment out multiple lines = ctrl + /
8. `streamlit run c:/xampp/htdocs/aubrey_dissertation/src/webapp/app.py` (http://localhost:8501/)

## YOUTUBE DATA API v3 api key credential (confidential)
- stored in creds.py file then imported api_key variable to other files that call the api and request data 
- Python Quick Tip: Hiding Passwords and Secret Keys in Environment Variables (Windows) https://www.youtube.com/watch?v=IolxqkL7cD8

### channel names
```
#Deep Look = KQEDDeepLook, CrashCourse = crashcourse, Khan Akademy = khanacademy, Vsauce = vsauce1, 3Blue1Brown = 3blue1brown, NancyPi = NancyPi, Smarter Every day = smartereveryday, Data Professor = DataProfessor, Kurzgesagt – In a Nutshell = inanutshell, TED Talks = TED, TKOR = Thekingofrandom, AsapSCIENCE = AsapSCIENCE, Michel van Beizen = MichelvanBiezen, Primer = PrimerLearning, Physics Girl = physicsgirl, SciShow = SciShow, and Everyday Astronaut = EverydayAstronaut. 
#science channel = sciencechannelclips, discovery = DiscoveryChannel, discovery uk = DiscoveryTV, veritasium, minutephysics, NileRed, TheRoyalInstitution 
#CrashCourse = crashcourse, Khan Akademy = khanacademy, Vsauce = vsauce1, Serrano.Academy = LuisSerrano, 3Blue1Brown = 3blue1brown, NancyPi = NancyPi, Smarter Every day = smartereveryday, Data Professor = DataProfessor, Kurzgesagt – In a Nutshell = inanutshell, TED Talks = TED, TKOR = Thekingofrandom, AsapSCIENCE = AsapSCIENCE, Michel van Beizen = MichelvanBiezen, Primer = PrimerLearning, Physics Girl = physicsgirl, SciShow = SciShow, and Everyday Astronaut = EverydayAstronaut. 
#EffectiveStudy = EffectiveStudy (no because indian language)
#what about coding? Microsoft Education, Corey Schafer
```


**some videos have comments disabled so extracted comment json files are less than total videos in a channel (e.g crashcourse 1400 videos but 400 comment files)*
**replies under comments are not included in comments json file because they are not always opinions on the actual video*
**some python files for data extraction are done manually per channel id due to api quota limitations*

**Requirements**
- MoSCoW framework/technique for prioritising requirements has 4 categories (must, should, could, won't)
- List of requirements for my web app/software:
1. users must be able to pick one channel name and action/function/goal/section (what to do with chosen channel)
2. channel names must be shown as options in drop down menu
3. actions/features must be shown as pages or sections
4. users could opt to input a youtube video title as an additional feature/tool that accomplishes recommendation functioning or users could opt to choose one video id from a drop down menu to view individual video sentiment analysis 
5. visualizations/figures/charts/graphs should be displayed/featured in analysis section/page if picked
6. dataframes and numericals/scoring/innerworkings could be displayed/included
7. recommended videos starting from the video of the most positive sentiment should appear and be listed out in recommendation section/page if picked
8. thumbnails of embedded youtube video URLs could be added (instead of only listing youtube video titles)
9. users won't be able to interfere/upload/update web app with new youtube videos' or comment files for system security, data and level of sophistication reasons/concerns/limitations
10. users must be able to navigate their way around the software smoothly and have a good user experience (click on Home/App button to return to main dashboard or click on About to read more about problem specification and purpose/aim)
11. users won't be able to select genres/categories (due to uncategorizeable channel keywords or video tags) to produce and organize a recommendation of videos of the same genre (SUBJECT TO CHANGE IN PROJECT PLAN)

**Project Scale and Scope**
- top 10 videos based on views
- top 10 videos based on likes 
- top 10 videos based on highest avg positive sentiment 
- sentiment scores, visualizations, findings and insights
- 17 english-only educational channels benchmarked against a standard of/a minimum of 1 million subs 
- visualizations in analysis page and recommendations of the best videos of the same chosen channel on Streamlit web app 

**Limitations/out of scope**
- web app does not automatically update with records of future educational channels that reach/surpass 1M subs nor future video uploads including their comments. "hosting" the web-app that self updates is out of scope for this project. "future work" would be to improve it so it auto updates and fetches new videos once a day
- web app does not have video genre/category options for users yet (videos are only organized by channels)
- no coding channels in data input because the youtube channels' subscriberCount < 1M. This acts as a control used as a standard of comparison for checking results
- web app does not have access to QUB student credentials database so unable to authenticate log ins (require integration of backends for a professional/sophisticated student learning site)
***Reflect on the methodology of the project and suggest improvements***

**Feedback from meeting with supervisor (30/08/2022)**
- [ ] web app UI wireframe draw.io
- [x] normalize sentiments to be able to fairly compare against various videos on a constant scale (bar chart's y-axis labelled as percentage)
- [x] automate and reuse sentiment analysis code to present top 10 most positively acclaimed videos 
- [ ] compare Commentaire's way of sentiment analysis (qualitative, descriptive, word frequency/word cloud focused) with mine (quantitative, numeric, direct)
- [x] write web app code (referred from streamlit docs and own ipynb notebook analysis code) as functions because a number of web pages require that code (extraction code files do not have to be because temporary usage/run once to only serve a purpose)
