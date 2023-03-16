from background import *
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang import Builder
from functools import partial
from kivy.core.window import Window
import requests
import random
import re
import gtts
from pydub import AudioSegment
import pydub
from pydub.playback import play
from  plyer import audio
import os

from background import *

DICTIONARY_NAME = "Listening_Speaking.txt"

JP_INDEX = 0
ENG_INDEX = 1
JP_SENT_INDEX = 2
ENG_SENT_INDEX = 3

WINDOWS_KEY = "nt"
ANDROID_KEY = "posix"

class ListeningBox(BoxLayout,):
    def build(self):
        self.my_scored_cards, self.score_weights, self.number_of_cards = load_listening_dictionary(DICTIONARY_NAME)      
        self.last_score = -1
        self.orientation = "vertical"
        self.buttonBar = BoxLayout(orientation = "horizontal")

        self.show_button = Button(text="読み", on_press=partial(self.ShowText))
        self.buttonBar.add_widget(self.show_button)

        self.show_button = Button(text="例文", on_press=partial(self.ShowExample))
        self.buttonBar.add_widget(self.show_button)

        self.answer_button = Button(text="回答", on_press=partial(self.ShowAnswer))
        self.buttonBar.add_widget(self.answer_button)

        self.addButton = Button(text="正しい", on_press=partial(self.AddPoint))
        self.buttonBar.add_widget(self.addButton)

        self.subtractButton = Button(text="間違い", on_press=partial(self.SubtractPoint))
        self.buttonBar.add_widget(self.subtractButton)
        self.add_widget(self.buttonBar)
        
        self.speakButton = Button(text = "聞く", on_press = partial(self.PlayWord))
        self.add_widget(self.speakButton)
        self.cardPrompt = Label()
        self.add_widget(self.cardPrompt)
        self.example = Label()
        self.example.bind(size=self.example.setter('text_size'))    
        self.add_widget(self.example)
        self.answer = Label(font_name = "DroidSansJapanese")
        self.add_widget(self.answer)
        self.sentence_answer = Label(font_name = "DroidSansJapanese")
        self.add_widget(self.sentence_answer)
        self.sentence_answer.bind(size=self.sentence_answer.setter('text_size'))    

        
        self.system = os.name

        self.GetCard()

    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_request_close=self.end_func)

    def end_func(self, *args):
        self.SaveResults()
        #print("cow died")
        Window.close()
        return True
    
    def get_word(self):
        tts = gtts .gTTS( self.Japanese, lang='ja' )  ##  request google to get synthesis
        tts .save( 'temp.mp3' )  ##  save audio
        self.PlayWord("dummy")

    def PlayWord(self, instance):
        if self.system == WINDOWS_KEY:
            word = AudioSegment.from_mp3("temp.mp3")
            play(word)  ##  play audio        elif self.system == ANDROID_KEY:
        elif self.system == ANDROID_KEY:
            audio.file_path = "temp.mp3"
            audio.play()
            

    def SaveResults(self):
        export_listeningLibrary_to_txt(self.my_scored_cards,DICTIONARY_NAME)

    def GetCard(self):
        self.score_weights = update_weights(self.my_scored_cards, self.number_of_cards)
        self.current_score = random.choices(range(1,len(self.score_weights)+1),weights = self.score_weights)[0]
        self.current_score, self.current_card, self.index = get_card(self.current_score,self.last_score,self.my_scored_cards, self.score_weights)
        
       # print(self.current_card)
        self.Japanese = self.current_card[JP_INDEX]
        self.get_word()
        self.English = re.sub("@","\n",self.current_card[ENG_INDEX])
        self.Japanese_Example = re.sub("@","\n",self.current_card[JP_SENT_INDEX])
        self.English_Sentence = re.sub("@","\n",self.current_card[ENG_SENT_INDEX])
        self.Japanese_Example = re.sub("<[/]*b>","",self.Japanese_Example)

    def refresh(self):
        self.cardPrompt.text = ""
        self.answer.text = ""
        self.example.text = ""
        self.sentence_answer.text = ""

    def ShowText(self, instance):
        self.cardPrompt.text = self.English

    def ShowExample(self, instance):
        self.example.text = self.English_Sentence

    def ShowAnswer(self, instance):
        self.answer.text = self.Japanese
        self.sentence_answer.text = self.Japanese_Example

    def AddPoint(self, instance):
       # print(self.current_score)
        this_card = self.my_scored_cards[self.current_score].pop(self.index)
        if (self.current_score + 1 > MAX_SCORE):
            new_score = MAX_SCORE
        else:
            new_score = self.current_score + 1
        self.my_scored_cards[new_score].append(this_card)
        self.refresh()
        self.last_score = new_score
        self.GetCard()
    
    def SubtractPoint(self, instance):
        #print(self.current_score)
        this_card = self.my_scored_cards[self.current_score].pop(self.index)
        if (self.current_score - 1 < START_SCORE):
            new_score = START_SCORE
        else:
            new_score = self.current_score - 1
        self.my_scored_cards[new_score].append(this_card)
        self.refresh()
        self.last_score = new_score
        self.GetCard()
        #print(this_card)