class Config:
    BASE_URL = 'base_url'

    CATEGORIES = ['category01', 'category02', 'category03']

    COMPANIES_LIST_HEADER = ['name', 'link']

    DATA_FOLDER_PATH = 'data/'

    DATA_HEADER = ['profile_title', 'address_street', 'address_zip', 'address_city',
                   'address_country', 'contact_email', 'contact_phone', 'website_links']

    PAGE_QUERY_PARAMS = {
        'oid': 0,
        'lang': 0,
        '_start': 0,
        '_rows': 20
    }
