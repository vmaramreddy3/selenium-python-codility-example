import json
import os
import socket

import allure
import pytest
from assertpy import assert_that

from tests.base_test import BaseTest
from utilities.constants import Constants
from utilities.data import Data

users = [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.feature("Login")
@pytest.mark.security
class TestLogin(BaseTest):
    @allure.description("invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    def test_invalid_login(self, email: str, password: str, data: Data):
        self.about_page.click_login_link()
        self.login_page.login(email, password)
        assert_that(self.login_page.get_error_message()).described_as(
            "login error message"
        ).is_equal_to(data.login.error_message)

    @allure.description("Basic sanity")
    @pytest.mark.devRun
    def test_sanity(self, base_url):
        assert_that(self.driver.current_url).described_as("URL").is_equal_to(base_url)

    @allure.description("valid login")
    @allure.title("Login with valid credentials test")
    @allure.tag("Tagged test")
    @pytest.mark.flaky(reruns=1)
    def test_valid_login(self, data: Data):
        self.about_page.set_geo_location(30.3079823, -97.893803)
        self.about_page.click_login_link()
        self.login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        assert_that(self.projects_page.get_title()).described_as(
            "page title"
        ).is_equal_to("codility")

    @allure.description("Check if email and password fields and login button are present on the page.")
    @pytest.mark.run(order=1)
    def test_fields_present(self):
        email_input = self.login_page.get_element_by_id("email-input")
        password_input = self.login_page.get_element_by_id("password-input")
        login_button = self.login_page.get_element_by_id("login-button")
        assert_that(email_input.is_displayed()).described_as("Email input field").is_true()
        assert_that(password_input.is_displayed()).described_as("Password input field").is_true()
        assert_that(login_button.is_displayed()).described_as("Login button").is_true()

    @allure.description("Login with valid credentials.")
    @pytest.mark.run(order=2)
    def test_valid_login(self, data: Data):
        self.login_page.login(data.valid_user.email, data.valid_user.password)
        success_message = self.login_page.get_element_by_css(".message.success").text
        assert_that(success_message).is_equal_to("Welcome to Codility")

    @allure.description("Login with invalid credentials.")
    @pytest.mark.parametrize("email, password", [("unknown@codility.com", "password")])
    @pytest.mark.run(order=3)
    def test_invalid_login(self, email, password, data: Data):
        self.login_page.login(email, password)
        error_message = self.login_page.get_element_by_css(".message.error").text
        assert_that(error_message).is_equal_to(data.login.error_message)

    @allure.description("Check if invalid email format is validated.")
    @pytest.mark.run(order=4)
    def test_invalid_email_format(self, data: Data):
        self.login_page.login("invalidemail", "password")
        validation_message = self.login_page.get_element_by_css(".validation.error").text
        assert_that(validation_message).is_equal_to("Enter a valid email")

    @allure.description("Check if empty credentials display validation errors.")
    @pytest.mark.run(order=5)
    def test_empty_credentials(self):
        self.login_page.login("", "")
        email_error = self.login_page.get_element_by_xpath("//div[contains(text(), 'Email is required')]").text
        password_error = self.login_page.get_element_by_xpath("//div[contains(text(), 'Password is required')]").text
        assert_that(email_error).is_equal_to("Email is required")
        assert_that(password_error).is_equal_to("Password is required")

    @allure.description("Check if login button is disabled when no input is provided.")
    @pytest.mark.run(order=6)
    def test_login_button_disabled_initially(self):
        login_button = self.login_page.get_element_by_id("login-button")
        assert_that(login_button.is_enabled()).is_false()

    @allure.description("Check if the password visibility toggle works correctly.")
    @pytest.mark.run(order=7)
    def test_password_visibility_toggle(self):
        password_input = self.login_page.get_element_by_id("password-input")
        password_input.send_keys("password")
        toggle_button = self.login_page.get_element_by_id("toggle-password-visibility")
        toggle_button.click()
        assert_that(password_input.get_attribute("type")).is_equal_to("text")

    @allure.description("Verify the title of the login page.")
    @pytest.mark.run(order=8)
    def test_page_title(self):
        expected_title = "Login - Codility"
        actual_title = self.driver.title
        assert_that(actual_title).is_equal_to(expected_title)

    @allure.description("Check if the user is redirected after successful login.")
    @pytest.mark.run(order=9)
    def test_redirect_after_login(self, data: Data):
        self.login_page.login(data.valid_user.email, data.valid_user.password)
        assert_that(self.driver.current_url).contains("/dashboard")

    @allure.description("Verify that characters typed in the password field are masked by default.")
    @pytest.mark.run(order=10)
    def test_password_field_character_masking(self):
        password_input = self.login_page.get_element_by_id("password-input")
        password_input.send_keys("password123")
        assert_that(password_input.get_attribute("type")).is_equal_to("password")

    @allure.description("Check if error messages persist after multiple failed login attempts.")
    @pytest.mark.run(order=11)
    def test_error_message_persistence(self, data: Data):
        for _ in range(2):
            self.login_page.login("unknown@codility.com", "wrongpassword")
            error_message = self.login_page.get_element_by_css(".message.error").text
            assert_that(error_message).is_equal_to(data.login.error_message)
            self.login_page.clear_fields()

    @allure.description("Verify that email validation is case-insensitive for invalid emails.")
    @pytest.mark.run(order=12)
    def test_invalid_email_case_insensitivity(self, data: Data):
        self.login_page.login("INVALID@CODILITY.COM", "password")
        error_message = self.login_page.get_element_by_css(".message.error").text
        assert_that(error_message).is_equal_to(data.login.error_message)

    @allure.description("Verify if browser autofill works correctly for the email field.")
    @pytest.mark.run(order=13)
    def test_email_autofill(self):
        email_input = self.login_page.get_element_by_id("email-input")
        self.login_page.set_field_value(email_input, "autofilled@codility.com")
        assert_that(email_input.get_attribute("value")).is_equal_to("autofilled@codility.com")

    @allure.description("Check if clearing the email field removes entered text.")
    @pytest.mark.run(order=14)
    def test_clear_email_field(self):
        email_input = self.login_page.get_element_by_id("email-input")
        email_input.send_keys("login@codility.com")
        self.login_page.clear_element(email_input)
        assert_that(email_input.get_attribute("value")).is_empty()

    @allure.description("Check if the Remember Me checkbox works correctly.")
    @pytest.mark.run(order=15)
    def test_remember_me_functionality(self):
        remember_me_checkbox = self.login_page.get_element_by_id("remember-me")
        assert_that(remember_me_checkbox.is_selected()).is_false()
        remember_me_checkbox.click()
        assert_that(remember_me_checkbox.is_selected()).is_true()

    @allure.description("Check if leading and trailing whitespace in credentials is trimmed.")
    @pytest.mark.run(order=16)
    def test_login_with_whitespace_trimmed(self, data: Data):
        self.login_page.login("  login@codility.com  ", "  password  ")
        success_message = self.login_page.get_element_by_css(".message.success").text
        assert_that(success_message).is_equal_to("Welcome to Codility")

    @allure.description("Check if email field enforces a maximum character limit.")
    @pytest.mark.run(order=17)
    def test_maximum_email_length(self):
        long_email = "a" * 256 + "@example.com"
        email_input = self.login_page.get_element_by_id("email-input")
        email_input.send_keys(long_email)
        actual_value = email_input.get_attribute("value")
        assert_that(len(actual_value)).is_less_than_or_equal_to(255)

    @allure.description("Check if error messages can be dismissed.")
    @pytest.mark.run(order=18)
    def test_error_message_dismissal(self):
        self.login_page.login("unknown@codility.com", "password")
        error_message = self.login_page.get_element_by_css(".message.error")
        assert_that(error_message.is_displayed()).is_true()
        close_button = self.login_page.get_element_by_css(".close-error")
        close_button.click()
        assert_that(error_message.is_displayed()).is_false()

    @allure.description("Check if the user is redirected after a successful login.")
    @pytest.mark.run(order=19)
    def test_redirect_after_login(self, data: Data):
        self.login_page.login(data.valid_user.email, data.valid_user.password)
        self.login_page.wait_for_url_contains("/dashboard")
        assert_that(self.driver.current_url).contains("/dashboard")

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @allure.story("As a user I want to be able to logout after a successful login.")
    def test_logout(self, data: Data):
        """Test case to verify the logout functionality.

        :param data: An instance of the Data dataclass containing test data.
        :type data: Data

        Source:
        - Example attachments from Allure-Pytest GitHub repository: https://github.com/allure-framework/allure-python/tree/master/allure-pytest/examples

        Steps:
        1. Perform a login with valid credentials.
        2. Click on the logout link.
        3. Verify that the page title matches the expected title after logout.

        Attachments:
        - A simple text attachment with masked password and hidden hostname.
        - Example HTML attachment.
        - Example file attachment (dog.png).
        - Example text content attachment.
        - Example CSV content attachment.
        - Example JSON content attachment.
        - Example XML content attachment.
        - Example URI list attachment.

        :return: None
        """
        allure.dynamic.parameter(
            "password", "qwerty", mode=allure.parameter_mode.MASKED
        )
        allure.dynamic.parameter(
            "hostname", socket.gethostname(), mode=allure.parameter_mode.HIDDEN
        )
        allure.attach(
            "<h1>Example html attachment</h1>",
            name="HTML Attachment Example",
            attachment_type=allure.attachment_type.HTML,
        )
        # example of a file attachment
        allure.attach.file(
            Constants.DATA_PATH / "dog.png",
            name="File Attachment Example",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            "Some text content",
            name="Text Attachment Example",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            "first,second,third\none,two,three",
            name="CSV Attachment Example",
            attachment_type=allure.attachment_type.CSV,
        )
        allure.attach(
            json.dumps({"first": 1, "second": 2}, indent=2),
            name="JSON Attachment Example",
            attachment_type=allure.attachment_type.JSON,
        )
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
                <tag>
                     <inside>...</inside>
                 </tag>
             """
        allure.attach(
            xml_content,
            name="XML Attachment Example",
            attachment_type=allure.attachment_type.XML,
        )
        allure.attach(
            "\n".join(
                [
                    "https://github.com/allure-framework",
                    "https://github.com/allure-examples",
                ]
            ),
            name="URI List Attachment Example",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        self.about_page.click_login_link()
        self.login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        self.projects_page.logout()
        assert_that(self.login_page.get_page_title()).described_as(
            "page title"
        ).is_equal_to(data.login.page_title)

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @allure.label("owner", "nir tal")
    @pytest.mark.skip(reason="skip test example")
    def test_skip(self):
        pass
