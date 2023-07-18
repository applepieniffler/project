# pip install kivy
# pip install schedule
# pip install pushbullet.py
# pip install plyer

import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.core.window import Window
#from pushbullet import Pushbullet
import schedule
import threading
import subprocess


class Daily_Dose(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.image = Image(source='dintaifung.png')  # Set the default image
        layout.add_widget(self.image)

        self.label = Label(text="Welcome! This app is designed to send daily motivational quotes at a specified time of your choice. Please choose your preferred time in the dropdown box (24-hour format; 5-minute intervals only) below:")
        layout.add_widget(self.label)

        self.name_input = TextInput(multiline=False, hint_text="Please input your name here.")
        layout.add_widget(self.name_input)

        self.time_spinner = Spinner(
            text='00:00',
            values=[f'{h:02d}:{m:02d}' for h in range(24) for m in range(0, 60, 5)],
            size_hint=(None, None),
            size=(1000, 400),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.time_spinner)

        self.button = Button(text="Submit", on_press=self.on_submit)
        layout.add_widget(self.button)

        return layout

    #def send_notification(self, name):
        #access_token = "o.ipNKhKRfaGDWccCZJ1GgaxTkGY6curYk"
        #pb = Pushbullet(access_token)
       # message = "This is your daily motivational quote!"  # Replace with actual quote
       # push = pb.push_note("Motivational Quote of the Day", message)
       # print("Notification sent to", name)
       # self.label.text = "Quote sent"  # Update label text
        
    def send_notification(self, name):
        message = "This is your daily motivational quote!"  # REPLACE WITH ACTUAL RANDOMIZED QUOTE
        script = f'display notification "{message}" with title "Motivational Quote of the Day" sound name "Crystal"'      
        duration_script = f'delay 20'
        combined_script = f'{script}\n{duration_script}'
        subprocess.run(['osascript', '-e', script])
        print("Notification sent to", name)
        self.label.text = "Quote sent. Have an amazing day " + name + ". You deserve it!"
        self.image.source = 'bowling.png'

    def schedule_jobs(self, name, selected_time):
        hour, minute = map(int, selected_time.split(':'))
        schedule.every().day.at(f'{hour:02d}:{minute:02d}').do(self.send_notification, name=name)

        while True:
            schedule.run_pending()

    def on_submit(self, instance):
        name = self.name_input.text
        selected_time = self.time_spinner.text

        self.label.text = f"Welcome, {name}!\nThis is your chosen notification time: {selected_time}"
        self.name_input.parent.remove_widget(self.name_input)
        self.time_spinner.parent.remove_widget(self.time_spinner)
        self.button.parent.remove_widget(self.button)
        
        self.image.source = 'inom.png'

        # Schedule the jobs in a background thread
        threading.Thread(target=self.schedule_jobs, args=(name, selected_time), daemon=True).start()

if __name__ == '__main__':
    Daily_Dose().run()