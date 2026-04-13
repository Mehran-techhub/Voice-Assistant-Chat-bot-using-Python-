# Voice-Assistant-Chat-bot-using-Python-

DOCUMENTATION OF VOICE ASSISTANT:________________________________________
Voice Assistant Application: Vision
Vision is a voice-activated assistant built using Python. It offers a range of functionalities to make daily tasks easier, including answering questions, performing system-level operations, and providing entertainment. Here's a complete explanation of its features and how it works:
________________________________________
Key Features of Vision
1.	Voice Interaction:
o	Vision interacts with the user through spoken and written responses.
o	Users can issue commands via their microphone, and the assistant responds both verbally and in a text chatbox.
2.	Information Retrieval:
o	Time and Date: It tells the current time and date.
o	Wikipedia Integration: Answers questions using Wikipedia's summary data.
o	Weather Information: Retrieves real-time weather information for a specified city.
3.	System Management:
o	Battery and CPU Usage: Displays the current battery percentage, charging status, and CPU usage.
o	Desktop Background Change: Allows the user to select a folder of wallpapers, randomly sets one as the background.
o	System Actions: Can lock, restart, or shut down the computer based on voice commands.
4.	Utility Tools:
o	Screenshot Capture: Takes a screenshot and saves it to a predefined location.
o	Open Applications/Websites: Opens websites like Google, YouTube, GitHub, etc., when requested.
o	Camera Access: Opens the device’s camera.
5.	Entertainment:
o	Jokes: Tells a random joke.
o	Casual Chat: Responds to friendly or casual queries, such as "Who are you?" or "Will you marry me?"
6.	Customization:
o	Voice Selection: Users can switch between male and female voices for the assistant.
________________________________________
How Vision Works
Modules and Libraries:
1.	pyttsx3: Handles text-to-speech conversion, allowing the assistant to speak to the user.
2.	speech_recognition: Captures and processes user voice input, converting it to text for further processing.
3.	tkinter: Creates a graphical user interface (GUI), including a chat box and control buttons.
4.	webbrowser: Opens websites in the default browser.
5.	datetime: Retrieves the current time and date.
6.	wikipediaapi: Queries Wikipedia for summaries of requested topics.
7.	pyautogui: Takes and saves screenshots.
8.	ctypes: Changes the desktop wallpaper.
9.	psutil: Monitors system performance (battery and CPU usage).
10.	pyjokes: Fetches random jokes for entertainment.
11.	requests: Fetches real-time weather information from OpenWeatherMap API.
12.	threading: Allows simultaneous execution of listening, speaking, and GUI updates without blocking the interface.
13.	os: Provides system-level functionality, like locking or restarting the system.
________________________________________
User Interaction Flow
1.	Launching the Application:
o	The app initializes with a GUI containing a chat box and buttons for running Vision, changing the voice, clearing the chat, and exiting the program.
2.	Voice Commands:
o	Once "Run Vision" is clicked, the assistant goes into "listening mode."
o	The user speaks commands, which are transcribed, processed, and acted upon by the assistant.
3.	Response and Feedback:
o	The assistant responds to commands by updating the chat box and speaking the output.
o	If an action is performed (e.g., taking a screenshot or opening a website), the result is acknowledged in the chat box.
________________________________________
What You Can Do With Vision
Command/Query	Functionality
"What is the time/date?"	Tells the current time and date.
"What is [topic] on Wikipedia?"	Retrieves a brief summary of the topic from Wikipedia.
"What's the weather in [city]?"	Provides real-time weather information, including temperature, humidity, and wind speed.
"Take a screenshot"	Captures a screenshot and saves it to a predefined location.
"Change background"	Allows you to select a folder of wallpapers and randomly changes the desktop background.
"Tell me a joke"	Shares a random joke from the pyjokes library.
"Open Google/YouTube/etc."	Opens popular websites like Google, YouTube, or Instagram in the default browser.
"How's the battery/CPU?"	Displays the current battery percentage, charging status, and CPU usage.
"Lock the system"	Locks the computer screen.
"Shutdown the system"	Shuts down the computer immediately.
"Restart the system"	Restarts the computer immediately.
"Open the camera"	Opens the device's camera application.
"Who are you?"	Engages in friendly conversation, introducing itself as Vision.
"Change the voice"	Prompts the user to switch between male and female voices.
________________________________________
Benefits of Using Vision
1.	Efficiency: Automates daily tasks like checking the weather, retrieving information, or managing the system.
2.	Ease of Use: The voice interface makes it accessible to users with minimal technical knowledge.
3.	Customization: Options for voice changes and desktop background personalization.
4.	Entertainment: Keeps the user entertained with jokes and casual conversation.
5.	Integration: Combines multiple tools like Wikipedia, OpenWeatherMap, and system utilities into one assistant.
________________________________________
Future Improvements (Potential Enhancements)
•	Language Support: Extend recognition and response to multiple languages.
•	Smart Context Handling: Implement memory to retain the context of previous queries for more dynamic interaction.
•	Improved Error Handling: Handle API failures or misrecognition gracefully.
•	Machine Learning: Use AI models for more natural conversations and predictive capabilities.
________________________________________
This voice assistant provides an accessible, multi-functional solution for managing tasks, retrieving information, and entertainment—all from one simple interface.

