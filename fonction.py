from tkinter import *
from tkinter import ttk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
from typing import Text
import requests, uuid, json
import os
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

camera1="https://dl.etna-alternance.net/activities/RTP-CLO2/001/project/France%20Inter/public/ressources/deux.jpeg?md5=hloWyJbiq6oRMTiIyviqZw&expires=1626187947"
camera2="https://dl.etna-alternance.net/activities/RTP-CLO2/001/project/France%20Inter/public/ressources/trois.jpg?md5=aiVgHAc1KcKYr0wJ5k0uag&expires=1627247766"
camera3="https://dl.etna-alternance.net/activities/RTP-CLO2/001/project/France%20Inter/public/ressources/quatre.jpg?md5=TKOuYznPsnH9cAiN7VHc_A&expires=1626176362"
camera4="https://dl.etna-alternance.net/activities/RTP-CLO2/001/project/France%20Inter/public/ressources/sept.jpeg?md5=yLXdfNod5ZZjdTfgYAcltQ&expires=1626176376"
camera5="https://dl.etna-alternance.net/activities/RTP-CLO2/001/project/France%20Inter/public/ressources/neuf.jpg?md5=n4pd9I06FNIdSSjv6btBUg&expires=1626176389"
globalcam = ""
globalper = ""

def selectcam(event):
    select = listecombo.get()
    global globalcam
    if select == "camera1":
        globalcam=camera1
    elif select == "camera2":
        globalcam=camera2
    elif select == "camera3":
        globalcam=camera3
    elif select == "camera4":
        globalcam=camera4
    elif select == "camera5":
        globalcam=camera5

def perseclect(event):
    prsselect = listepers.get()
    global globalper
    if prsselect == "1":
        globalper=1
    elif prsselect == "2":
        globalper=2
    elif prsselect == "3":
        globalper=3
    elif prsselect == "4":
        globalper=4
    elif prsselect == "5":
        globalper=5

def Franceinter():
    subscription_key = "8015e2285a864d899de55000d9e0cd01"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    KEY = "6b6d276f0b9044a2a6eb3000e5be1f53"
    ENDPOINT = "https://tete.cognitiveservices.azure.com/"
    speech_key, service_region = "180359c21aef4877a11c7b23517bed2c", "francecentral"
    location = "francecentral"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'fr',
        'to': ['en']
    }
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config = SpeechConfig(subscription="4b12e5cc013143a89e32915937b747b4", region="francecentral")

    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    single_face_image_url = globalcam
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))

    nbr = 0
    for face in detected_faces:
        nbr = nbr+1

    three_image_face_ID = detected_faces[0].face_id

    nbrper = globalper
    with open('nombre.txt', 'w') as txtfile:
        json.dump(nbrper, txtfile)

    nbrpersonne = int(nbrper)

    body = [{
        'text': ''
    }]
    body[0]['text'] = entry.get()
    
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    trad = response[0]['translations'][0]['text']

    if nbr > nbrpersonne:
        audio_config = AudioOutputConfig(use_default_speaker=True)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(entry.get())
        audio_config = AudioOutputConfig(filename="audio_fr.wav")
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        test = AudioOutputConfig(filename="audio_en.wav")
        synthesizer2 = SpeechSynthesizer(speech_config=speech_config, audio_config=test)
        result = synthesizer.speak_text_async(entry.get())
        result2 = synthesizer2.speak_text_async(trad).get()

    else:
        audio_config = AudioOutputConfig(filename="audio_fr.wav")
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        test = AudioOutputConfig(filename="audio_en.wav")
        synthesizer2 = SpeechSynthesizer(speech_config=speech_config, audio_config=test)
        result = synthesizer.speak_text_async(entry.get())
        result2 = synthesizer2.speak_text_async(trad).get()

window = Tk()
window.geometry("700x300")

label = Label(text="Quel caméra ?")
label.pack()

listeder = ["camera1", "camera2", "camera3", "camera4", "camera5"]
listecombo = ttk.Combobox(values=listeder)
listecombo.current(0)
listecombo.bind("<<ComboboxSelected>>", selectcam)
listecombo.pack()

quest = Label(text="Combien de personne sont admises en simultanées dans le studio")
quest.pack()

nombre = ["1", "2", "3", "4", "5"]
listepers = ttk.Combobox(values=nombre)
listepers.current(0)
listepers.bind("<<ComboboxSelected>>", perseclect)
listepers.pack()

quest = Label(text="Message à faire passer ")
quest.pack()

entry = Entry(width=50)
entry.pack()

btn = Button(window, height=1, width=10, text="Traduire", bg="red", command=Franceinter)
btn.pack()

window.mainloop()