# Python libs
import sys
from time import strftime, sleep
import argparse
import os

# Custom libs
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 

# Argument parser configuration 
parser = argparse.ArgumentParser(description="Gimme arguments")
parser.add_argument("-u", "--username", help="Librus Synergia username", type=str, required=True)
parser.add_argument("-p", "--password", help="Librus Synergia password", type=str, required=True)
parser.add_argument("-hl", "--headless", help="Start in headless mode", action="store_true", required=False)
parser.add_argument("-v", "--verbose", help="Start in verbose mode", action="store_true", required=False) # debugging mode
args = parser.parse_args()

# Print verbose messages
def verbose(text):
    if args.verbose:
        print("[VERBOSE]" + text)

class Presence():
    def __init__(self):
        self.driver = None
        self.username = args.username
        self.password = args.password
        self.unread_messages = []

    def setup(self):
        options = Options()
        if args.headless:
            options.add_argument("--headless")
            options.add_argument("window-size=1920,1080")
            print("[Setup] Starting in headless mode")
        else:
            options = None
            print("[Setup] Starting in normal mode")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        print("[Setup] Finished")

    def quit(self):
        self.driver.quit()

    def login(self):
        self.driver.get("https://portal.librus.pl/rodzina")
        self.driver.find_element(By.LINK_TEXT, "LIBRUS Synergia").click()
        self.driver.find_element(By.LINK_TEXT, "Zaloguj").click()
        self.driver.switch_to.frame(0)
        print("[Login] Switched to login frame")
        sleep(2)
        self.driver.find_element(By.ID, "Login").click()
        self.driver.find_element(By.ID, "Login").send_keys(self.username) # Send username to input field
        print("[Login] Sending username")
        self.driver.find_element(By.ID, "Pass").click()
        self.driver.find_element(By.ID, "Pass").send_keys(self.password) # Send password to input field
        print("[Login] Sending password")
        self.driver.find_element(By.ID, "LoginBtn").click()
        print("[Login] Finished")

    def check_messages(self):
        count = 0
        self.driver.get("https://synergia.librus.pl/wiadomosci")
        tbody = self.driver.find_elements(By.CSS_SELECTOR,
         "#formWiadomosci > div > div > table > tbody > tr > td:nth-child(2) > table.decorated.stretch > tbody > tr"
         )
        for msg in tbody:
            # Check if message is unread by checking style attribute
            if "font-weight: bold;" in msg.find_element(By.CSS_SELECTOR, "td:nth-child(3)").get_attribute("style"):
                # Add unread messages to array
                self.unread_messages.append(msg.find_element(By.CSS_SELECTOR, "td:nth-child(4) > a").get_attribute("href"))
                count += 1
        print(f"[Check messages] Found {count} unread messages")
        verbose("[Check messages] Unread messages links:\n" + "\n".join(map(str, self.unread_messages)))
        self._read_messages()

    def _read_messages(self):
        for index, message in enumerate(self.unread_messages):
            self.driver.get(message) # Go to message link
            print(f"Reading message {index}")
            verbose(f"Message link is {message}")
            # Save screenshot of message in homepath
            self.driver.save_screenshot(os.path.join(os.environ['HOMEPATH'], f'wiadomosc_librus{strftime("%Y-%m-%d_%H-%M-%S")}.png'))
            self.unread_messages.pop(index) # Remove readed message from array

if __name__ == "__main__":
    presence = Presence()

    try:
        presence.setup()
        presence.login()
        schedule.every(1).minutes.do(presence.check_messages)
        while True:
            verbose("Starting the loop ∞")
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        print("Bye ;)")
    finally:
        presence.quit()
