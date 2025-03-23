Network Traffic Monitor
This project is a Python script that automates the process of logging into a network monitoring dashboard, navigating to a specific graph, and extracting network traffic data (inbound and outbound speeds) from an image using Optical Character Recognition (OCR). The script uses Selenium for web automation and Tesseract for OCR.

Features
Automated Login: Logs into the network monitoring dashboard using provided credentials.

Graph Navigation: Navigates to a specific graph page to view network traffic data.

Image Extraction & OCR: Extracts the graph image, processes it using Tesseract OCR, and extracts inbound and outbound traffic values.

Error Handling: Includes basic error handling to ensure the script runs smoothly.

Prerequisites
Before running the script, ensure you have the following installed:

Python 3.x: The script is written in Python 3.

ChromeDriver: The script uses ChromeDriver for browser automation. It is automatically installed via webdriver_manager.

Tesseract OCR: Install Tesseract OCR on your system and ensure it is accessible in your PATH.

Download Tesseract from here.

Set the path to the Tesseract executable in the script: pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe".

Required Python Libraries: Install the required libraries using pip:

bash
Copy
pip install selenium webdriver-manager pytesseract pillow requests
Usage
Clone the repository:

bash
Copy
git clone https://github.com/your-username/network-traffic-monitor.git
cd network-traffic-monitor
Update the script with your login credentials (if necessary):

python
Copy
username_input.send_keys("your-username")
password_input.send_keys("your-password")
Run the script:

bash
Copy
python main.py
The script will:

Open a Chrome browser window.

Log into the network monitoring dashboard.

Navigate to the specified graph.

Extract and print the inbound and outbound traffic values.

Code Overview
Key Functions
login(): Handles the login process by entering credentials and submitting the form.

navigate_to_graph(): Navigates to the specific graph page containing the network traffic data.

extract_values_from_image(): Extracts the graph image, processes it using OCR, and extracts the inbound and outbound traffic values.

Dependencies
Selenium: Used for browser automation.

Tesseract OCR: Used for extracting text from images.

Pillow: Used for image processing.

Requests: Used for downloading the graph image.

Example Output
Copy
Inbound Current: 45 Mbps
Outbound Current: 23 Mbps
Notes
Ensure the Tesseract path is correctly set in the script.

The script is designed for a specific network monitoring dashboard. You may need to modify the XPaths and URLs for other dashboards.

The script includes a time.sleep() function to allow pages to load. Adjust the sleep duration as needed based on your network speed.
