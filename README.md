# my dissertation 
😣❗
## python interpreter: 3.9.13 ('.venv': venv)

`python -m venv .venv`
`pip freeze > requirements.txt`
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
`.venv\Scripts\activate`
`.venv\Scripts\pip.exe install pandas (or another)`
powershell command to find number of files = `(ls src/results/crashcourse | Measure-Object -line).Lines`
shortcut to comment out multiple lines = ctrl + /

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


**Project Scale and Scope**
- top 10 videos based on views
- sentiment scores, findings and insights
- top 10 videos with highest positive sentiment scores
- 17 english-only educational channels with a minimum of 1 million subs 
- visualizations and recommendations of the best videos of the same tags/genres/categories on Streamlit web app 

