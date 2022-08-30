# my dissertation 
😣❗
## python interpreter: 3.9.13 ('.venv': venv)

1. `python -m venv .venv`
2. `pip freeze > requirements.txt` or `pip3 freeze | Out-File -FilePath requirements.txt`
3. `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
4. `.venv\Scripts\activate`
5. `.venv\Scripts\pip.exe install pandas (or another)`
6. powershell command to find number of files = `(ls src/results/crashcourse | Measure-Object -line).Lines`
7. shortcut to comment out multiple lines = ctrl + /

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


**Project Scale and Scope**
- top 10 videos based on views
- sentiment scores, findings and insights
- top 10 videos with highest positive sentiment scores
- 17 english-only educational channels with a minimum of 1 million subs 
- visualizations and recommendations of the best videos of the same tags/genres/categories on Streamlit web app 

**Feedback from meeting with supervisor (30/08/2022)**
**ToDo list:**
- [ ] web app UI wireframe draw.io
- [ ] normalize sentiments to be able to fairly compare against various videos on a constant scale (bar chart's y-axis labelled as percentage)
- [ ] automate and reuse sentiment analysis code to present top 10 most positively acclaimed videos 

