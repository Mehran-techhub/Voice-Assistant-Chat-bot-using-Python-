import threading
import pyttsx3
import speech_recognition as sr
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from tkinter import simpledialog
import webbrowser
import datetime
import wikipediaapi
import os
import pyautogui
import random
import ctypes
import pyjokes
import psutil
import requests
from googletrans import Translator
import tkinter as tk
import tkinter.font as tkfont
import pyttsx3
import threading

class VisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Assistant")

        # Initialize speech engine and state variables
        self.engine = pyttsx3.init()
        self.speak_lock = threading.Lock()  # Ensure only one thread uses the speech engine
        self.listening = False  # Prevent overlapping commands
        self.is_speaking = False  # Block listening while speaking
        self.language = "en"  # Default language is English

        # GUI Setup
        self.chat_font = tkfont.Font(family="Arial", size=12)
        self.chat_box = tk.Text(root, state="disabled", wrap="word", height=20, width=50, font=self.chat_font)
        self.chat_box.pack(padx=10, pady=10)

        self.run_button = tk.Button(root, text="Run Vision", command=self.run_vision, font=self.chat_font)
        self.run_button.pack(pady=5)

        self.voice_button = tk.Button(root, text="Change Voice", command=self.select_voice, font=self.chat_font)
        self.voice_button.pack(pady=5)

        self.language_button = tk.Button(root, text="Change Language", command=self.select_language, font=self.chat_font)
        self.language_button.pack(pady=5)

        self.clear_chat_button = tk.Button(root, text="Clear Chat", command=self.clear_chat, font=self.chat_font)
        self.clear_chat_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_vision, font=self.chat_font)
        self.exit_button.pack(pady=5)

    def update_chat(self, message):
        """Update chat box with a new message."""
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", f"{message}\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")

    def clear_chat(self):
        """Clear the chat box."""
        self.chat_box.config(state="normal")
        self.chat_box.delete("1.0", "end")  # Remove all text from the chat box
        self.chat_box.config(state="disabled")
        self.update_chat("Vision: Chat has been reset.")  # Optional confirmation message

    def speak(self, audio):
        """Speak a message using pyttsx3 in a thread-safe way."""
        def speak_thread():
            self.is_speaking = True  # Prevent listening while speaking
            with self.speak_lock:  # Ensure only one thread accesses the speech engine
                self.engine.say(audio)
                self.engine.runAndWait()
            self.is_speaking = False  # Allow listening after speaking

        threading.Thread(target=speak_thread, daemon=True).start()

    def select_voice(self):
        """Cycle through available voices."""
        voices = self.engine.getProperty("voices")
        current_voice = self.engine.getProperty("voice")

        # Find the current voice and move to the next one
        for i, voice in enumerate(voices):
            if voice.id == current_voice:
                next_voice = voices[(i + 1) % len(voices)]  # Cycle to the next voice
                self.engine.setProperty("voice", next_voice.id)
                self.speak("Voice has been changed.")
                self.update_chat("Vision: Voice has been changed.")
                return

        self.speak("No alternate voices found.")
        self.update_chat("Vision: No alternate voices found.")

    def select_language(self):
        """Prompt user to select a language."""
        languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr"
        }

        self.speak("Select a language. I support English, Spanish, and French.")
        self.update_chat("Vision: Select a language.")
        
        choice = simpledialog.askstring("Language", "Enter 'en' for English, 'es' for Spanish, or 'fr' for French:")
        if choice in languages.values():
            self.language = choice
            self.engine.setProperty("voice", choice)
            self.speak(f"Language set to {choice.upper()}.")
            self.update_chat(f"Vision: Language set to {choice.upper()}.")
        else:
            self.update_chat("Vision: Invalid or unsupported language. Defaulting to English.")
            self.speak("Invalid or unsupported language. Defaulting to English.")
            self.language = "en"
            
    def get_answer_from_wikipedia(self, question):
        """Retrieve an answer from Wikipedia."""
        user_agent = "VisionBot/1.0"
        wiki_lang = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

        search_query = question.split('about', 1)[-1].strip()
        page = wiki_lang.page(search_query)

        if page.exists():
            return page.summary.split('\n')[0]
        else:
            return "Sorry, I couldn't find any information on that topic in Wikipedia."

    def open_website(self, command):
        """Open a website based on user command."""
        websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "chat gpt": "https://chat.openai.com",
            "stack overflow": "https://stackoverflow.com"
        }

        for site in websites:
            if site in command.lower():
                webbrowser.open(websites[site])
                return f"Opening {site.capitalize()}..."
        return "Sorry, I can't find the website you mentioned."

    def tell_time_and_date(self):
        """Tell the current time and date."""
        now = datetime.datetime.now()
        current_time = now.strftime('%I:%M %p')
        current_date = now.strftime('%A, %D %B %Y')
        return f"The current time is {current_time}. Today is {current_date}."

    def take_screenshot(self):
        screenshot_path = os.path.join(os.path.expanduser("~"), "C:\\Users\\HP\\OneDrive\\Pictures\\Screenshots", "screenshot.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        return f"Screenshot saved at {screenshot_path}"
    
    
    def change_desktop_background(self):
        try:
            # Ask the user to select a folder
            folder_path = filedialog.askdirectory(title="Select Folder Containing Wallpapers")
            
            if folder_path:
                wallpapers = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png"))]

                if wallpapers:
                    # Pick a random wallpaper
                    wallpaper = random.choice(wallpapers)
                    wallpaper_path = os.path.join(folder_path, wallpaper)
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
                    return f"Desktop background changed successfully to {wallpaper}."
                else:
                    return "No valid image files found in the specified folder."
            else:
                return "No folder selected."
        except Exception as e:
            return f"Error changing background: {e}"
        
        
    def tell_a_joke(self):
        return pyjokes.get_joke()
    
    def open_camera(self):
        """Open the camera."""
        try:
            os.system("start microsoft.windows.camera:")
            return "Camera opened successfully."
        except Exception as e:
            return f"Error opening camera: {e}"
        
        
    def control_system(self, action):
        """Perform system control actions."""
        actions = {
            "lock": "shutdown /l",
            "shutdown": "shutdown /s /f /t 0",
            "restart": "shutdown /r /f /t 0"
        }
        if action in actions:
            os.system(actions[action])
            return f"System {action} initiated."
        else:
            return "Invalid action."
        
        
    def get_system_usage(self):
        battery = psutil.sensors_battery()
        battery_percentage = battery.percent
        battery_status = battery.power_plugged
        battery_info = f"Battery percentage: {battery_percentage}%."
        if battery_status:
            battery_info += " Charging."
        else:
            battery_info += " Not charging."

        cpu_usage = psutil.cpu_percent(interval=1)
        return f"{battery_info} CPU usage: {cpu_usage}%."
        
        
    def get_weather(self, city):
        """Fetch weather for a city."""
        api_key = "9ee7dee3ec70a09120434817b3643b7e"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]  
                wind_speed = data["wind"]["speed"]
                return f"The current weather in {city} is {weather} with a temperature of {temp}°C, humidity of {humidity}%, and wind speed of {wind_speed} m/s."
            else:
                return "City not found or unable to retrieve weather data."
        except Exception as e:
            return f"Error retrieving weather data: {e}"
        
    def take_command(self):
        """Capture audio command from the user."""
        if self.is_speaking:  # Don't listen while speaking
            return "None"

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            self.update_chat("Vision: Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.update_chat("Vision: Recognizing...")
                if self.language != "en":
                    query = recognizer.recognize_google(audio, language=self.language)
                else:
                    query = recognizer.recognize_google(audio)
                self.update_chat(f"You: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                self.update_chat("Vision: I didn't hear anything. Please speak again.")
                self.speak("I didn't hear anything. Could you repeat?")
                return "None"
            except sr.UnknownValueError:
                self.update_chat("Vision: Sorry, I couldn't understand that. Please repeat.")
                self.speak("Sorry, I couldn't understand that. Could you repeat?")
                return "None"
            except sr.RequestError as e:
                self.update_chat("Vision: There was an issue with the speech recognition service.")
                self.speak("There was an issue with the speech recognition service. Please try again later.")
                return "None"

    def process_command(self, query):
        """Process the user's command."""
        if "hello" in query:
            self.update_chat("Vision: Hello! How can I assist you?")
            self.speak("Hello! How can I assist you?")
        elif "who am i" in query:
            self.update_chat("Vision: If you are talking, then you are human.")
            self.speak("If you are talking, then you are human.")
        elif "what is your name" in query:
            self.update_chat("Vision: I'm Vision, your smart assistant. What can I do for you today?")
            self.speak("I'm Vision, your smart assistant. What can I do for you today?")
        elif "who are you" in query:
            self.update_chat("Vision: I am an assistant who can answer your questions.")
            self.speak("I am an assistant who can answer your questions.")
        elif "how are you" in query:
            self.update_chat("Vision: I'm fine. Thank you for asking me. What about you?")
            self.speak("I'm fine. Thank you for asking me. What about you?")
        elif "i am good" in query:
            self.update_chat("Vision: I'm happy to hear that. Let me know how I can help you!")
            self.speak("I'm happy to hear that. Let me know how I can help you!")
        elif "time" in query or "date" in query:
            response = self.tell_time_and_date()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "wikipedia" in query or "about" in query:
            response = self.get_answer_from_wikipedia(query)
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "screenshot" in query:
            response = self.take_screenshot()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "change background" in query:
            response = self.change_desktop_background()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "joke" in query:
            response = self.tell_a_joke()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "camera" in query:
            response = self.open_camera()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "shutdown" in query:
            response = self.control_system("shutdown")
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "restart" in query:
            response = self.control_system("restart")
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "lock" in query:
            response = self.control_system("lock")
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "battery" in query or "cpu" in query:
            response = self.get_system_usage()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "weather" in query:
            city = query.replace("weather", "").strip()
            response = self.get_weather(city)
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "open" in query:
            response = self.open_website(query)
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "language" in query:
            self.select_language()
        elif "exit" in query or "quit" in query or "stop" in query:
            self.update_chat("Vision: Goodbye!")
            self.speak("Goodbye! Exiting now.")
            self.exit_vision()
        else:
            self.update_chat(f"Vision: I'm not sure how to handle '{query}'.")
            self.speak(f"I'm not sure how to handle '{query}'.")

    def listen_loop(self):
        """Continuously listen for commands."""
        while self.listening:
            query = self.take_command()
            if query in ["exit", "quit", "stop"]:
                self.update_chat("Vision: Exiting listening mode.")
                self.speak("Exiting listening mode.")
                break
            if query != "None":
                self.process_command(query)

    def run_vision(self):
        """Start the assistant and begin listening."""
        if not self.listening:
            self.listening = True
            self.run_button.pack_forget()  # Hide the RUN button when assistant starts
            self.update_chat("Vision: Online and listening.")
            self.speak("Vision is now online.")
            threading.Thread(target=self.listen_loop, daemon=True).start()


    def exit_vision(self):
        """Exit the application."""
        self.listening = False
        self.update_chat("Vision: Exiting...")
        self.speak("Goodbye! Exiting now.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisionApp(root)
    root.mainloop()

