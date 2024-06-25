import os
from pipes import quote
import struct
import subprocess
import time
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import re
import webbrowser
import sqlite3
import pvporcupine


from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("wisdom.db")
cursor = con.cursor()

# wisdom startup sound

def playAssistantsound():
    music_dir = "www\\assets\\sound\\jarvis_advance_sound.mp3"
    music_dir2 = "www\\assets\\sound\\jarvis_at_your_service.mp3"
    playsound(music_dir2)
    playsound(music_dir)

@eel.expose
def postassistantsound():
    music_dir = "www\\assets\\sound\\start_sound.mp3"
    playsound(music_dir)

# To open a application or website we are using openCommand function

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+ query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    # speak("यूट्यूब पर "+search_term+" चलाता हूँ, सर")
    speak("Playing "+search_term+" on Youtube")
    kit.playonyt(search_term)

def hotword(): 
    porcupine=None 
    paud=None 
    audio_stream=None 
    try: 
        
        # pre trained keywords     
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"])  
        paud=pyaudio.PyAudio() 
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length) 
         
        # loop for streaming 
        while True: 
            keyword=audio_stream.read(porcupine.frame_length) 
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword) 
 
            # processing keyword comes from mic  
            keyword_index=porcupine.process(keyword) 
 
            # checking first keyword detetcted for not 
            if keyword_index>=0: 
                print("hotword detected") 
 
                # pressing shorcut key win+j 
                import pyautogui as autogui 
                autogui.keyDown("win") 
                autogui.press("j") 
                time.sleep(2) 
                autogui.keyUp("win")

    except Exception as e:
        print(f"error: {e}")

# Using find contacts function to find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "starting video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    user_input = query
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

def exitnow():
    a = input("Are you sure you want to exit")

    if a == "yes" or "YES":
        exit()
    elif a == "no" or "NO":
        pass
    else:
        print("Please write yes or no")

@eel.expose()
def htmlexit():
    exit()