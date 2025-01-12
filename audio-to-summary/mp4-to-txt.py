import subprocess
import speech_recognition as sr
import os
import tempfile

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

def mp4_to_txt(input_file, output_file):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        temp_wav_file.close()
        convert_mp4_to_wav(input_file, temp_wav_file.name)
        text = speech_to_text(temp_wav_file.name)
        os.remove(temp_wav_file.name)
        
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w') as f:
            f.write(text)

if __name__ == "__main__":
    os.chdir("..")
    
    test_video_file = "nas-download\\python\\aiA6_1130321_1.mp4"
    output_text_file = "mp4-to-txt\\python\\aiA6_1130321_1.txt"
    mp4_to_txt(test_video_file, output_text_file)
