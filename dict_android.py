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

from jisho_api.word import Word
import csv

LISTENING_SPEAKING_FILENAME = "Listening_Speaking.txt"
READING_WRITING_FILENAME = "Reading_Writing.txt"

class AddButton(Button):
    def __init__(self, Entry, **kwargs):
        super(AddButton, self).__init__(**kwargs)
        self.entry = Entry
        self.text = "暗記カード作成"

class SearchResult(BoxLayout):
    entry = DictProperty()
    on_press = ObjectProperty()

    def on_entry(self, instance, new_obj):
        # handle the DictProperty named show
        #print(new_obj)
        for ch in self.children:
            if isinstance(ch, BoxLayout):
                # remove any previous obj instances
                self.remove_widget(ch)
                break
        if True:
            self.clear_widgets()
            self.added = False
            #print("resetting")
        j = 1
        if not self.added:
            self.entry = new_obj
            if(self.entry["is_common"]):
                self.myColor = (1,0,1,1)
            else:
                self.myColor = (0,0,1,1)
            
            i = 0
            #print(self.on_press)
            jbox = BoxLayout(orientation = "vertical", size_hint_x = 2)
            ebox = BoxLayout(orientation = "vertical", size_hint_x = 2)  
            button = Button(on_press = self.on_press, text = "暗記カード作成")  
           # print("cat")

            for eachForm in dict(self.entry)["japanese"]:
                self.japanese = eachForm["word"]
                # print(self.japanese)
                self.reading = eachForm["reading"]
                #print(self.reading)
                if self.japanese == None:
                    self.japanese = ""
                if self.reading == None:
                    self.reading = ""
                label = Label(text = self.japanese + "「" + self.reading + "」", font_name = "DroidSansJapanese", color = self.myColor)
                label.bind(size=label.setter('text_size'))    
                jbox.add_widget(label)
                self.english = ""
                if i < len(dict(self.entry)["senses"]):
                    eachEng =  dict(self.entry)["senses"][i]
                    for eachDef in eachEng["english_definitions"]:
                        self.english = self.english + "," + eachDef
                    elabel = Label(text = self.english[1:])
                    elabel.bind(size=elabel.setter('text_size'))    
                    ebox.add_widget(elabel)
                i = i + 1
                j = j + 1
            self.add_widget(jbox)         
            self.add_widget(ebox)
            self.add_widget(button)
            #print("added")
            self.added = True
            self.height = self.minimum_height*(j)
        else:
            print("skipped")
        

    def __init__(self, **kwargs):
        super(SearchResult, self).__init__(**kwargs)   
        if self.entry != None and self.entry != {}:
            self.japanese = dict(self.entry)["japanese"][0]["word"]
            self.reading = dict(self.entry)["japanese"][0]["reading"]
            self.add_widget(Label(text = self.japanese, font_name = "DroidSansJapanese"))
            self.add_widget(Label(text = self.reading, font_name = "DroidSansJapanese"))
            print("****************")
        else:
            print("-")
            self.added = False
        self.orientation = "horizontal"
        self.height = self.minimum_height
        self.size_hint_x = 1
        

Builder.load_string('''
<ResultsView>:
    viewclass: 'SearchResult'
    size_hint_x: 1
    spacing: 40
    space_x: self.size[0]
    RecycleBoxLayout:
        default_size: None, dp(150)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height 
        orientation: 'vertical'
        outline_width: 10
        outline_colour: (0, 1, 0, 0)
<BoxLayout>        
    canvas.before:
        Color:
            rgba: 0, 1, 0, 0.5
        Line:    # --- adds a border --- #
            width: 1
            rectangle: self.x, self.y, self.width, self.height
''')

class ResultsView(RecycleView):
    entry = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.orientation = "vertical"

    def update_data(self, newData):
        self.data = []
        self.refresh_from_data()
        self.data = newData
        self.refresh_from_data()

        #print("cat")

class SearchBoxPage(BoxLayout):
    eachEntry = DictProperty()
    current = ObjectProperty()

    def makeFlashCard(self, entry, instance):
        
        ####LISTENING/SPEAKING
        i = 0
        self.hiragana = []
        self.english = []
        self.rows = []
        #print(entry)
        #######
        for eachForm in dict(entry)["japanese"]:
            if eachForm["reading"] not in self.hiragana:
                if eachForm["reading"] == None:
                    pass
                else:
                    # print(self.japanese)
                    self.hiragana.append(eachForm["reading"])
                    #print(self.reading)
                    
                    self.eng = ""
                    if i < len(dict(entry)["senses"]):
                        eachEng =  dict(entry)["senses"][i]
                        for eachDef in eachEng["english_definitions"]:
                            self.eng = self.eng + "," + eachDef
                        self.english.append(self.eng[1:])
                    else:
                        print("ERROR: Less definitons than entries")
                i = i + 1
            else: 
                jindex = self.japanese.index(eachForm)
                # print(self.japanese)
                #print(self.reading)
                if eachForm["reading"] == None:
                    pass
                else:
                    self.eng = ""
                    if i < len(dict(entry)["senses"]):
                        eachEng =  dict(entry)["senses"][i]
                        for eachDef in eachEng["english_definitions"]:
                            self.eng = self.eng + "," + eachDef
                        self.english[jindex]= "@".join(self.english[jindex]+self.eng[1:])
                    else:
                        print("ERROR: Less definitons than entries")
                i = i + 1       

        with open(LISTENING_SPEAKING_FILENAME,'a', encoding='utf-8') as listFile:
            j = 0
            writer_object = csv.writer(listFile, delimiter="\t")
            
            for eachReading in self.hiragana:
                self.rows.append([None,eachReading, self.english[j],"@","@",1,1])
                j = j + 1

            print(self.rows)
            for eachRow in self.rows:
                writer_object.writerow(eachRow)

            listFile.close()
        ####READING/WRITING
        i = 0
        self.japanese = []
        self.reading = []
        self.english = []
        self.rows = []
        #print(entry)
        #######
        for eachForm in dict(entry)["japanese"]:
            if eachForm["word"] not in self.japanese:
                if eachForm["word"] == None:
                    pass
                else:        
                    self.japanese.append(eachForm["word"])
                    # print(self.japanese)
                    self.reading.append(eachForm["reading"])
                    #print(self.reading)
                    
                    self.eng = ""
                    if i < len(dict(entry)["senses"]):
                        eachEng =  dict(entry)["senses"][i]
                        for eachDef in eachEng["english_definitions"]:
                            self.eng = self.eng + "," + eachDef
                        self.english.append(self.eng[1:])
                    else:
                        print("ERROR: Less definitons than entries")
                i = i + 1
            else: 
                # print(self.japanese)
                #print(self.reading)
                if self.japanese == None:
                    pass
                else:
                    jindex = self.japanese.index(eachForm)

                    self.reading[jindex] = "@".join([self.reading[jindex],eachForm["reading"]])
                    
                    self.eng = ""
                    if i < len(dict(entry)["senses"]):
                        eachEng =  dict(entry)["senses"][i]
                        for eachDef in eachEng["english_definitions"]:
                            self.eng = self.eng + "," + eachDef
                        self.english[jindex]= "@".join(self.english[jindex]+self.eng[1:])
                    else:
                        print("ERROR: Less definitons than entries")
                i = i + 1     

        with open(READING_WRITING_FILENAME, 'a', encoding='utf-8') as readFile:
            j = 0
            writer_object = csv.writer(readFile, delimiter="\t")
            
            for eachKanji in self.japanese:
                self.rows.append([None,eachKanji, self.english[j],"@","@","@",1,self.reading[j],1])
                j = j + 1

            print(self.rows)
            for eachRow in self.rows:
                writer_object.writerow(eachRow)

            readFile.close()

    def search(self, instance):
        print(instance)
        response = Word.request(self.searchBox.text)
        new_data = []
        if response != None:
            answer =  response.dict()["data"]
           
            for eachEntry in answer:
                self.eachEntry = eachEntry
                current = partial(self.makeFlashCard,self.eachEntry)
                new_data.append({"on_press": current,"entry": self.eachEntry, })
              #  print(type(self.eachEntry))
            
        print("cow")
        self.resultsBox.update_data(new_data)
        self.resultsBox.refresh_from_data()

    def build(self):
        self.name = "search_page"
        self.orientation = "vertical"
        self.searchbar = BoxLayout(orientation = "horizontal", size_hint_y = 0.5)
        self.searchBox = TextInput()
        self.resultsBox = ResultsView()
        self.mySearchBtn = Button(text = "検索", on_press = partial(self.search), size_hint_x = 0.2, background_color = (1,0,1,1))
        self.searchbar.add_widget(self.searchBox)
        self.searchbar.add_widget(self.mySearchBtn)
       # self.mybox.add_widget(SearchResult(Word.request("cow").dict()["data"][0])) #test
        self.add_widget(self.searchbar)
        self.add_widget(self.resultsBox)

if __name__ == "__main__":
    myHomePage = Main()
    myHomePage.run()
        