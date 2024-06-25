import os
import eel
import playsound
from time import sleep

from engine.features import *
from engine.command import *

def start():
    
    eel.init("www")

    
    postassistantsound()


    os.system('start chrome.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)