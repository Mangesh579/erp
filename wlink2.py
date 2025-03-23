import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
from PIL import Image
import pytesseract
from io import BytesIO

# Initialize WebDriver (Ensure you have chromedriver installed)
driver = webdriver.Chrome()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

try:
    # Open the login page
    driver.get("https://corporate.worldlink.com.np/login/index")
    
    # Wait for the username input to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Enter username
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("S249")  # Replace with actual username
    
    # Enter password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("4120")  # Replace with actual password
    
    # Click the login button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Log me in']"))
    ).click()
    
    # Wait for navigation and click Kathmandu link
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "cktarea"))
    ).click()
    
    time.sleep(3)
    
    # Click on the specific circuit link
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "link_7312"))
    ).click()
    
    # Wait for the image containing traffic data
    img_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'data:image/png;base64')]"))
    )

    # Extract base64 data from the image
    img_src = img_element.get_attribute("src").split(",")[-1]
    
    # Decode the base64 image data
    image_data = base64.b64decode(img_src)
    image = Image.open(BytesIO(image_data))
    
    # Perform OCR to extract text
    extracted_text = pytesseract.image_to_string(image)

    # Modify regex to capture both Mbps and Kbps values
    inbound_match = re.search(r"Inbound\s*Current:\s*([\d]+\.\d+)\s*(M|K)", extracted_text, re.IGNORECASE)
    outbound_match = re.search(r"Outbound\s*Current:\s*([\d]+\.\d+)\s*(M|K)", extracted_text, re.IGNORECASE)

    def convert_speed(value, unit):
        """ Convert speed to Mbps, set to 1 Mbps if Kbps """
        if unit.upper() == "K":
            return 1  # If Kbps, set to 1 Mbps
        return int(float(value))  # Convert to integer if Mbps

    # Convert extracted values
    inbound_current = convert_speed(inbound_match.group(1), inbound_match.group(2)) if inbound_match else "0"
    outbound_current = convert_speed(outbound_match.group(1), outbound_match.group(2)) if outbound_match else "0"

    # Print extracted values
    print("Inbound Current:", inbound_current, "Mbps")
    print("Outbound Current:", outbound_current, "Mbps")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()
