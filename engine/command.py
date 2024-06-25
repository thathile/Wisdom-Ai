import os
import pyttsx3
import speech_recognition as sr
import eel
import time
from googletrans import Translator

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')       # getting details of current voice
    engine.setProperty('voice', voices[0].id)   # setting voices 0 for male 1 for female
    engine.setProperty('rate', 175)     # setting up new voice rate
    eel.DisplayMessage(text)
    # print(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()



def takecommand():

    r = sr.Recognizer()
    t = Translator()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-IN')
        # query.lower() = t.translate(query.lower() ,dest='en').text
        print(f"user said: {query}")
        eel.DisplayMessage(query.lower())
        time.sleep(2)
       
    except Exception as e:
        return ""

    return query.lower()


@eel.expose
def allCommand(message=1):
    if message == 1:
        query = takecommand()
        print(query.lower())
        eel.senderText(query.lower())
    else:
        query = message
        eel.senderText(query.lower())


    try:


        if "open" in query.lower():
            from engine.features import openCommand
            openCommand(query.lower())
        elif "on youtube" in query.lower():
            from engine.features import PlayYoutube
            PlayYoutube(query.lower())
        
        elif "send a message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send a message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)

        elif "remember that" in query:
                    from engine.config import ASSISTANT_NAME
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = query.replace(ASSISTANT_NAME, "")
                    
                    speak(f"Sir, You told " + rememberMessage)
                    remember = open("engine\\Remember.txt", "a")
                    remember.write(rememberMessage)
                    remember.close()
        elif "what do you remember" in query:
                    remember = open("engine\\Remember.txt", "r")
                    speak("Sir, You told me " + remember.read())

        elif "shutdown the system" in query:
                    speak("Are you sure you want to studown the system")
                    shutUPdown = query
                    if shutUPdown == "yes":
                        os.system("shutdown /s /t 1")

        elif "internet speed" in query:
                    import speedtest

                    try:
                        wifi = speedtest.Speedtest()
                        upload_net = wifi.upload() / 1048576  # Convert to megabytes
                        download_net = wifi.download() / 1048576  # Convert to megabytes
                        print("Your Wifi Upload speed is", upload_net, "megabytes")
                        print("Your Wifi Download speed is", download_net, "megabytes")
                        speak(f"Your Wifi Upload speed is {upload_net} megabytes")
                        speak(f"Your Wifi Download speed is {download_net} megabytes")
                    except ModuleNotFoundError:
                        print("The speedtest module is not installed. Install it using 'pip install speedtest-cli'")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        # elif "exit" or "system close" or "close now" in query.lower():
        #     from engine.features import exitnow
        #     exitnow()

        else:
            from engine.features import chatBot
            chatBot(query.lower())

    except Exception as e:
        print(e)
    eel.ShowHood()

