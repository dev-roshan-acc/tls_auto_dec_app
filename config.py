# ------------------------- CONFIGURATION -------------------------

# TLScontact URLs
TLS_LOGIN_URL = "https://auth.visas-de.tlscontact.com/auth/realms/atlas/protocol/openid-connect/auth?response_type=code&client_id=web_app&scope=openid%20roles%20atlas%20web-origins%20email%20offline_access%20profile%20address%20phone&state=jKhhh8yCnyc7oUlTfAIkxGF-OKaxWtlNHXjDAHHf55c%3D&redirect_uri=https://visas-de.tlscontact.com/login/oauth2/code/oidc&issuer=gbLON2de"
TLS_APPOINTMENT_URL = "https://visas-de.tlscontact.com/appointment/gb/gbLON2de/2995819"
TLS_HOME_URL = "https://visas-de.tlscontact.com/visa/gb/gbLON2de/home"

# TLScontact Credentials
TLS_USERNAME = "acc.roshanshrestha@gmail.com"
TLS_PASSWORD = "@System9813"  # Ensure you use app-specific password or environment variable

# Email Credentials for Alerts
EMAIL_ADDRESS = "acc.roshanshrestha@gmail.com"
EMAIL_PASSWORD = "your_email_app_password_here"  # Ensure you use app-specific password
TO_EMAIL = "acc.roshanshrestha@gmail.com"

# Timezone
TIMEZONE = "Europe/London"

# Working hours for TLScontact appointment checking
WORKING_HOURS_START = 9
WORKING_HOURS_END = 18

# Off-peak hours (for more frequent checks)
OFF_PEAK_START = 0
OFF_PEAK_END = 2
OFF_PEAK_INTERVAL = 300  # 5 minutes during off-peak hours

# Peak hours (for less frequent checks)
PEAK_INTERVAL = 600  # 10 minutes during peak hours (between 9 AM - 6 PM)

# Check Interval
CHECK_INTERVAL = PEAK_INTERVAL

# Headless Mode
HEADLESS_MODE = False  # Set to True for background execution

# Randomized sleep time between checks (in seconds)
RANDOM_SLEEP_MIN = 5
RANDOM_SLEEP_MAX = 15

# Log file settings
LOG_FILE = "appointment_checker_log.txt"
