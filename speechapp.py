import speech_recognition as sr

def say():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        r.adjust_for_ambient_noise(source)
        # audio_data = r.record(source, duration=4)
        audio_data = r.listen(source)
        # convert speech to text
        msg = r.recognize_google(audio_data)
        # print(msg)
        return msg

# say()
    
