import subprocess
import speech_recognition as sr
import os

def convert_mp4_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command, check=True)

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"


if __name__ == "__main__":
    os.chdir("..")
    video_folder = 

