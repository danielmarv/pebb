from datetime import datetime
import time
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
activationWord = 'computer'  # single word

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

appId = 'J3TQWQ-8LHVY23T8Q'
wolframClient = wolframalpha.Client(appId)

def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

class CarAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

    def turn_on_lights(self):
        self.speak("Turning on lights")

    def lock_doors(self):
        self.speak("Locking doors")

    def play_music(self, song):
        self.speak(f"Playing {song}")

    def adjust_ac_temperature(self, temperature):
        self.speak(f"Adjusting AC temperature to {temperature} degrees Celsius")

    def listen_to_owner(self):
        with sr.Microphone() as source:
            print("Listening to owner...")
            audio_data = self.recognizer.listen(source, timeout=5)
        
        try:
            command = self.recognizer.recognize_google(audio_data).lower()
            print(f"Owner said: {command}")
            self.process_owner_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error connecting to Google API: {e}")

    def process_owner_command(self, command):
        if "lights" in command:
            self.turn_on_lights()
        elif "lock doors" in command:
            self.lock_doors()
        elif "play music" in command:
            song = command.split("play music")[1].strip()
            self.play_music(song)
        elif "adjust temperature" in command:
            temperature = int(command.split("adjust temperature to")[1].strip())
            self.adjust_ac_temperature(temperature)
        else:
            print("Command not recognized.")

    def speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

# Main loop
if __name__ == '__main__':
    car_assistant = CarAssistant()

    speak('This is an AI Developed by Daniel. Please speak your query, and I shall provide what you want.')

    while True:
        print("Listening for a command...")
        query = input("Enter a command: ").lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    car_assistant.speak('Greetings, all.')
                else:
                    query.pop(0)  # Remove say
                    speech = ' '.join(query)
                    car_assistant.speak(speech)

            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                car_assistant.speak('Opening....')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                car_assistant.speak('Querying the universal databank.')
                car_assistant.speak(wikipedia.summary(query, sentences=2))

            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                car_assistant.speak('Computing.')
                try:
                    result = wolframClient.query(query)
                    car_assistant.speak(next(result.results).text)
                except:
                    car_assistant.speak('Unable to compute')

            if query[0] == 'log':
                car_assistant.speak('Ready to write your note')
                new_note = input("Enter your note: ").lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open(f'note_{now}.txt', 'w') as new_file:
                    new_file.write(new_note)
                car_assistant.speak('Note written')

            if query[0] == 'exit':
                car_assistant.speak('Goodbye')
                break
