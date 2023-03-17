from kivy.app import App
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config

from functools import partial

from dict_android import *
from listening_android import *
from speaking_android import *

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: '辞書'
            on_press: root.manager.current = 'search_page'
            font_name: "DroidSansJapanese"

        Button:
            text: '暗記カード'
            on_press: root.manager.current = 'learn_page'
            font_name: "DroidSansJapanese"


<SearchPage>:
    name: "search_page"

<LearningMainPage>
    name: "learn_page"
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "聞き取り"
            on_press: root.manager.current = "listening_page"            
            font_name: "DroidSansJapanese"
        Button:
            text: "話し出す"
            on_press: root.manager.current = "speaking_page"
            font_name: "DroidSansJapanese"

<ListeningPage>
    name: "listening_page"

<SpeakingPage>
    name: "speaking_page"    

""")

# Declare both screens
class MenuScreen(Screen):
    pass

class LearningMainPage(Screen):
    pass

class ListeningPage(Screen):
    def on_pre_enter(self, *args):
       lbp = ListeningBox()
       lbp.build()
       self.add_widget(lbp)

class SpeakingPage(Screen):
    def on_pre_enter(self, *args):
       sbp = SpeakingBox()
       sbp.build()
       self.add_widget(sbp)
       

class SearchPage(Screen):
    def on_pre_enter(self, *args):
       sbp = SearchBoxPage()
       sbp.build()
       self.add_widget(sbp)
    
class TestApp(App):

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SearchPage(name='search_page'))        
        self.sm.add_widget(LearningMainPage(name='learn_page'))
        self.sm.add_widget(ListeningPage(name='listening_page'))
        self.sm.add_widget(SpeakingPage(name='speaking_page'))
        return self.sm
    
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key in [27,1001]:
            self.sm.current = "menu"
            return True


if __name__ == '__main__':
    TestApp().run()