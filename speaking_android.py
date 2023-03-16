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

from background import *

DICTIONARY_NAME = "Listening_Speaking.txt"

JP_INDEX = 0
ENG_INDEX = 1
JP_SENT_INDEX = 2
ENG_SENT_INDEX = 3

class SpeakingBox(BoxLayout,):
    def build(self):
        self.my_scored_cards, self.score_weights, self.number_of_cards = load_speaking_dictionary(DICTIONARY_NAME)      
        self.last_card = []
        self.orientation = "vertical"
        self.buttonBar = BoxLayout(orientation = "horizontal")
        self.show_button = Button(text="例文", on_press=partial(self.ShowExample))
        self.buttonBar.add_widget(self.show_button)

        self.answer_button = Button(text="回答", on_press=partial(self.ShowAnswer))
        self.buttonBar.add_widget(self.answer_button)

        self.addButton = Button(text="正しい", on_press=partial(self.AddPoint))
        self.buttonBar.add_widget(self.addButton)

        self.subtractButton = Button(text="間違い", on_press=partial(self.SubtractPoint))
        self.buttonBar.add_widget(self.subtractButton)

        
        self.add_widget(self.buttonBar)

        self.cardPrompt = Label(font_name = "DroidSansJapanese")
        self.add_widget(self.cardPrompt)
        self.example = Label(font_name = "DroidSansJapanese")
        self.example.bind(size=self.example.setter('text_size'))    

        self.add_widget(self.example)
        self.answer = Label()

        self.add_widget(self.answer)
        self.sentence_answer = Label()
        self.add_widget(self.sentence_answer)
        self.sentence_answer.bind(size=self.sentence_answer.setter('text_size'))    


        self.GetCard()

    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_request_close=self.end_func)

    def end_func(self, *args):
        self.SaveResults()
        #print("cow died")
        Window.close()
        return True

    def SaveResults(self):
        export_speakingLibrary_to_txt(self.my_scored_cards,DICTIONARY_NAME)

    def GetCard(self):
        self.score_weights = update_weights(self.my_scored_cards, self.number_of_cards)
        self.current_score = random.choices(range(1,len(self.score_weights)+1),weights = self.score_weights)[0]
        self.current_score, self.current_card, status, self.index = get_card_reverse(self.current_score,self.last_card,self.my_scored_cards, self.score_weights)
        
        if status == "GOOD":
            English = self.current_card[JP_INDEX]
            self.cardPrompt.text = English
            self.English = re.sub("@","\n",self.current_card[ENG_INDEX])
            self.English_Example = re.sub("@","\n",self.current_card[ENG_SENT_INDEX])
            self.Japanese_Sentence = re.sub("@","\n",self.current_card[JP_SENT_INDEX])
            self.Japanese_Sentence = re.sub("<[/]*b>","",self.Japanese_Sentence)

        elif status == "ERROR":
            self.cardPrompt.text = "PRACTICE LISTENING MORE"
            self.English = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True
        else:
            self.cardPrompt.text = "Unknown Status"
            self.English = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True

    def refresh(self):
        self.cardPrompt.text = ""
        self.answer.text = ""
        self.example.text = ""
        self.sentence_answer.text = ""

    def ShowExample(self, instance):
        self.example.text = self.Japanese_Sentence

    def ShowAnswer(self, instance):
        self.answer.text = self.English
        self.sentence_answer.text = self.English_Example

    def AddPoint(self, instance):
       # print(self.current_score)
        this_card = self.my_scored_cards[self.current_score].pop(self.index)
        if (self.current_score + 1 > MAX_SCORE):
            new_score = MAX_SCORE
        else:
            new_score = self.current_score + 1
        self.my_scored_cards[new_score].append(this_card)
        self.refresh()
        self.last_card = this_card
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
        self.last_card = this_card
        self.GetCard()
        #print(this_card)