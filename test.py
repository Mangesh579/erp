from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service =  Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "gLFyf"))
)

input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear()
input_element.send_keys("Mangesh Shrestha" + Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Mangesh Shrestha"))
)

link = driver.find_element(By.PARTIAL_LINK_TEXT, "Mangesh Shrestha")
link.click()

time.sleep(10)



# Extract product names and prices
products = driver.find_elements(By.CLASS_NAME, "product-name")
prices = driver.find_elements(By.CLASS_NAME, "product-price")

data = []
for product, price in zip(products, prices):
    data.append({"Product": product.text, "Price": price.text})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("products.xlsx", index=False)

print("Data extracted successfully!")

driver.quit()
