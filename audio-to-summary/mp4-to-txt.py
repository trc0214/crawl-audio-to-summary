import subprocess
import speech_recognition as sr
import os
import tempfile
from pydub import AudioSegment

def convert_mp4_to_wav(input_file, wav_file):
    AudioSegment.from_file(input_file).export(wav_file, format='wav')

def get_audio_length(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return len(audio)

def split_audio(audio_file, chunk_length_ms=60000):
    audio = AudioSegment.from_file(audio_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def speech_to_text(audio_chunk, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def process_audio_file(audio_file, language, chunk_length_ms=60000):
    audio_length = get_audio_length(audio_file)
    if audio_length > chunk_length_ms:
        chunks = split_audio(audio_file, chunk_length_ms)
        full_text = ""
        for i, chunk in enumerate(chunks):
            chunk_file = f"chunk_{i}.wav"
            chunk.export(chunk_file, format="wav")
            text = speech_to_text(chunk_file, language)
            full_text += text + " "
            os.remove(chunk_file)
        return full_text
    else:
        return speech_to_text(audio_file, language)
    
def mp4_to_txt(input_file, output_file, language):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        temp_wav_file.close()
        convert_mp4_to_wav(input_file, temp_wav_file.name)
        text = process_audio_file(temp_wav_file.name, language)
        os.remove(temp_wav_file.name)
        
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

if __name__ == "__main__":
    nas_download_folder = {
        "nas-download\\python": {'download_dir': 'mp4-to-txt\\python'},
    }

    for folder, paths in nas_download_folder.items():
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".mp4"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(paths['download_dir'], file.replace(".mp4", ".txt"))
                    mp4_to_txt(input_file, output_file, "zh-TW")
                    print(f"Transcript saved to '{output_file}'")