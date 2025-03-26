# TLScontact Appointment Checker

This is an automated Python script that checks for available appointment slots on the TLScontact website and sends an email alert when a slot becomes available. It runs continuously, checking for slots at intervals and notifying you via email when an appointment is found.

## Features
- Logs in to TLScontact and navigates to the appointment page.
- Checks for available appointment slots.
- Sends an email notification when a slot becomes available.
- Configurable check intervals for peak and off-peak hours.
- Runs continuously in the background.

## Prerequisites

- Python 3.6+ installed.
- A Gmail account for sending email alerts (you'll need to create an app password for secure access).
- Chrome browser and `chromedriver` for Selenium.

