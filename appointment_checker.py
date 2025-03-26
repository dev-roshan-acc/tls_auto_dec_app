import time
import smtplib
import config as CONFIGURATION  # Import settings from CONFIGURATION.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pytz  # For timezone management
import random


# ---------------- SEND EMAIL ALERT ----------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert():
    """Sends an email notification when an appointment slot is available."""
    subject = "🎉 TLScontact Appointment Slot Available!"  # Emoji included in the subject
    body = f"An appointment slot is now available. Book it here: {CONFIGURATION.TLS_APPOINTMENT_URL}"
    
    # Create the email message using MIMEMultipart to support both subject and body
    message = MIMEMultipart()
    message["From"] = CONFIGURATION.EMAIL_ADDRESS
    message["To"] = CONFIGURATION.TO_EMAIL
    message["Subject"] = subject
    
    # Attach the body with the message
    message.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(CONFIGURATION.EMAIL_ADDRESS, CONFIGURATION.EMAIL_PASSWORD)
            server.sendmail(CONFIGURATION.EMAIL_ADDRESS, CONFIGURATION.TO_EMAIL, message.as_string())
        print("[✅] Email alert sent!")
    except Exception as e:
        print("[❌] Error sending email:", e)


# ---------------- GET CURRENT TIME IN UK ----------------
def get_current_time_in_uk():
    """Gets the current time in the UK (GMT/BST)."""
    uk_timezone = pytz.timezone("Europe/London")
    return datetime.now(uk_timezone)


# ---------------- LOGGING ----------------
def log_message(message):
    """Logs the message to a file."""
    with open(CONFIGURATION.LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


# ---------------- CHECK TLS CONTACT SLOTS ----------------
def check_slots():
    """Logs in to TLScontact, checks for available slots, and sends an alert if found."""
    
    # Get the current time in the UK
    current_time = get_current_time_in_uk()
    print(f"[⏰] Current time in UK: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define operating hours
    if current_time.hour >= CONFIGURATION.OFF_PEAK_START and current_time.hour < CONFIGURATION.OFF_PEAK_END:
        # Off-peak hours (increase frequency of checks)
        check_interval = CONFIGURATION.OFF_PEAK_INTERVAL
        log_message(f"[INFO] Off-peak hours detected. Frequency set to {check_interval} seconds.")
    else:
        # Working hours (default frequency)
        check_interval = CONFIGURATION.PEAK_INTERVAL
        log_message(f"[INFO] Peak hours detected. Frequency set to {check_interval} seconds.")
    
    # Setup Chrome options
    options = Options()
    options.headless = CONFIGURATION.HEADLESS_MODE  # Run in background if True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("[🌍] Opening TLScontact login page...")
        driver.get(CONFIGURATION.TLS_HOME_URL)
        wait = WebDriverWait(driver, 15)

        # Step 1: Login to TLS Contact
        try:
            # Step 2: Click the "Login" button to navigate to the login page
            login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tls-button-link")))
            login_button.click()
            print("[ℹ] Clicked the login button, navigating to login page...")
            
            # Step 3: Locate the email and password fields and login
            email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
            
            email_input.send_keys(CONFIGURATION.TLS_USERNAME)
            password_input.send_keys(CONFIGURATION.TLS_PASSWORD)
            password_input.send_keys(Keys.RETURN)

            print("[🔑] Logging in...")
            time.sleep(5)

            # Verify login success
            if driver.current_url == "https://visas-de.tlscontact.com/formGroup/gb/gbLON2de":
                print("[✅] Login successful!")
            else:
                print("[❌] Login failed! Check credentials or website issues.")
                return  # Exit after login failure
                
        except Exception as e:
            print(f"[❌] Login failed! Error: {e}")
            return  # Exit after login failure

        # Step 2: Navigate to Appointment Page
        driver.get(CONFIGURATION.TLS_APPOINTMENT_URL)
        print("[📅] Checking appointment availability...")
        time.sleep(5)

        # Step 3: Check for available slots
        try:
            slots = driver.find_elements(By.XPATH, "//span[contains(text(), 'Available')]")
            
            # Debug: Print the available slot count
            print(f"[🔍] Found {len(slots)} slots (if any).")
            
            if slots:
                print("[🎉] Slot available! Sending email alert...")
                send_email_alert()
                
            else:
                print("[🔄] No slots available. Checking again later...")

        except Exception as e:
            print(f"[⚠️] Error checking slots: {e}")
            

    except Exception as e:
        print(f"[⚠️] Error checking slots: {e}")

    finally:
        driver.quit()
        print(f"[⏳] Waiting {check_interval} seconds before checking again...\n")
        time.sleep(check_interval)


# ---------------- RUN CONTINUOUSLY ----------------
while True:
    check_slots()
