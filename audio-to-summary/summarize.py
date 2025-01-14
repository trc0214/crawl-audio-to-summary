import os
from openai import AzureOpenAI

def txt_to_summarize(input_file, output_file, azure_endpoint, api_key, api_version="2024-02-01", model="gpt-35-turbo-16k", ai_theme="給以下文章摘要"):
    with open(input_file, 'r', encoding='utf-8') as f:
        article_text = f.read()

    prompt = [
            {
                "role": "system",
                "content": f"{ai_theme}."
            },
            {
                "role": "user",
                "content": f"User says: {article_text}"
            }
        ]
    client = AzureOpenAI(azure_endpoint=azure_endpoint, api_key=api_key, api_version=api_version)
    
    ai_response = client.chat.completions.create(model=model , messages=prompt).choices[0].message.content
        
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ai_response)

if __name__ == "__main__":
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY") 
    api_version = "2024-02-01"
    model = "gpt-35-turbo-16k"
    ai_theme = "用中文給以下文章摘要"
    
    txt_folder = "mp4-to-txt"
    summary_folder = "txt-to-summary"
    
    for folder in os.listdir(txt_folder):
        for file in os.listdir(f"{txt_folder}/{folder}"):
            if file.endswith(".txt"):
                output_folder = f"{summary_folder}/{folder}"
                if os.path.exists(f"{output_folder}/{file}"):
                    print(f"File {file} already exists. Skipping...")
                    continue
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                txt_to_summarize(f"{txt_folder}/{folder}/{file}", f"{output_folder}/{file}", azure_endpoint, api_key, api_version, model, ai_theme)
                print(f"Converted {file} to text.")