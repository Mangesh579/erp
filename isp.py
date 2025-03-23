import re
import base64
import time
from io import BytesIO
from PIL import Image
import pytesseract
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Constants
CHROME_DRIVER_PATH = r"D:\webdriver\chromedriver.exe"
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ERP_LOGIN_URL = "https://erp.silverlining.com.np/BankLog/V2/BankLog.cshtml?Group=8.%20ISP-Link-Monitoring"
ERP_CREDENTIALS = {
    "username": "mangesh.shrestha@silverlining.com.np",
    "password": "Default@123"
}

# Initialize Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

def login_to_erp():
    """Login to the ERP system."""
    driver.get(ERP_LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Username"))).send_keys(ERP_CREDENTIALS["username"])
    driver.find_element(By.NAME, "Password").send_keys(ERP_CREDENTIALS["password"], Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

def input_values_to_erp(values):
    """Input extracted values into ERP form fields."""
    driver.get(ERP_LOGIN_URL)
    time.sleep(3)  # Wait for the page to load
    for field_name, value in values.items():
        driver.find_element(By.NAME, field_name).send_keys(value, Keys.RETURN)

def extract_integer(value):
    """Extract integer part from a string."""
    return value.split('.')[0]

def convert_speed(value, unit):
    """Convert speed to Mbps, set to 1 Mbps if Kbps."""
    return 1 if unit.upper() == "K" else int(float(value))

def extract_values_from_image(img_element):
    """Extract text from an image using OCR."""
    img_src = img_element.get_attribute("src").split(",")[-1]
    image_data = base64.b64decode(img_src)
    image = Image.open(BytesIO(image_data))
    return pytesseract.image_to_string(image)

def process_npix():
    """Process NPIX data."""
    driver.get("https://nms2.npix.net.np/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("silverlining")
    driver.find_element(By.NAME, "password").send_keys("N&p@I#x@@2019%%", Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

    driver.find_element(By.XPATH, '//a[@data-toggle="tab" and @href="#ports"]').click()
    time.sleep(3)  # Wait for content to load

    td_elements = driver.find_elements(By.XPATH, '//td[@align="right"]')
    values = [td.text.strip().replace("\u00a0", " ") for td in td_elements]

    if len(values) >= 36:
        data = {
            "BankLog_756247": extract_integer(values[23]),
            "BankLog_756248": extract_integer(values[26]),
            "BankLog_756249": extract_integer(values[32]),
            "BankLog_756250": extract_integer(values[35])
        }
        input_values_to_erp(data)

def process_wlink(circuit_id, field_names):
    """Process WLINK data."""
    driver.get("https://corporate.worldlink.com.np/login/index")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("S249")
    driver.find_element(By.NAME, "password").send_keys("4120", Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cktarea"))).click()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, circuit_id))).click()

    img_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'data:image/png;base64')]")))
    extracted_text = extract_values_from_image(img_element)

    inbound_match = re.search(r"Inbound\s*Current:\s*([\d]+\.\d+)\s*(M|K)", extracted_text, re.IGNORECASE)
    outbound_match = re.search(r"Outbound\s*Current:\s*([\d]+\.\d+)\s*(M|K)", extracted_text, re.IGNORECASE)

    data = {
        field_names[0]: convert_speed(inbound_match.group(1), inbound_match.group(2)) if inbound_match else "0",
        field_names[1]: convert_speed(outbound_match.group(1), outbound_match.group(2)) if outbound_match else "0"
    }
    input_values_to_erp(data)

def process_subisu():
    """Process Subisu data."""
    driver.get("https://graph.subisu.net.np/index.php")
    time.sleep(3)
    driver.switch_to.frame("page")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("silverlining")
    driver.find_element(By.ID, "password").send_keys("123456", Keys.RETURN)
    time.sleep(2)
    driver.switch_to.default_content()

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'sbgs.php?member=Silverlining-Pvt-Ltd-PL-Durbarmarg') and contains(@href, 'viewmode=1')]"))).click()
    time.sleep(2)

    img_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'Silverlining-Pvt-Ltd-PL-Durbarmarg_day.png')]")))
    img_url = img_element.get_attribute("src")
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    extracted_text = pytesseract.image_to_string(img)

    match = re.findall(r"(?i)Current:\s*([\d.]+)\s*Mb/s", extracted_text)
    if len(match) >= 2:
        data = {
            "BankLog_756255": int(float(match[1])),
            "BankLog_756256": int(float(match[0]))
        }
        input_values_to_erp(data)

def process_mos():
    """Process MOS data."""
    driver.get("https://monitoring.mos.com.np/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login_username"))).send_keys("SilverMOS")
    driver.find_element(By.NAME, "login_password").send_keys("S@<>.M0S", Keys.RETURN)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Login']"))).click()
    time.sleep(3)

    graph_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "graph_16592"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", graph_image)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", graph_image)

    # Wait for large image to load
    time.sleep(3)

    large_graph = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "graph_16592")))
    image_bytes = large_graph.screenshot_as_png
    img = Image.open(BytesIO(image_bytes))
    extracted_text = pytesseract.image_to_string(img)

    download_match = re.search(r"download Current:\s*([\d]+)", extracted_text, re.IGNORECASE)
    upload_match = re.search(r"Upload Current:\s*([\d,.]+)", extracted_text, re.IGNORECASE)

    if download_match and upload_match:
        data = {
            "BankLog_756260": int(float(download_match.group(1))),
            "BankLog_756259": int(float(upload_match.group(1)))
        }
        input_values_to_erp(data)

try:
    login_to_erp()
    process_npix()
    process_wlink("link_7309", ["BankLog_756251", "BankLog_756252"])
    process_wlink("link_7312", ["BankLog_756253", "BankLog_756254"])
    process_subisu()
    process_mos()
finally:
    driver.quit()