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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

class VisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Assistant")

        # Initialize speech engine and state variables
        self.engine = pyttsx3.init()
        self.speak_lock = threading.Lock()  # Ensure only one thread uses the speech engine
        self.listening = False  # Prevent overlapping commands
        self.is_speaking = False  # Block listening while speaking

        # GUI Setup
        self.chat_font = tkfont.Font(family="Arial", size=12)
        self.chat_box = tk.Text(root, state="disabled", wrap="word", height=20, width=50, font=self.chat_font)
        self.chat_box.pack(padx=10, pady=10)
        

        self.run_button = tk.Button(root, text="Run Vision", command=self.run_vision, font=self.chat_font)
        self.run_button.pack(pady=5)

        self.voice_button = tk.Button(root, text="Change Voice", command=self.select_voice, font=self.chat_font)
        self.voice_button.pack(pady=5)
        
        self.clear_chat_button = tk.Button(root, text="Clear Chat", command=self.clear_chat, font=self.chat_font)
        self.clear_chat_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_vision, font=self.chat_font)
        self.exit_button.pack(pady=5)
        
        # This is for taking a quiz
        self.root = root
        self.root.title("Vision Assistant")
        self.quiz_questions = {
            "What is 5 + 3?": "8",
            "What is the capital of France?": "Paris",
            "Who wrote 'Hamlet'?": "William Shakespeare"
        }
        self.current_question_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.incorrect_questions = []   
        
        
        
    def open_quiz_window(self):
        """Open a new Tkinter window for the quiz."""
        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Take Quiz")
        
        self.quiz_window.geometry("600x400")

        # Create and display question
        self.question_label = tk.Label(self.quiz_window, text=self.get_current_question())
        self.question_label.pack(pady=20)

        # Create input field for user answer
        self.answer_entry = tk.Entry(self.quiz_window, width=40)
        self.answer_entry.pack(pady=10)

        # Create 'Send Answer' button
        self.send_button = tk.Button(self.quiz_window, text="Send Answer", command=self.check_answer)
        self.send_button.pack(pady=20)
        
        
    def get_current_question(self):
        """Get the current question based on the current question index."""
        if self.current_question_index < len(self.quiz_questions):
            return list(self.quiz_questions.keys())[self.current_question_index]
        else:
            return "Quiz Finished!"
        
        
    def check_answer(self):
        """Check the user's answer and give feedback."""
        user_answer = self.answer_entry.get().strip()
        correct_answer = list(self.quiz_questions.values())[self.current_question_index]

        if user_answer.lower() == correct_answer.lower():
            self.correct_answers += 1
            feedback = "Correct!"
        else:
            self.wrong_answers += 1
            feedback = f"Incorrect. The correct answer is: {correct_answer}"
            self.incorrect_questions.append((list(self.quiz_questions.keys())[self.current_question_index], correct_answer))

        self.current_question_index += 1
        self.update_quiz_window(feedback)
        
        
    def update_quiz_window(self, feedback):
        """Update the quiz window with feedback and next question."""
        # Provide feedback on the answer
        feedback_label = tk.Label(self.quiz_window, text=feedback)
        feedback_label.pack()

        # If there are more questions, show the next one, otherwise show the score
        if self.current_question_index < len(self.quiz_questions):
            self.question_label.config(text=self.get_current_question())
            self.answer_entry.delete(0, tk.END)
        else:
            self.show_score()
            
            
    def show_score(self):
        """Show the final score and the incorrect answers with correct answers."""
        score_message = f"Quiz Finished!\nCorrect Answers: {self.correct_answers}\nWrong Answers: {self.wrong_answers}"
        self.quiz_window.destroy()

        # Show a message with the results
        score_window = tk.Toplevel(self.root)
        score_window.title("Quiz Results")
        
        score_label = tk.Label(score_window, text=score_message)
        score_label.pack()

        if self.incorrect_questions:
            incorrect_label = tk.Label(score_window, text="Incorrect Answers (with correct ones):")
            incorrect_label.pack()

            for question, correct_answer in self.incorrect_questions:
                incorrect_feedback = f"{question} - Correct answer: {correct_answer}"
                incorrect_answer_label = tk.Label(score_window, text=incorrect_feedback)
                incorrect_answer_label.pack()

        # Optionally, add a button to close the score window
        close_button = tk.Button(score_window, text="Close", command=score_window.destroy)
        close_button.pack()
        
        
        
        
        
        
    
    def open_email_input_window(self):
        """Open a new Tkinter window with email input fields."""
        self.email_window = tk.Toplevel(self.root)
        self.email_window.title("Send Email")

        self.email_window.geometry("500x400")

        # Create input fields for email details
        self.recipient_label = tk.Label(self.email_window, text="Recipient Email:")
        self.recipient_label.pack(padx=15, pady=10)

        self.recipient_entry = tk.Entry(self.email_window, width=40)
        self.recipient_entry.pack(padx=15, pady=10)

        self.subject_label = tk.Label(self.email_window, text="Subject:")
        self.subject_label.pack(padx=15, pady=10)

        self.subject_entry = tk.Entry(self.email_window, width=40)
        self.subject_entry.pack(padx=15, pady=10)

        self.body_label = tk.Label(self.email_window, text="Body:")
        self.body_label.pack(padx=15, pady=10)

        self.body_entry = tk.Entry(self.email_window, width=40, height=8)
        self.body_entry.pack(padx=15, pady=10)

        self.send_button = tk.Button(self.email_window, text="Send Email", command=self.on_send_button_click)
        self.send_button.pack(pady=15)
    
    
    
    def on_send_button_click(self):
        """Handles the click event of the Send button."""
        sender_email = "your_email@gmail.com"  # Replace with your email
        sender_password = "Qwert@678"  # Replace with your email app password
        recipient_email = self.recipient_entry.get()
        subject = self.subject_entry.get()
        body = self.body_entry.get()

        if recipient_email and subject and body:
            # Call the send_email function to send the email
            self.send_email(sender_email, sender_password, recipient_email, subject, body)
        else:
            self.update_chat("Vision: Please fill in all the fields.")
            self.speak("Please fill in all the fields.")

    def send_email(self, sender_email, sender_password, recipient_email, subject, body):
        # Use the previous email-sending function here
        try:
            # Set up the server and log in
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()

            # Notify the user
            self.update_chat("Vision: Email sent successfully.")
            self.speak("Email sent successfully.")
        
        except Exception as e:
            self.update_chat(f"Vision: Error sending email: {e}")
            self.speak(f"Error sending email: {e}")
    
    
    
      

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

    def set_voice(self, voice_type):
        """Set the voice type for the assistant."""
        voices = self.engine.getProperty('voices')
        if voice_type == 0:
            self.engine.setProperty('voice', voices[1].id)
            self.speak("Voice set to female.")
            self.update_chat("Vision: Voice set to female.")
        elif voice_type == 1:
            self.engine.setProperty('voice', voices[0].id)
            self.speak("Voice set to male.")
            self.update_chat("Vision: Voice set to male.")
        else:
            self.speak("Invalid choice. Default voice retained.")
            self.update_chat("Vision: Invalid choice. Default voice retained.")

    def select_voice(self):
        """Prompt user for voice preference."""
        self.speak("Enter 0 for female voice or 1 for male voice.")
        self.update_chat("Vision: Enter 0 for female voice or 1 for male voice.")
        try:
            choice = int(input("Your choice: "))
            self.set_voice(choice)
        except ValueError:
            self.speak("Invalid input. Please enter 0 or 1.")
            self.update_chat("Vision: Invalid input. Please enter 0 or 1.")

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

    
    def play_music(self): 
        music_path = "D:\\Theory of Programming Languages Book\\Islamic Music"
    
        try:
            music_files = [f for f in os.listdir(music_path)]
            if music_files:
                music_files.sort()  
                music_file = os.path.join(music_path, music_files[0])
                os.startfile(music_file)
                return "Playing music from your collection."
            else:
                return "No music files found in the directory."
        except Exception as e:
            return f"Failed to play music: {e}"
    
    
    def send_whatsapp_message(self):
        """Send a WhatsApp message using Selenium."""
        # Ask for phone number and message through GUI
        phone_number = simpledialog.askstring("WhatsApp", "Enter the recipient's phone number (including country code):")
        if phone_number:
            message = simpledialog.askstring("WhatsApp", "Enter the message you want to send:")
            if message:
                # Use ChromeDriver and open WhatsApp Web
                driver = webdriver.Chrome(executable_path="path_to_chromedriver")  # Provide path to chromedriver
                driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")

                self.speak("opening whatsapp web")
                print("Opening WhatsApp Web...")

                # Wait for the page to load
                time.sleep(15)

                # Wait until QR code is scanned or the user is logged in
                self.speak("please scan the qr code if prompted")
                print("Please scan the QR code if prompted.")

                # Wait for the chat to load (we can use WebDriverWait for better synchronization)
                time.sleep(5)

                try:
                    # Locate the "Send" button and click it
                    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                    send_button.click()
                    self.speak("message sent successfully")
                    print("Message sent successfully!")

                except Exception as e:
                    self.speak("error sending message")
                    print(f"Error sending message: {e}")

                # Allow some time for the message to send before closing
                time.sleep(5)

                driver.quit()

            else:
                self.speak("no message entered")
                print("No message entered.")
        else:
            self.speak("no phone number entered")
            print("No phone number entered.")
    
    

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
     
    def clear_recycle_bin(self):
        # This will run a system command to clear the recycle bin
        try:
            if os.name == 'nt':  # Check if the system is Windows
                # Run the Windows API command to clear the recycle bin
                ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
                self.speak("recycle bin cleared successfully")
                print("Recycle bin cleared successfully.")
            else:
                print("This function is only supported on Windows.")
        except Exception as e:
            print(f"Error: {e}")
     
        
        
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
        
    
    
    
    
   
    def process_command(self, query):
        """Process the user's command."""
        if "hello" in query:
            self.update_chat("Vision: Hello! How can I assist you?")
            self.speak("Hello! How can I assist you?")
        elif "who i am" in query:
            self.update_chat("Vision: If you are talking then you are human.")
            self.speak("if you are talking then you are human")
        elif "what is your name" in query:
            self.update_chat("Vision: I'm Vision, your smart assistant. What can I do for you today?")
            self.speak("i am vision your smart assistant what can i do for you today")
        elif "who are you" in query:
            self.update_chat("Vision: I am assistant who can answer your questions.")
            self.speak("i am assistant who can answer your questions")
        elif "how are you" in query:
            self.update_chat("Vision: I'm fine. Thank you for asking me how I am. What about you?")
            self.speak("i am fine  thank you for asking me how i am  what about you")
        elif "i am good" in query:
            self.update_chat("Vision: I'm happy to hear that. Let me know how I can help you!")
            self.speak("i am happy to hear that  Let me know how i can help you")
        elif "will you marry me" in query:
            self.update_chat("Vision: I appreciate the sentiment, but I'm not quite ready for that step.")
            self.speak("i appreciate the sentiment but i am not quite ready for that step")
        elif "can we be good friends" in query:
            self.update_chat("Vision: Sure thing! Friends are here to support each other, and that's what I'm here for.")
            self.speak("sure thing friends are here to support each other and that is what i am here for")
        elif "clear recycle bin" in query:
            self.clear_recycle_bin()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "send whatsapp message" in query:  # one
            self.send_whatsapp_message()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "take quiz" in query:  # two
            self.open_quiz_window()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "send email" in query:  # three
            self.open_email_input_window()
            self.update_chat(f"Vision: {response}")
            self.speak(response)
        elif "play music" in query:
            response = self.play_music() 
            self.update_chat(f"Vision: {response}")
            self.speak(response)
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
        elif "exit" in query or "quit" in query or "stop" in query:
            self.update_chat("Vision: Goodbye!")
            self.speak("Goodbye! Exiting now.")
            self.exit_vision()
        else:
            self.update_chat(f"Vision: I'm not sure how to handle '{query}'.")
            self.speak(f"I'm not sure how to handle '{query}'.")

    
    
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
                query = recognizer.recognize_google(audio, language='en-in')
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
        """Start the assistant."""
        if not self.listening:
            self.listening = True
            self.run_button.pack_forget()  # Hide the RUN button
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
