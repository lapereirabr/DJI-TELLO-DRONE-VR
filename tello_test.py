from tello import Tello
import sys
from datetime import datetime
import time
import random
import os
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=0.25)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio,language = "en-IN")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# create recognizer and mic instances
sample_rate = 96000
recognizer = sr.Recognizer()
microphone = sr.Microphone()
#recognizer.energy_threshold = 4000

#Used to Initiliaze Voice Recognition
int_breaker = 0



start_time = str(datetime.now())
file_name =  "command.txt"


f = open(file_name, "r")
commands = f.readlines()

tello = Tello()
for command in commands:
    if command != '' and command != '\n':
        command = command.rstrip()

        if command.find('delay') != -1:
            sec = float(command.partition('delay')[2])
            print ('delay %s' % sec)
            time.sleep(sec)
            pass
        else:
            print(command)
            tello.send_command(command)

w = open(file_name, "w")


while True:
        print ('delay to wait for Voice Recognition')
        time.sleep(5)
        print("SPEAK IN 2 SEC")
        VRcommand = recognize_speech_from_mic(recognizer, microphone)
        print("You said: {}".format(VRcommand["transcription"]))
        print("You said: {}".format(VRcommand["error"]))


        #Final_Command = command["transcription"]
        i = 0
        tempCom = VRcommand["transcription"]
        com_list = tempCom.split()
        command = ""
        #identifies Command

        for word in (com_list):
            print(i)
            if(com_list[i] == "forward" or com_list[i] == "four word" or com_list[i] == "forwards"):
                command += "forward "
                i=i+1
            elif (com_list[i] == "back" or com_list[i] == "backwards" or com_list[i] == "backward"):
                w.write("back ")
                i=i+1
            elif (com_list[i] == "left"):
                w.write("left ")
                i=i+1
            elif (com_list[i] == "right" or com_list[i] == "bright" or com_list[i] == "write" ):
                w.write("right ")
                i=i+1
            elif (com_list[i] == "elevate" or com_list[i].endswith("ate")):
                w.write("up ")
                i=i+1
            elif (com_list[i] == "down" or com_list[i].endswith("own") or com_list[i].endswith("ound")):
                w.write("down ")
                i=i+1
            elif (com_list[i] == "land"):
                w.write("land ")
                i=i+1
            else:
                print("Incorrect Command")
                i=i+1

            #identifies magnitude

        i = 0
        for word in (com_list):
            print("Magnitude of Command to be WRITTEN TO FILE")
            if(com_list[i].isdigit()):
                print("Magnitude of Command to be WRITTEN TO FILE")
                command += com_list[i]
            else:
                i = i + 1
         
        tello.send_command(command)

        if command == "land":
            break;
exit()