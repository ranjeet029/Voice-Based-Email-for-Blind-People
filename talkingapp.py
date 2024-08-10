#pip install pyttsx3

import pyttsx3


def talk(audio):
    engine = pyttsx3.init("")

    voice= engine.getProperty('voices') #getting details of current voice

    engine.setProperty('voice', voice[1].id)
    engine.setProperty('rate',110)
    engine.say(audio) 

    engine.runAndWait() 
#----------------------------------------------------------------

