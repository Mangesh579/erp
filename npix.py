from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
driver = webdriver.Chrome()

# Step 1: Login
driver.get("https://nms2.npix.net.np/login")  # Replace with actual login URL

# Find and fill in login fields (update selectors as needed)
username_input = driver.find_element(By.NAME, "username")  # Replace with actual field name
password_input = driver.find_element(By.NAME, "password")  # Replace with actual field name

username_input.send_keys("username")  # Replace with actual username
password_input.send_keys("password")  # Replace with actual password
password_input.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(5)  # Adjust as necessary

# Step 2: Click on "Ports" tab
ports_tab = driver.find_element(By.XPATH, '//a[@data-toggle="tab" and @href="#ports"]')
ports_tab.click()

# Wait for content to load
time.sleep(3)

# Step 3: Extract inbound and outbound values
try:
    well_div = driver.find_element(By.XPATH, '//div[@class="well"]')
    text_content = well_div.text
    
    # Extract Inbound and Outbound values (modify regex if needed)
    td_elements = driver.find_elements(By.XPATH, '//td[@align="right"]')

    values = [td.text.strip().replace("\u00a0", " ") for td in td_elements]
    def extract_integer(value):
        return value.split('.')[0]  # Splits at '.' and takes the first part

    # Ensure we have enough values before accessing indices
    if len(values) >= 36:
        print("DATA HUB Inbound:", extract_integer(values[23]))  
        print("DATA HUB Outbound:", extract_integer(values[26]))  
        print("Accesswoorld Inbound:", extract_integer(values[32]))  
        print("Accessworld Outbound:", extract_integer(values[35]))  
    else:
        print("Not enough data extracted.") 
  
except Exception as e:
    print(f"Error extracting values: {e}")

# Close the driver
driver.quit()
