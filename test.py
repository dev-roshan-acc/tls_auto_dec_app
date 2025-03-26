from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open TLS Contact website
TLS_URL = "https://visas-de.tlscontact.com/appointment/gb/gbLON2de/2995819"
driver.get(TLS_URL)

input("✅ Website loaded successfully. Press Enter to close...")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for the appointment section to load
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    appointment_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "your_element_selector_here")))
    print("✅ Appointment section loaded!")
except:
    print("⚠️ Error: Could not find the appointment section.")


driver.quit()
