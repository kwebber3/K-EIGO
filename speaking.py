from tkhtmlview import *
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import random
import re

from background import *

DICTIONARY_NAME = "listening_Speaking.txt"

JP_INDEX = 0
ENG_INDEX = 1
JP_SENT_INDEX = 2
ENG_SENT_INDEX = 3

class Speaking(Toplevel,):
    def __init__(self):
        Toplevel.__init__(self) 
        self.title("Speaking")
        self.state("zoomed")
        self.grab_set()
        self.my_scored_cards, self.score_weights, self.number_of_cards = load_speaking_dictionary(DICTIONARY_NAME)      
        self.last_score = -1

        self.show_button1 = tkinter.Button(self, text="Show Example", command=lambda:self.ShowExample())
        self.show_button1.grid(row=0, column=0)

        self.show_button2 = tkinter.Button(self, text="Show Answer", command=lambda:self.ShowAnswer())
        self.show_button2.grid(row=0, column=1)

        self.right_button = tkinter.Button(self, text="Correct", command=lambda:self.AddPoint())
        self.right_button.grid(row=1, column=0)

        self.wrong_button = tkinter.Button(self, text="Wrong", command=lambda:self.SubtractPoint())
        self.wrong_button.grid(row=1, column=1)

        self.GetCard()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        self.SaveResults()
        self.destroy()

    def SaveResults(self):
        export_speakingLibrary_to_txt(self.my_scored_cards,DICTIONARY_NAME)

    def GetCard(self):
        self.card_panel = tkinter.Frame(self)
        self.card_panel.grid(row=2,column=0,columnspan=2)
        self.score_weights = update_weights(self.my_scored_cards, self.number_of_cards)
        self.current_score = random.choices(range(1,len(self.score_weights)+1),weights = self.score_weights)[0]
        self.current_score, self.current_card, status = get_card_advanced(self.current_score,self.last_score,self.my_scored_cards, self.score_weights)
        
        if status == "GOOD":
            Japanese = self.current_card[JP_INDEX]
            English = re.sub("@","\n",self.current_card[ENG_INDEX])
            Japanese_Example = re.sub("@","\n",self.current_card[JP_SENT_INDEX])
            English_Sentence = re.sub("@","\n",self.current_card[ENG_SENT_INDEX])
            Japanese_Example = re.sub("<[/]*b>","",Japanese_Example)

            tkinter.Label(self.card_panel, text=English, font="Helvetica 36").grid(row=0,column=0)
            self.hint_sentence = tkinter.Label(self.card_panel, text=English_Sentence, font="Helvetica 30")
            self.hint_sentence.grid(row=0,column=1)
            self.hint_sentence.grid_remove()
            self.answer = tkinter.Label(self.card_panel, text=Japanese, font="Helvetica 36")
            self.answer.grid(row=1,column=0)
            self.answer.grid_remove()
            self.example = tkinter.Label(self.card_panel, text=Japanese_Example, font="Helvetica 30")
            self.example.grid(row=1,column=1)
            self.example.grid_remove()
        elif status == "ERROR":
            self.show_button1.destroy()
            self.show_button2.destroy()
            self.wrong_button.destroy()
            self.right_button.destroy()
            tkinter.Label(self, text="PRACTICE LISTENING MORE").grid(column=0, row = 0)

    def ShowExample(self):
        self.hint_sentence.grid(row=0,column=1)

    def ShowAnswer(self):
        self.answer.grid(row=1,column=0)
        self.example.grid(row=1,column=1)

    def AddPoint(self):
        this_card = self.my_scored_cards[self.current_score].pop(0)
        if (self.current_score + 1 > MAX_SCORE):
            new_score = MAX_SCORE
        else:
            new_score = self.current_score + 1
        self.my_scored_cards[new_score].append(this_card)
        self.card_panel.destroy()
        self.last_score = new_score
        self.GetCard()
    
    def SubtractPoint(self):
        this_card = self.my_scored_cards[self.current_score].pop(0)
        if (self.current_score - 1 < START_SCORE):
            new_score = START_SCORE
        else:
            new_score = self.current_score - 1
        self.my_scored_cards[new_score].append(this_card)
        self.card_panel.destroy()
        self.last_score = new_score
        self.GetCard()
        #print(this_card)