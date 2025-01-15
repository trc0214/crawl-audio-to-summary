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
    
    video_base_url = "https://wmnl1691.direct.quickconnect.to:5001/?launchApp=SYNO.VideoController2.Application&SynoToken=39YEsxYDI58o6&launchParam=player_id%3Dstreaming%26browse_type%3Dfilevideo%26video_type%3Dfilevideo%26is_drive%3Dfalse%26path%3D%252Fvolume1%252FAIITLAB%252F%25E6%2596%25B0%25E7%2594%259F%25E5%2585%25A5%25E5%25AD%25B8%25E6%2595%2599%25E6%259D%2590(%25E5%25BF%2585%25E7%259C%258B)%252F"
    
    freshman_requirements = {
        "python_folder": {
            "folder_name": "1.%2520Python%252F",
            "video_id": {
                "Aia6": {
                    "113": {
                        "03": {"05": {"1"}}
                    }
                },
                "aiA6": {
                    "113": {
                        "03": {"05": {"2","3","4","5","6"},
                                "07": {"1","2","3","4","5","6"},
                                "10": {"1","2","3","4","5","6"},
                                "12": {"1","2","3","4","5","6"},
                                "14": {"1","2","3","4","5","6"},
                                "17": {"1","2","3","4","5"},
                                "19": {"1","2","3","5"},
                                "21": {"1","2","3","4","5","6"},
                                }
                    }
                }
            },
            "download_dir": "nas-download\\python",
        },
        "numpy_folder": {
            "folder_name": "2.%2520Numpy%252F",
            "video_id": {
                "aiA6": {
                    "113": {
                        "03": {
                                "24": {"1","2","3","4","5","6"},
                                "26": {"1","2","3","4","5","6"},
                            },
                        "04": {"02": {"1","2","3","4","5","6"},}
                    }
                }
            },
            "download_dir": "nas-download\\numpy",
        },
        "powerbi_folder": {
            "folder_name": "3.%2520PowerBI%252F",
            "video_id": {
                "aiA6": {
                    "113": {
                        "03": {
                                "28": {"1","2","3","4","5","6"},
                                "31": {"1","2","3","4","5","6"},
                            },
                    }
                }
            },
            "download_dir": "nas-download\\powerbi",
        },
        "machine_learning_folder": {
            "folder_name": "4.%2520%25E6%25A9%259F%25E5%2599%25A8%25E5%25AD%25B8%25E7%25BF%2592%252F",
            "video_id": {
                "aiA6": {
                    "113": {
                        "04": {
                                "09": {"1","2","3","4","5","6"},
                                "11": {"1","2","3","4","5","6"},
                            },
                    }
                }
            },
            "download_dir": "nas-download\\machine-learning",
        },
        "deep_learning_folder": {
            "folder_name": "5.%2520%25E6%25B7%25B1%25E5%25BA%25A6%25E5%25AD%25B8%25E7%25BF%2592%252F",
            "video_id": {
                "Aia6": {
                    "113": {
                        "04": {
                            "16": {"1","2","3","4","5","6","7"},
                            "23": {"1","2","3","4","5","6","7"},
                            "28": {"1","2","3","4","5","6","7"},
                        }
                    }
                },
                "aiA6": {
                    "113": {
                        "04": {"14": {"1","2","3","4","5","6"},
                                "21": {"1","2","3","4","5","6"},
                                "30": {"1","2","3","4","5","6"},
                                }
                    }
                }
            },
            "download_dir": "nas-download\\deep-learning",
        },
        "chatgpt_folder": {
            "folder_name": "6.%2520ChatGPT%25E6%2587%2589%25E7%2594%25A8%252F",
            "video_id": {
                "aiA6": {
                    "113": {
                        "05": {
                            "02": {"1", "2", "3", "4", "5", "6"},
                            "05": {"1", "2", "3", "4", "5"},
                            "07": {"1", "2", "3", "4", "5", "6"},
                            "09": {"1", "2", "3", "4", "5"},
                        },
                    }
                }
            },
            "download_dir": "nas-download\\chatgpt",
        },
    }

    for folder in freshman_requirements.values():
        for prefix, years in folder["video_id"].items():
            for year, months in years.items():
                for month, days in months.items():
                    for day, lessons in days.items():
                        for lesson in lessons:
                            video_id = f"{prefix}_{year}{month}{day}_{lesson}"
                            filename = f"{video_id}.mp4"
                            file_path = os.path.join(folder["download_dir"], filename)
                            
                            if os.path.exists(file_path):
                                print(f"File {filename} already exists. Skipping download.")
                                continue
                            
                            print(f"Downloading {video_id}")
                            video_url = video_base_url + folder["folder_name"] + video_id + ".mp4"
                            direct_url = get_direct_url(driver, video_url, "_html5_video_player")
                            if direct_url:
                                download_file(direct_url, folder["download_dir"], filename)
                                time.sleep(15)
    driver.quit()