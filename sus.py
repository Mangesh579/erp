import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytesseract
from PIL import Image
import requests
from io import BytesIO

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def login():
    driver.get("https://graph.subisu.net.np/index.php")
    time.sleep(3)  # Let frames load
    driver.switch_to.frame("page")  # Switch to the 'page' frame

    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Login!!']")))

    username_input.send_keys("username")
    password_input.send_keys("password")
    login_button.click()
    time.sleep(2)
    driver.switch_to.default_content()

def navigate_to_graph():
    wait = WebDriverWait(driver, 5)
    link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'sbgs.php?member=Silverlining-Pvt-Ltd-PL-Durbarmarg') and contains(@href, 'viewmode=1')]")))
    link.click()
    time.sleep(2)

def extract_values_from_image():
    wait = WebDriverWait(driver, 10)
    img_element = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'Silverlining-Pvt-Ltd-PL-Durbarmarg_day.png')]")))
    img_url = img_element.get_attribute("src")

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    # Perform OCR
    extracted_text = pytesseract.image_to_string(img)

    # Updated Regex (check how OCR extracts text)
    match = re.search(r"(?i)out\s*Current:\s*([\d.]+)\s*Mb/s.*?Hin\s*Current:\s*([\d.]+)\s*Mb/s", extracted_text, re.DOTALL)

    if match:
        outbound_current = int(float(match.group(1)))
        inbound_current = int(float(match.group(2)))
        print(f"Inbound Current: {inbound_current} Mbps")
        print(f"Outbound Current: {outbound_current} Mbps")
    else:
        print("Could not extract Inbound/Outbound values.")

try:
    login()
    navigate_to_graph()
    extract_values_from_image()
finally:
    driver.quit()
