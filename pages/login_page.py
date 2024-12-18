from typing import Tuple

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login Page."""

    COMPANY_EMAIL_FIELD: Tuple[str, str] = (By.CSS_SELECTOR, "input[type=email]")
    CONTINUE_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "button[type=submit]")
    PASSWORD_FIELD: Tuple[str, str] = (By.CSS_SELECTOR, "input[type=password]")
    LOGIN_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "button[type=submit]")
    LOGIN_ERROR_MESSAGE: Tuple[str, str] = (By.CSS_SELECTOR, "p[class*='LoginForm__ErrorMessage'][class$='error']")
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "svg[aria-labelledby='title']")
    FORGOT_PASSWORD_LINK: Tuple[str, str] = (
        By.CSS_SELECTOR,
        "a[href='https://login.codility.com/forgot-password']",
    )
    NEED_HELP_LINK: Tuple[str, str] = (By.CSS_SELECTOR,"a[href='https://support.codility.com/hc/en-us/articles/4403106904599']")
    LOGIN_ARTICLE_LINK: Tuple[str, str] = (By.CSS_SELECTOR,"a[href='https://support.codility.com/hc/en-us/articles/4413298311191-Can-t-log-in-See-what-might-be-the-reason']")
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Log in with username: {username} and password: {password}")
    def login(self, username: str, password: str) -> None:
        self.fill_text(self.COMPANY_EMAIL_FIELD, username)
        self.click(self.CONTINUE_BUTTON)
        self.fill_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        return self.get_text(self.LOGIN_ERROR_MESSAGE)

    @allure.step("Get page title")
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    @allure.step("Click Forgot Password link")
    def click_forgot_password(self) -> None:
        self.click(self.FORGOT_PASSWORD_LINK)
