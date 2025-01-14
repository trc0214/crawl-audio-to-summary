import os
import tempfile
from pydub import AudioSegment
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def convert_mp4_to_wav(input_file, wav_file):
    AudioSegment.from_file(input_file).export(wav_file, format='wav')

def wav_to_txt(input_file, output_file, model_id="openai/whisper-large-v3-turbo", device="cuda:0"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )
    
    result = pipe(input_file)
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
def mp4_to_txt(input_file, output_file):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        convert_mp4_to_wav(input_file, temp_wav_file.name)
        wav_to_txt(temp_wav_file.name, output_file)
    os.remove(temp_wav_file.name)

if __name__ == "__main__":
    
    mp4_folder = "nas-download"
    txt_folder = "mp4-to-txt"
    
    for folder in os.listdir(mp4_folder):
        for file in os.listdir(f"{mp4_folder}/{folder}"):
            if file.endswith(".mp4"):
                mp4_to_txt(f"{mp4_folder}/{folder}/{file}", f"{txt_folder}/{folder}/{file.replace('.mp4', '.txt')}")
                print(f"Converted {file} to text.")