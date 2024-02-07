import re

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import Config
from utils.csv_manager import CsvManager

from .base_scraper import BaseScraper
from .element_locators import ElementLocators


class CompaniesListScraper(BaseScraper):
    '''
    A scraper for extracting companies list from a web page.
    '''

    def __init__(self):
        '''Initialize the CompaniesListScraper.'''
        super().__init__()

    def get_total_pages_num(self):
        '''
        Get the total number of pages from pagination information.

        Returns:
            The total number of pages.
        '''
        pagination_info = self.driver.find_element(
            *ElementLocators.PAGINATION_INFO_CLASS).text
        pages_info = [int(num) for num in re.findall(r'\d+', pagination_info)]

        total_pages = pages_info[1]

        return total_pages

    def get_page_links(self, url):
        '''
        Get the links to all pages containing company information.

        Args:
            url: The base URL of the companies list page.

        Returns:
            A list of page URLs.
        '''
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                ElementLocators.PAGINATION_INFO_CLASS)
        )
        total_pages = self.get_total_pages_num()

        page_query_params = Config.PAGE_QUERY_PARAMS

        page_links = []

        for page in range(1, total_pages + 1):
            link = f'{url}?'

            page_query_params['_start'] = (page - 1) * 20

            for param, value in page_query_params.items():
                link += f'{param}={value}&'

            link = link.rstrip('&')

            page_links.append(link)

        return page_links

    def scrape_companies_list(self, page_links):
        '''
        Scrape the list of companies from each page.

        Args:
            page_links: A list of page URLs.

        Returns:
            A list of lists, each containing company name and link.
        '''
        companies_list = []

        for page_link in page_links:
            self.open_web_page(page_link)

            result_items = self.driver.find_elements(
                *ElementLocators.RESULT_ITEM_CLASS)

            for item in result_items:
                name = self.get_element_text_or_none(
                    item, ElementLocators.RESULT_ITEM_NAME_CSS)
                link = self.get_element_attribute_or_none(
                    item, ElementLocators.RESULT_ITEM_LINK_CSS)

                companies_list.append([name, link])

        return companies_list

    def save_data_to_csv_file(self, scraped_data, category):
        '''
        Save scraped data to a CSV file.

        Args:
            scraped_data: The data to be saved.
            category: The category of data being saved.

        Returns:
            The path to the saved CSV file.
        '''
        header = Config.COMPANIES_LIST_HEADER
        output_path = f'{Config.DATA_FOLDER_PATH}{category}_companies_list.csv'
        CsvManager.write_to_csv(header, scraped_data, output_path)

        return output_path

    def get_companies_list(self, url):
        '''
        Run the scraper.

        Args:
            url: The URL of the web page to scrape.

        Returns:
            The path to the saved CSV file.
        '''
        self.open_web_page(url)
        page_links = self.get_page_links(url)
        companies_list = self.scrape_companies_list(page_links)
        companies_list_filepath = self.save_data_to_csv_file(
            companies_list, category=url.split('/')[-1].replace('.', '-'))
        self.cleanup()

        return companies_list_filepath
