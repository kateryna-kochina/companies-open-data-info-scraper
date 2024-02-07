from selenium.webdriver.common.by import By


class ElementLocators:
    # For company list scraping
    PAGINATION_INFO_CLASS = (By.CLASS_NAME, 'pnb-seo__pagination__info')
    CURRENT_PAGE_CSS = (
        By.CSS_SELECTOR, '#site-wrapper > div.pnb-seo > div:nth-child(2) > div > div > div.pnb-seo__pagination.pnb-seo__pagination--top > ul > li.current')
    NEXT_PAGE_XPATH = (By.XPATH, 'following-sibling::li/a')
    RESULT_ITEM_CLASS = (By.CLASS_NAME, 'pnb-seo__result-item')
    RESULT_ITEM_NAME_CSS = (
        By.CSS_SELECTOR, 'li.pnb-seo__result-item > div.pnb-seo__result-item__main-row > div > h4 > a > span')
    RESULT_ITEM_LINK_CSS = (
        By.CSS_SELECTOR, 'li.pnb-seo__result-item > div.pnb-seo__result-item__main-row > div > h4 > a')

    # For companies data scraping
    COMPANY_DATA_BTN_CSS = (
        By.CSS_SELECTOR, '#finder-profile > div > div > section > div > div > div.profile-grid__content.profile-grid__content--secondary > div.profile__cta-buttons > button > div')
    METABAR_WIDGET_ID = (By.ID, "metabar-widget")
    GRID_ITEM_CSS = (
        By.CSS_SELECTOR, '#site-wrapper > header > div > div > div.grid.page.advert-row-expandable > div')
    PROFILE_TEXT_CLASS = (By.CLASS_NAME, 'profile__text')
    STAND_MAPS_CLASS = (By.CLASS_NAME, 'stand__maps')
    TITLE_BAR_CLASS = (By.CLASS_NAME, 'page-section__title-bar')
    MODAL_PAGE_CSS = (
        By.CSS_SELECTOR, 'body > div.modal-container > div > div.modal-window__inner')
