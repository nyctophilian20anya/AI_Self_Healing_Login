import os
import ssl
import threading
import time

import certifi
import google.generativeai as genai
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ================= SSL FIX =================
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["PYTHONHTTPSVERIFY"] = "0"
ssl._create_default_https_context = ssl._create_unverified_context
print("✅ SSL bypass enabled for Gemini API")
# ===========================================


# ================= AI CONFIG =================
# Gemini AI optional - comment out for ChromeDriver test
# YOUR_API_KEY = "AIzaSyCwyQgp-c0rX-IctwTAeQgNoqHTaLPNMjk"
# genai.configure(api_key=YOUR_API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash")
# print("🤖 Gemini AI model loaded")
# =============================================


def ask_ai_with_timeout(prompt, timeout=8):
    """
    Gemini call with timeout - DISABLED for ChromeDriver test
    """
    print("⚠️ AI DISABLED - using fallback locators")
    return "//input[@id='username']"  # Dummy XPath for testing

def ask_ai_for_xpath(html, description):
    print(f"🤖 SIMULATED AI for {description}")
    if "username" in description:
        return "//input[@id='username']"
    elif "password" in description:
        return "//input[@id='password']"
    else:
        return "//button[@type='submit']"


def run_test():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ FIXED DRIVER - MANUAL PATH (bypasses WinError 193)
    service = Service(r"C:\Users\TA40096281\.wdm\drivers\chromedriver\win64\146.0.7680.165\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    print("✅ Chrome started with manual driver")

    wait = WebDriverWait(driver, 10)
    driver.maximize_window()

    try:
        print("✅ Opening browser...")
        driver.get("https://the-internet.herokuapp.com/login")

        # ================= USERNAME =================
        try:
            username = driver.find_element(By.ID, "wrong-username")
        except NoSuchElementException:
            xpath = ask_ai_for_xpath(driver.page_source[:3000], "username field")
            if xpath:
                print("🤖 AI XPath:", xpath)
                username = driver.find_element(By.XPATH, xpath)
            else:
                print("⚠️ Fallback username locator")
                username = driver.find_element(By.ID, "username")

        username.send_keys("tomsmith")

        # ================= PASSWORD =================
        try:
            password = driver.find_element(By.ID, "wrong-password")
        except NoSuchElementException:
            xpath = ask_ai_for_xpath(driver.page_source[:3000], "password field")
            if xpath:
                print("🤖 AI XPath:", xpath)
                password = driver.find_element(By.XPATH, xpath)
            else:
                print("⚠️ Fallback password locator")
                password = driver.find_element(By.ID, "password")

        password.send_keys("SuperSecretPassword!")

        # ================= LOGIN BUTTON =================
        try:
            driver.find_element(By.XPATH, "//button[@id='wrong-id']").click()
        except NoSuchElementException:
            print("❌ Login button not found. Self-healing...")
            xpath = ask_ai_for_xpath(driver.page_source[:3000], "login button")
            if xpath:
                print("🤖 AI XPath:", xpath)
                driver.find_element(By.XPATH, xpath).click()
            else:
                print("⚠️ Fallback login locator")
                driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(3)

        # ================= VERIFICATION =================
        if "secure" in driver.current_url:
            print("🎉 LOGIN SUCCESS")
        else:
            print("⚠️ Login might have failed")

    finally:
        input("\nPress Enter to close browser...")
        driver.quit()
        print("✅ Test Execution Finished")


# ================= RUN =================
run_test()