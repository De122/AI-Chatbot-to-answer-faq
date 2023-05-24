import speech_recognition as s
from chatterbot 
sr=s.Recognizer()

with s.Microphone()  as m:
    audio=sr.listen(m)
    string=sr.recognize_google(audio,language='eng-ind')
    print(string)


