# import necessary libraries

import numpy as np
import pandas as pd
import os
import zipfile

from transformers import MgpstrProcessor, MgpstrForSceneTextRecognition
from PIL import Image
import cv2
import torch

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from PIL import Image
import tempfile
import random
import time

import undetected_chromedriver as uc


import shutil

from fp.fp import FreeProxy



def obtain_captcha_text(filename):
    # Assuming processor and model are already defined
    processor = MgpstrProcessor.from_pretrained('alibaba-damo/mgp-str-base')
    model = MgpstrForSceneTextRecognition.from_pretrained('alibaba-damo/mgp-str-base')


    # Load image
    # captcha_image_path = "image_file.png"
    captcha_image_path = filename
    image = cv2.imread(captcha_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB since PIL needs RGB
    image = Image.fromarray(image)

    # Process the image and get pixel values
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    # Generate model output
    with torch.no_grad():  # Prevent backpropagation since you're not training
        outputs = model(pixel_values)

    # Decode the output to get generated text
    generated_text = processor.batch_decode(outputs.logits)

    output = generated_text['generated_text'][0].upper()
    # print(output)

    return output



# Process HK Market Data
def move_hk_market_data():
    # Define the paths
    zip_file_path = "raw/d_hk_txt.zip"
    extraction_path = "extracted_data"
    output_path_etf = "hk/etf"
    output_path_stocks = "hk/stocks"

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Define the directories for ETFs and Stocks
    hk_path = os.path.join(extraction_path, "data", "daily", "hk")
    etf_folder = os.path.join(hk_path, "hkex etfs")
    stocks_folder = os.path.join(hk_path, "hkex stocks")


    # Create output directories if they don't exist
    os.makedirs(output_path_etf, exist_ok=True)
    os.makedirs(output_path_stocks, exist_ok=True)

    # Function to process .txt files and save as .csv
    def process_txt_to_csv(input_path, output_path, suffix="-HKD"):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".txt"):
                    input_file = os.path.join(root, file)
                    # Load the .txt file
                    df = pd.read_csv(input_file, sep=",")  # Adjust delimiter if necessary
                    # Clean the column headers to remove '<>' characters
                    df.columns = [col.strip('<>').strip() for col in df.columns]
                    # Extract the filename before the first dot
                    ticker = file.split('.')[0]
                    output_file = os.path.join(output_path, f"{ticker.upper()}{suffix}.csv")
                    df.to_csv(output_file, index=False)

    # Process ETF data
    process_txt_to_csv(etf_folder, output_path_etf)

    # Process Stock data (loop through subfolders)
    for subfolder in os.listdir(stocks_folder):
        subfolder_path = os.path.join(stocks_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            process_txt_to_csv(subfolder_path, output_path_stocks)

# Process US Market Data

def move_us_market_data():
    # Define the paths
    zip_file_path = "raw/d_us_txt.zip"
    extraction_path = "extracted_data"
    output_path_etf = "us/etf"
    output_path_stocks = "us/stocks"

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Define the directories for ETFs and Stocks
    us_path = os.path.join(extraction_path, "data", "daily", "us")
    nas_etf_folder = os.path.join(us_path, "nasdaq etfs")
    ny_etf_folder = os.path.join(us_path, "nyse etfs")

    nas_stock_folder = os.path.join(us_path, "nasdaq stocks")
    ny_stock_folder = os.path.join(us_path, "nyse stocks")


    # Create output directories if they don't exist
    os.makedirs(output_path_etf, exist_ok=True)
    os.makedirs(output_path_stocks, exist_ok=True)

    # Function to process .txt files and save as .csv
    def process_txt_to_csv(input_path, output_path, suffix="-USD"):
        for root, _, files in os.walk(input_path):
            for file in files:
                try:
                    if file.endswith(".txt"):
                        input_file = os.path.join(root, file)
                        # Load the .txt file
                        df = pd.read_csv(input_file, sep=",")  # Adjust delimiter if necessary
                        # Clean the column headers to remove '<>' characters
                        df.columns = [col.strip('<>').strip() for col in df.columns]
                        # Extract the filename before the first dot
                        ticker = file.split('.')[0]
                        output_file = os.path.join(output_path, f"{ticker.upper()}{suffix}.csv")
                        df.to_csv(output_file, index=False)
                except:
                    print("Error handling: "+file)

    # Process NASDAQ ETF data
    process_txt_to_csv(nas_etf_folder, output_path_etf)

    # Process NASDAQ Stock data (loop through subfolders)
    for subfolder in os.listdir(nas_stock_folder):
        subfolder_path = os.path.join(nas_stock_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            process_txt_to_csv(subfolder_path, output_path_stocks)



    # Process NYSE ETF data (loop through subfolders)
    for subfolder in os.listdir(ny_etf_folder):
        subfolder_path = os.path.join(ny_etf_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            process_txt_to_csv(subfolder_path, output_path_etf)

    # Process NYSE Stock data (loop through subfolders)
    for subfolder in os.listdir(ny_stock_folder):
        subfolder_path = os.path.join(ny_stock_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            process_txt_to_csv(subfolder_path, output_path_stocks)



# Process UK Market Data

def move_uk_market_data():
    # Define the paths
    zip_file_path = "raw/d_uk_txt.zip"
    extraction_path = "extracted_data"
    output_path_etf = "uk/etf"
    output_path_stocks = "uk/stocks"

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Define the directories for ETFs and Stocks
    uk_path = os.path.join(extraction_path, "data", "daily", "uk")
    etf_folder = os.path.join(uk_path, "lse etfs")
    stocks_folder = os.path.join(uk_path, "lse stocks")


    # Create output directories if they don't exist
    os.makedirs(output_path_etf, exist_ok=True)
    os.makedirs(output_path_stocks, exist_ok=True)

    # Function to process .txt files and save as .csv
    def process_txt_to_csv(input_path, output_path, suffix="-GBP"):
        for root, _, files in os.walk(input_path):
            for file in files:
                try:
                    if file.endswith(".txt"):
                        input_file = os.path.join(root, file)
                        # Load the .txt file
                        df = pd.read_csv(input_file, sep=",")  # Adjust delimiter if necessary
                        # Clean the column headers to remove '<>' characters
                        df.columns = [col.strip('<>').strip() for col in df.columns]
                        # Extract the filename before the first dot
                        ticker = file.split('.')[0]
                        output_file = os.path.join(output_path, f"{ticker.upper()}{suffix}.csv")
                        df.to_csv(output_file, index=False)
                except:
                    print("Error fetching data for: " + file)

    # Process Stocks data
    process_txt_to_csv(stocks_folder, output_path_stocks)

    # Process ETF data (loop through subfolders)
    for subfolder in os.listdir(etf_folder):
        subfolder_path = os.path.join(etf_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            process_txt_to_csv(subfolder_path, output_path_etf)



# Process Macro Data for different countries

def move_macro_data():
    # Define the paths
    zip_file_path = "raw/d_macro_txt.zip"
    extraction_path = "extracted_data"
    us_output_path = "macro/us"
    uk_output_path = "macro/uk"
    ca_output_path = "macro/ca"
    cn_output_path = "macro/cn"

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Define the directories for ETFs and Stocks
    path = os.path.join(extraction_path, "data", "daily", "macro")
    us_folder = os.path.join(path, "us")
    ca_folder = os.path.join(path, "ca")
    uk_folder = os.path.join(path, "uk")
    cn_folder = os.path.join(path, "cn")



    # Create output directories if they don't exist
    os.makedirs(us_output_path, exist_ok=True)
    os.makedirs(uk_output_path, exist_ok=True)
    os.makedirs(ca_output_path, exist_ok=True)
    os.makedirs(cn_output_path, exist_ok=True)

    # Function to process .txt files and save as .csv
    def process_txt_to_csv(input_path, output_path, suffix=""):
        for root, _, files in os.walk(input_path):
            for file in files:
                try:
                    if file.endswith(".txt"):
                        input_file = os.path.join(root, file)
                        # Load the .txt file
                        df = pd.read_csv(input_file, sep=",")  # Adjust delimiter if necessary
                        # Clean the column headers to remove '<>' characters
                        df.columns = [col.strip('<>').strip() for col in df.columns]
                        # Extract the filename before the first dot
                        ticker = file.split('.')[0]
                        output_file = os.path.join(output_path, f"{ticker.upper()}{suffix}.csv")
                        df.to_csv(output_file, index=False)
                except:
                    print("Error fetching data for: " + file)

    # Process us macro data
    process_txt_to_csv(us_folder, us_output_path)
    process_txt_to_csv(uk_folder, uk_output_path)
    process_txt_to_csv(ca_folder, ca_output_path)
    process_txt_to_csv(cn_folder, cn_output_path)


user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0",
]

proxy_list = [
  "192.168.1.10:8080",  # replace with your proxies
  "192.168.1.11:8081",
    # ... more proxies
]



def get_proxy_from_api():
    try:
        # Initialize FreeProxy with desired parameters
        proxy = FreeProxy(country_id=['CA'], timeout=1, rand=True).get()
        return proxy
    except Exception as e:
        print(f"Error fetching proxy: {e}")
        return None


def get_random_user_agent():
    return random.choice(user_agents)

# def get_random_proxy():
#     return random.choice(proxy_list)

'''
# Initialize the WebDriver with options for resetting session
def initialize_driver():
    # Create a temporary user data directory
    temp_user_data_dir = tempfile.mkdtemp()
    
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    
    # Use a fresh user data directory for a clean session
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    user_agent = get_random_user_agent()
    print(user_agent)
    options.add_argument(f"user-agent={user_agent}")
    proxy_address = get_proxy_from_api()[7:]
    options.add_argument(f'--proxy-server={proxy_address}')

    # options.add_argument("--headless")

    # Avoid automation detection
    # options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Disable caching for a fresh session
    # options.add_argument("--disable-application-cache")
    # options.add_argument("--disable-cache")
    # options.add_argument("--disable-offline-load-stale-cache")
    # options.add_argument("--disk-cache-size=0")
    
    # Start Chrome in incognito mode (optional, for extra privacy)
    # options.add_argument("--incognito")
    
    # Disable browser extensions
    # options.add_argument("--disable-extensions")
    
    # Disable password manager
    # options.add_argument("--disable-save-password-bubble")

    # Add desired capabilities for headers
    # capabilities = DesiredCapabilities.CHROME.copy()
    # capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    # Set up the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options) #, desired_capabilities=capabilities)

    # driver = webdriver.Chrome(options=options)
    # driver.delete_all_cookies()
    # driver.execute_script("window.localStorage.clear();")
    # driver.execute_script("window.sessionStorage.clear();")

    print("New browser session initialized.")
    return driver
'''

# # Initialize the WebDriver with options for resetting session
# def initialize_driver():
#     driver = uc.Chrome(headless=False,use_subprocess=False)
#     print("New browser session initialized.")
#     return driver


# Initialize the WebDriver with options for resetting session
def initialize_driver():
    # Create a temporary user data directory
    temp_user_data_dir = tempfile.mkdtemp()
    
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    
    # Use a fresh user data directory for a clean session
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    
    # Set up the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options) #, desired_capabilities=capabilities)

    print("New browser session initialized.")
    return driver

def save_captcha_image(driver):
    # Capture the CAPTCHA image
    captcha_element = driver.find_element(By.ID, "cpt_cd")
    location = captcha_element.location
    size = captcha_element.size

    # Take a full-page screenshot
    screenshot_path = "full_screenshot.png"
    driver.save_screenshot(screenshot_path)

    captcha_filename = "captcha.png"

    # Crop to the CAPTCHA area
    with Image.open(screenshot_path) as img:
        left = int(location['x'])
        top = int(location['y'])
        right = left + (int(size['width']) * 2.5)
        bottom = top + (int(size['height']) * 2.2)

        captcha_area = img.crop((1.2 * left, 1.25 * top, right, bottom))
        captcha_area.save(captcha_filename)

    print("Screenshot of CAPTCHA saved as 'captcha.png'.")
    return captcha_filename


def check_captcha_status(driver):
    table = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.ID, 't11')) ) 
    # Locate the <tr> element within the table 
    tr_element = table.find_element(By.ID, 'cpt_al') 
    # Locate the <td> element within the <tr> element 
    td_element = tr_element.find_element(By.ID, 'f13') 
    # Locate the <b> element within the <td> element 
    b_element = td_element.find_element(By.TAG_NAME, 'b') 
    # Print the text within the <b> tag
    return b_element.text

def download_data(driver, link_extension = 'd_us_txt', captcha=True):
 # Open the URL
    url = 'https://stooq.com/db/h/'
    driver.get(url)

    time.sleep(random.uniform(2, 10)) # random delay

    # Wait for the CAPTCHA to appear and solve it manually
    print("Please solve the CAPTCHA automatically...")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '{0}')]".format(link_extension)))  # Wait until the specific link is visible
    )

    # Click on the desired link
    target_link = driver.find_element(By.XPATH, "//a[contains(@href, '{0}')]".format(link_extension))
    target_link.click()

    time.sleep(random.uniform(2, 5)) # random delay


    if captcha == True:

        # try:
        # Wait for CAPTCHA to appear
        print("CAPTCHA detected")
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "cpt_cd"))  # Wait for the CAPTCHA to load
        )

        control_status = False
        while(control_status==False):
            # Save and process the CAPTCHA
            captcha_filename = save_captcha_image(driver)
            captcha_text = obtain_captcha_text(captcha_filename)
            # Attempt to type the CAPTCHA and press Enter
            webdriver.ActionChains(driver).send_keys(captcha_text).perform()
            time.sleep(2)
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

            time.sleep(random.uniform(1, 5)) # random delay

            status = check_captcha_status(driver)
            if status == "Wrong code! Try again": 
                print("CAPTCHA submission failed. Resetting CAPTCHA...")
                reset_button = driver.find_element(By.XPATH, "//a[@onclick='cpt_o();return false']")
                reset_button.click()
                print("CAPTCHA has been reset. Retrying...")
            else: 
                control_status = True # pass the logic
                break

            time.sleep(random.uniform(2, 5)) # random delay

        # Wait for the download notification to appear
        print("Waiting for the notification with download ID 'cpt_gh'...")
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cpt_gh"))
        )

        # Click the Download link
        download_button.click()
        print("File download initiated.")
        time.sleep(random.uniform(2, 5)) # random delay
    else:
        pass

    print("Downloading other files")
    return None


def move_file(src, dest):
    shutil.move(src, dest)

def move_market_data(filename=''):
    user_name = 'oyetu' # Kenny
    file_directory = f'C:/Users/{user_name}/OneDrive/Documents/Research Work/Quant/QuantOptimus/Foundational Data Generation/raw/'
    download_directory = f'C:/Users/{user_name}/Downloads/'

    # check if the file_directory exist, if not, create the directory
    os.makedirs(file_directory, exist_ok=True)

    # move the just downloaded file into historical data directory
    src_file = download_directory + filename
    dest_file = file_directory + filename
    move_file(src_file, dest_file)


def delete_folder(folder_path = 'raw'):
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Delete the folder and its contents
        shutil.rmtree(folder_path)
        print(f'The folder at {folder_path} has been deleted.')
    else:
        print(f'The folder at {folder_path} does not exist or is not a directory.')

