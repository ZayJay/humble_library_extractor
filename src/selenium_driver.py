from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class SeleniumDriver:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.humblebundle.com/login')

    def run(self):

        # Cookie Popup
        self.wait_until_element_is_interactable(By.ID, "onetrust-accept-btn-handler", 5)
        cookie_consent_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        self.click_when_interactable(cookie_consent_button)

        # Sign-in
        username_input = self.driver.find_element(By.NAME, "username")
        self.enter_text_when_interactable(username_input, "Zajac.Steven@gmail.com")

        password_input = self.driver.find_element(By.NAME, "password")
        with open(".creds") as f:
            password_text = f.read()
        self.enter_text_when_interactable(password_input, password_text)

        submit_button = self.driver.find_element(By.CLASS_NAME, "flat-cta-button")
        self.click_when_interactable(submit_button)

        # 2FA
        self.wait_until_element_is_interactable(By.CLASS_NAME, "twofactor-form-view", 5)
        verification_code_input = self.driver.find_element(By.CLASS_NAME, "text-input")
        verification_code = input("Enter verification code:")
        self.enter_text_when_interactable(verification_code_input, verification_code)

        button_verify = None
        buttons = self.driver.find_elements(By.TAG_NAME, "button")

        for button in buttons:
            if button.get_attribute("type") == "submit" and button.text == "VERIFY":
                button_verify = button

        if button_verify is not None:
            self.click_when_interactable(button_verify)
        else:
            print("Could not find 'Verify' button!")

        # Purchases tab

        input("Press Enter to continue...")

        self.driver.close()

    def wait_until_element_is_interactable(self, strategy, value, timeout):

        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: self.driver.find_elements(strategy, value))

    def click_when_interactable(self, element):

        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(self.driver, timeout=5, poll_frequency=1.5, ignored_exceptions=errors)
        wait.until(lambda d: element.click() or True)

    def enter_text_when_interactable(self, element, text):

        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(self.driver, timeout=5, poll_frequency=1.5, ignored_exceptions=errors)
        wait.until(lambda d: element.send_keys(text) or True)