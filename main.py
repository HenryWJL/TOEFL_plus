from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput


def str_insert(str_origin, pos, str_add):
        str_list = list(str_origin)    
        str_list.insert(pos, str_add) 
        str_out = ''.join(str_list)    
        return  str_out


def text_modify(text):
    new_text = []
    for line in text:
        if len(line) > 29:
            added_newline = int(len(line) / 29)
            for idx in range(1, added_newline + 1):
                line = str_insert(line, idx * 30 - 1, '\n')
                
        new_text.append(line)    
    return new_text


class WordsScreen(Screen):
    current_idx = NumericProperty(0)
    wordsList = []
    with open('word.txt', 'r') as f:
        wordsList = f.readlines()
    
    
    def set_current_idx(self, day):
        self.current_idx = (int(day) - 1) * 50
    
    
    def previous_word(self):
        if self.current_idx >= 1:
            self.current_idx -= 1
    
    
    def next_word(self):
        if self.current_idx < len(self.wordsList) - 1:
            self.current_idx += 1
        

class TranslationScreen(Screen):
    current_idx = NumericProperty(0)
    translationList = []
    with open('translation.txt', 'r') as f:
        translationList = f.readlines()
    translationList = text_modify(translationList)
    
    
    def set_current_idx(self, day):
        self.current_idx = (int(day) - 1) * 50
    
    
    def previous_word(self):
        if self.current_idx >= 1:
            self.current_idx -= 1
    
    
    def next_word(self):
        if self.current_idx < len(self.translationList) - 1:
            self.current_idx += 1
            

class HomeScreen(Screen):
    pass
        
            
class ScreensManager(ScreenManager):
    
    
    def on_touch_up(self, touch):
        home_screen = self.get_screen('home')
        words_screen = self.get_screen('words')
        translation_screen = self.get_screen('translation')
        if touch.y < self.height / 3 and self.current == 'home':
            self.current = 'words'
            day = home_screen.day.text
            if day == '' or int(day) > 68 or int(day) < 0:
                day = '1'
            words_screen.set_current_idx(day)
            translation_screen.set_current_idx(day)
            
        elif touch.y > 2 * self.height / 3 and self.current == 'words':
            self.current = 'home'
            home_screen.day.do_undo()
        
        elif touch.y < self.height / 3 and self.current == 'words':
            self.current = 'translation'
            
        elif touch.y > 2 * self.height / 3 and self.current == 'translation':
            self.current = 'words'
            
        elif touch.x < self.width / 3 and self.current == 'words':
            words_screen.previous_word()
            translation_screen.previous_word()
            
        elif touch.x > 2 * self.width / 3 and self.current == 'words':
            words_screen.next_word()
            translation_screen.next_word()
        

class VocabularyApp(App):
   
    
    def build(self):
        return ScreensManager()
    
    
if __name__ == '__main__':
    VocabularyApp().run()

