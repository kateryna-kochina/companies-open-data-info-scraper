import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import Config
from utils.csv_manager import CsvManager

from .base_scraper import BaseScraper
from .element_locators import ElementLocators


class CompaniesDataScraper(BaseScraper):
    '''
    A scraper for extracting detailed data of companies from their individual pages.
    '''

    def __init__(self):
        '''Initialize the CompaniesDataScraper.'''
        super().__init__()

    def wait_for_page_load(self):
        '''Wait for the page to fully load.'''
        # Wait for document.readyState to be complete
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

        # Wait for specific elements to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ElementLocators.METABAR_WIDGET_ID))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ElementLocators.GRID_ITEM_CSS))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ElementLocators.PROFILE_TEXT_CLASS))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ElementLocators.STAND_MAPS_CLASS))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(ElementLocators.TITLE_BAR_CLASS))

        # Wait for jQuery to be loaded
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return (typeof jQuery != 'undefined') && jQuery.active == 0")
        )

        # Wait for all scripts to be completed
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

    def scrape_company_data(self):
        '''
        Scrape data from the company's page.

        Returns:
            HTML content of the modal window.
        '''
        retries = 3
        for _ in range(retries):
            try:
                self.wait_for_page_load()
                time.sleep(2)
                self.driver.execute_script(
                    "window.scrollTo(0, -document.body.scrollHeight);")

                company_data_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(ElementLocators.COMPANY_DATA_BTN_CSS))
                company_data_btn.click()

                modal_window = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(ElementLocators.MODAL_PAGE_CSS))

                html_content = modal_window.get_attribute('innerHTML')

                return html_content

            except TimeoutException:
                print('Timeout occurred. Retrying...')
                continue

            except ElementClickInterceptedException:
                print('Element click intercepted. Retrying...')
                continue

            except Exception as e:
                print(f'An error occurred: {e}')
                break

    def parse_modal_window_data(self, html_content):
        '''
        Parse data from the modal window.

        Args:
            html_content: HTML content of the modal window.

        Returns:
            List containing parsed company data.
        '''
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract profile title
        profile_title_section = soup.find('section', {'id': 'profile-title'})
        try:
            h1_element = profile_title_section.find('h1')
            profile_title = h1_element.text.strip()
        except AttributeError:
            profile_title = None
            print("No <h1> element found inside the section with id 'profile-title'")

        # Extract address details
        address_street = None
        address_zip = None
        address_city = None
        address_country = None
        address_street_tag = soup.find('div', {'class': 'address-street'})
        if address_street_tag:
            address_street = address_street_tag.text.strip()
        address_zip_tag = soup.find('span', {'class': 'address-zip'})
        if address_zip_tag:
            address_zip = address_zip_tag.text.strip()
        address_city_tag = soup.find('span', {'class': 'address-city'})
        if address_city_tag:
            address_city = address_city_tag.text.strip()
        address_country_tag = soup.find('div', {'class': 'address-country'})
        if address_country_tag:
            address_country = address_country_tag.text.strip()

        # Extract contact details
        contact_email = None
        contact_phone = None
        contact_email_tag = soup.find('div', {'class': 'exh-contact-email'})
        if contact_email_tag:
            try:
                contact_email = contact_email_tag.text.split(': ')[1].strip()
            except IndexError:
                print("No email found in 'exh-contact-email' div")
        contact_phone_tag = soup.find('div', {'class': 'exh-contact-phone'})
        if contact_phone_tag:
            try:
                contact_phone = contact_phone_tag.text.split(': ')[1].strip()
            except IndexError:
                print("No phone number found in 'exh-contact-phone' div")

        # Extract all website links
        links = []
        link_list = soup.find('div', {'class': 'link-list'})
        if link_list:
            links = [link['href'] for link in link_list.find_all('a')]

        return [profile_title, address_street, address_zip, address_city,
                address_country, contact_email, contact_phone, [link for link in links]]

    def save_data_to_csv_file(self, scraped_data, category):
        '''
        Save scraped data to a CSV file.

        Args:
            scraped_data: The data to be saved.
            category: The category of data being saved.
        '''
        header = Config.DATA_HEADER
        output_path = f'{Config.DATA_FOLDER_PATH}{category}_companies_data.csv'
        CsvManager.write_to_csv(header, scraped_data, output_path)

    def run(self, url, file_path):
        '''
        Run the scraper.

        Args:
            url: The base URL for company pages.
            file_path: The file path containing company links.
        '''
        file_path = f'{Config.DATA_FOLDER_PATH}{url.split("/")[-1].replace(".", "-")}_companies_list.csv'

        rows = CsvManager.read_csv(file_path)

        for row in rows:
            company_link = row[1]
            self.open_web_page(company_link)

            html_content = self.scrape_company_data()
            company_data = self.parse_modal_window_data(html_content)

            self.save_data_to_csv_file(
                [company_data], category=url.split('/')[-1].replace('.', '-'))

        self.cleanup()
