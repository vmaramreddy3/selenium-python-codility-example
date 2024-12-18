from typing import Tuple

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AboutPage(BasePage):
    """About page - The first page that appears when navigating to base URL"""

    LOGIN_LINK: Tuple[str, str] = (By.CSS_SELECTOR, "a[href='https://login.codility.com']")
    FOR_CANDIDATES_LINK: Tuple[str, str] = (By.CSS_SELECTOR, "a[href='https://app.codility.com/programmers']")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Click Login link")
    def click_login_link(self) -> None:
        self.click(self.LOGIN_LINK)

    @allure.step("Click Register link")
    def click_for_candidates_link(self) -> None:
        self.click(self.FOR_CANDIDATES_LINK)
