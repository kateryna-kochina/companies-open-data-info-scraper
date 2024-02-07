from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class BaseScraper:
    '''Base class for web scraping.'''

    def __init__(self):
        '''Initialize the web driver.'''
        chrome_options = Options()
        chrome_options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def cleanup(self):
        '''Quit the web driver to clean up resources.'''
        self.driver.quit()

    def open_web_page(self, url):
        '''Open a web page in the web driver.'''
        self.driver.get(url)

    def get_element_attribute_or_none(self, element, locator):
        '''
        Get the attribute value of an element or return None if the element is not found.

        Args:
            element: The parent element to search within.
            locator: The locator strategy and value to find the element.

        Returns:
            The attribute value of the found element, or None if the element is not found.
        '''
        try:
            return element.find_element(*locator).get_attribute('href')
        except NoSuchElementException:
            return None

    def get_element_text_or_none(self, element, locator):
        '''
        Get the text content of an element or return None if the element is not found.

        Args:
            element: The parent element to search within.
            locator: The locator strategy and value to find the element.

        Returns:
            The text content of the found element, or None if the element is not found.
        '''
        try:
            return element.find_element(*locator).text
        except NoSuchElementException:
            return None
