""" This little program runs test with unittest and selenium
    which is a fast and easy way of implementing automated tests."""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path # You can get the latest chromedriver with this module
from time import sleep


class EggTimerPage(object):
    """In this class we keep attributes of the page. On a bigger project we could have pages split into different
        files dedicated to specific methods for each page, but with such a simple site it's not necessary."""

    url = "https://e.ggtimer.com/"
    input_field = 'start_a_timer'
    go_button = 'timergo'
    progress_text = 'progressText'


class EggTimerTests(unittest.TestCase):
    """This is our test case, here we declare the methods that represent each step of our tests.
        The idea being these steps be reusable on different tests.
        Like I said above, on a bigger project it might be more handy to keep the methods on a page
        class specific for the page the method will work, to keep things tidy."""

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # We can simply remove this option to run the browser normally
        self.driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
        self.driver.implicitly_wait(10)

    def go_to_site(self, url):
        self.driver.get(url)

    def set_alarm(self, time):
        self.driver.find_element_by_id(EggTimerPage.input_field).clear()
        self.driver.find_element_by_id(EggTimerPage.input_field).send_keys(time)
        self.driver.find_element_by_id(EggTimerPage.go_button).click()

    def check_alert(self, time):
        alert = WebDriverWait(self.driver, time).until(EC.alert_is_present())
        alert.accept()

    def check_alarm(self):
        text = self.driver.find_element_by_id(EggTimerPage.progress_text).text
        unittest.TestCase.assertEqual(self, text, "Time Expired!", "No Time Expired! displayed")

    """ The first test sets an alarm though the form in the main page,
        then it checks that it actually goes off."""

    def test_basic_alarm(self):
        self.go_to_site(EggTimerPage.url)
        self.set_alarm(3)
        self.check_alert(5)
        self.check_alarm()

    """ This test sets an alarm directly though the url,
        and also checks that it goes off"""

    def test_url_alarm(self):
        self.go_to_site(EggTimerPage.url + '5')
        sleep(5)
        self.check_alarm()

    """Here we check the special alarm 'tabata' using the URL directly as well.
        In this case I've decided to check its attributes on the js code directly."""

    def test_url_tabata(self):
        self.go_to_site(EggTimerPage.url + 'tabata')
        default_text = self.driver.execute_script("return Egg.defaultText")
        sequence = self.driver.execute_script("return Egg.sequence;")

        unittest.TestCase.assertEqual(self, 'Tabata', default_text,
                                      'The default text found on the script isn\'t Tabata!')
        unittest.TestCase.assertEqual(self, len(sequence), 15, 'The sequence should have 15 steps!')

    def tearDown(cls):
        cls.driver.quit()
