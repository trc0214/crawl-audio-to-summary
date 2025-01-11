import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv 
import os
from selenium.webdriver.common.keys import Keys
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def driver_setup():
    options =  webdriver.ChromeOptions()
    options.add_argument('--enable-logging')
    options.add_argument('--v=1')
    return webdriver.Chrome(options=options)

def nas_login(driver, login_url, username, password):
    driver.get(login_url)
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "current-password"))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

def get_direct_url(driver, orginal_url, url_element):
    try:
        driver.get(orginal_url)
        target_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, url_element))
        )
        target_url = target_element.get_attribute("src")
        return target_url
    except TimeoutException:
        print(f"Error: Element with ID '{url_element}' not found within the given time.")
    except NoSuchElementException:
        print(f"Error: Element with ID '{url_element}' does not exist on the page.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def download_file(url, download_dir, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        with open(f"{download_dir}/{filename}", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)

        print(f"File downloaded successfully to '{filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")    


if __name__ == "__main__":
    load_dotenv()
    login_url, username, password = os.getenv("NAS_URL"), os.getenv("NAS_USERNAME"), os.getenv("NAS_PASSWORD")
    driver = driver_setup()
    nas_login(driver, login_url, username, password)
    
    video_base_url = "https://wmnl1691.direct.quickconnect.to:5001/?launchApp=SYNO.VideoController2.Application&SynoToken=39YEsxYDI58o6&launchParam=player_id%3Dstreaming%26browse_type%3Dfilevideo%26video_type%3Dfilevideo%26is_drive%3Dfalse%26path%3D%252Fvolume1%252FAIITLAB%252F%25E6%2596%25B0%25E7%2594%259F%25E5%2585%25A5%25E5%25AD%25B8%25E6%2595%2599%25E6%259D%2590(%25E5%25BF%2585%25E7%259C%258B)%252F1.%2520Python%252F"
    
    freshman_requirements = {
        "python_folder": {
            "year": "113",
            "mounth": "03",
            "dates_lessons": {"05", "07", "10", "12", "14", "17", "19", "21"},
            "defult_lesson": 6,
            "download_dir": "nas-download\\python",
        }
    }

    for folder in freshman_requirements.values():
            for date in folder["dates_lessons"]:
                for lesson in range(1, folder["defult_lesson"]):
                    video_id = f"aiA6_{folder['year']}{folder['mounth']}{date}_{lesson}"
                    filename = f"{video_id}.mp4"
                    file_path = os.path.join(folder["download_dir"], filename)
                    
                    if os.path.exists(file_path):
                        print(f"File {filename} already exists. Skipping download.")
                        continue
                    
                    print(f"Downloading {video_id}")
                    video_url = video_base_url + video_id + ".mp4"
                    direct_url = get_direct_url(driver, video_url, "_html5_video_player")
                    if direct_url:
                        download_file(direct_url, folder["download_dir"], filename)
                        time.sleep(15)