#install kivy
#install pusher_push_notifications

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from pusher_push_notifications import PushNotifications

class Daily_Dose(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Welcome! This app is designed to send daily motivational quotes at a specified time of your choice. Please choose your preferred time in the dropdown box (24 hour format; 5 minute intervals only) below:")
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

    def on_submit(self, instance):
        name = self.name_input.text
        selected_time = self.time_spinner.text

        self.label.text = f"Welcome, {name}!\nNotification time: {selected_time}"
        self.name_input.parent.remove_widget(self.name_input)
        self.time_spinner.parent.remove_widget(self.time_spinner)
        self.button.parent.remove_widget(self.button)

        # Initialize Pusher Push Notifications with your credentials
        beams_client = PushNotifications(
            instance_id='b2af0741-505b-460b-a2a5-fe4063a97f16',
            secret_key='D9535666AA6A359DD933354AB6CF327297C4AC037A27F9BEE9719B1DF06CDB89',
        )

        # Send the push notification at the selected time
        response = beams_client.publish_to_interests(
            interests=['motivation'],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': {
                            'title': 'Motivational Quote',
                            'body': 'This is your daily motivational quote!',
                        },
                    },
                },
            },
        )

        # Handle the response
        if 'status_code' in response and response['status_code'] == 200:
            print("Notification sent successfully!")
        else:
            print("Failed to send notification:", response)

if __name__ == '__main__':
    Daily_Dose().run()


