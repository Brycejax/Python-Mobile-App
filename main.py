#-----------------------------------------------
# Developer----- Bryce Martin
# Description---- This program will use Kivy
#                 to create a simple mobile app
#                 for the experience.
#-----------------------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]["password"] == pword:
            self.manager.current = "login_screen_success"
        else:
            #accessing a label
            self.ids.login_wrong.text = "Wrong Username or Password"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
            #add to the dictonary
        users[uname] = {'username' : uname, 'password' : pword,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", "w") as file:
            json.dump(users, file)

        #lets redirect the user
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try a different feeling"

class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()