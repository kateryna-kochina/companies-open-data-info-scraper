from config import Config
from scraper.companies_data_scraper import CompaniesDataScraper
from scraper.companies_list_scraper import CompaniesListScraper
from utils.folder_cleaner import clear_folder


def run_web_scraper():
    '''
    Initiates and runs the web scraper.
    '''
    # Initialize instances of the scrapers
    companies_list_scraper = CompaniesListScraper()
    companies_data_scraper = CompaniesDataScraper()

    # Clear data folder before starting
    clear_folder(Config.DATA_FOLDER_PATH)

    # Iterate through categories and scrape data
    for category in Config.CATEGORIES:
        url = '{}{}'.format(Config.BASE_URL, category)
        print('Scraping data from:', url)

        # Run list scraper to get company list
        companies_list_filepath = companies_list_scraper.get_companies_list(url)

        # Run data scraper using the company list file
        companies_data_scraper.run(url, file_path=companies_list_filepath)


if __name__ == '__main__':
    run_web_scraper()
