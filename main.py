import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
from google import genai
from gtts import gTTS
import pygame
import os

# -----------------------------
# Initialization
# -----------------------------

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize pygame only once
pygame.mixer.init()

# Gemini client
client = genai.Client(
    api_key="YOUR API KEY"
)


# -----------------------------
# Text-to-Speech
# -----------------------------

def speak(text):
    print("Jarvis:", text)

    try:
        tts = gTTS(text=text, lang="en")
        tts.save("temp.mp3")

        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()

        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")

    except Exception as e:
        print("TTS Error:", e)

        # Fallback to pyttsx3
        engine.say(text)
        engine.runAndWait()


# -----------------------------
# Gemini AI
# -----------------------------

def genaiprocess(command):

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=command
        )

        return interaction.output_text

    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, I could not connect to Gemini."


# -----------------------------
# Process Commands
# -----------------------------

def processcommand(c):

    command = c.lower().strip()

    if "open google" in command:

        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in command:

        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:

        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:

        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play "):

        song = command.replace("play ", "", 1).strip()

        if song in musiclibrary.music:

            link = musiclibrary.music[song]

            webbrowser.open(link)

            speak(f"Playing {song}")

        else:

            speak(
                f"I could not find {song} in your music library."
            )

    else:

        output = genaiprocess(command)

        speak(output)


# -----------------------------
# Main Program
# -----------------------------

if __name__ == "__main__":

    speak("Initializing Jarvis")

    while True:

        try:

            # -----------------------------
            # Listen for wake word
            # -----------------------------

            with sr.Microphone() as source:

                print("Listening...")

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            print("Recognizing...")

            word = recognizer.recognize_google(audio)

            print("You said:", word)

            # -----------------------------
            # Check wake word
            # -----------------------------

            if word.lower().strip() == "jarvis":

                speak("Yes?")

                # -----------------------------
                # Listen for command
                # -----------------------------

                with sr.Microphone() as source:

                    print("Jarvis Active...")

                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=10
                    )

                command = recognizer.recognize_google(audio)

                print("Command:", command)

                processcommand(command)

        except sr.WaitTimeoutError:

            print("Listening timed out.")

        except sr.UnknownValueError:

            print("Could not understand audio.")

        except sr.RequestError as e:

            print("Speech recognition service error:", e)

        except Exception as e:

            print("Error:", e)
