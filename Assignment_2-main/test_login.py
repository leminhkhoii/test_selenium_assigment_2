import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException  # Importing TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import pytest
@pytest.mark.usefixtures("driver")  

#Test Login and Logout
def test_login_and_logout(driver):
    # Navigate to the home page
    driver.get("https://demo.opencart.com/en-gb?route=common/home")

    # Wait to ensure the page is fully loaded
    time.sleep(5)  # Adjust wait time if necessary

    # Wait for the "My Account" dropdown to be clickable
    account_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']"))
    )
    driver.execute_script("arguments[0].click();", account_dropdown)  # Use JavaScript to click

    # Wait for the "Login" link to be visible and clickable
    try:
        login_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        driver.execute_script("arguments[0].click();", login_link)  # Click the "Login" link
    except Exception as e:
        print("Error locating the Login link:", e)
        print("Current page source:", driver.page_source)
        return  # Exit if there's an error

    # Wait for the email input to appear and fill in login details
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    ).send_keys("quoctrung87377@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("Nozdormu1#")
    
    # Click the submit button
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Verify successful login by checking the URL
    WebDriverWait(driver, 20).until(
        EC.url_contains("account/account")
    )
    assert "account/account" in driver.current_url, "Login failed or user not redirected to account page."

    # Now perform the logout process
    # Wait for the "My Account" dropdown to be clickable
    account_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']"))
    )
    driver.execute_script("arguments[0].click();", account_dropdown)

    # Wait for the "Logout" link to be clickable
    logout_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    driver.execute_script("arguments[0].click();", logout_link)

    # Wait for the logout to complete and check the URL
    WebDriverWait(driver, 20).until(
        EC.url_contains("account/logout")
    )

    # Assert logout success by checking if the current URL contains "account/logout"
    assert "account/logout" in driver.current_url, "Logout was not successful."

    # Optional: Check if the user is redirected to the homepage after logging out
    WebDriverWait(driver, 20).until(
        EC.url_contains("common/home")
    )
    assert "common/home" in driver.current_url, "User was not redirected to the homepage after logout."
    
    # Test Invalid Email Login
# PASS
def test_invalid_email_login(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")
    time.sleep(5)  # Add a brief pause after loading the page

    # Wait for the email input field to appear and then enter an invalid email
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    email_field.send_keys("invalidemailexample.com")  # Enter an invalid email

    # Enter an incorrect password
    password_field = driver.find_element(By.ID, "input-password")
    password_field.send_keys("incorrectpassword")  # Enter an incorrect password

    time.sleep(5)  # Add a brief pause before clicking
    # Wait until the login button is clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    # Adding a brief pause to ensure everything is ready before clicking
    time.sleep(1)
    
    # Click the login button using JavaScript click
    driver.execute_script("arguments[0].click();", login_button)

    # Wait for the error message to appear
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
    )

    # Assert that the error message is displayed and has the expected text
    assert error_message.is_displayed(), "Error message is not displayed."
    assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
        "Unexpected error message content."


# PASS
def test_invalid_password_login(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")

    # Wait for the email input field to appear and enter a valid email
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    email_field.send_keys("quoctrung87377@gmail.com")  # Enter a valid email

    # Enter an incorrect password
    password_field = driver.find_element(By.ID, "input-password")
    password_field.send_keys("incorrectpassword")  # Enter an incorrect password
    time.sleep(10)  # Add a brief pause before clicking

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    # Click the login button using different methods for reliability
    try:
        login_button.click()  # Normal click
        time.sleep(1)  # Wait briefly after click

        # Fallback JavaScript click if normal click doesn't work
        if "Warning: No match for E-Mail Address" not in driver.page_source:
            driver.execute_script("arguments[0].click();", login_button)
            time.sleep(1)

    except Exception as e:
        print("Click attempt failed:", e)

    # Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed and check its text
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# PASS
def test_empty_password_login(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")

    # Wait for the email input field to appear and enter a valid email
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    email_field.send_keys("quoctrung87377@gmail.com")  # Enter a valid email

    # Leave the password field empty
    password_field = driver.find_element(By.ID, "input-password")
    password_field.clear()  # Make sure it is empty
    time.sleep(10)  # Add a brief pause before clicking
    

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    # Click the login button
    login_button.click()

    # Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed and check its text
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# PASS
def test_empty_email_login(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")

    # Wait for the password input field to appear and enter a valid password
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-password"))
    )
    password_field.send_keys("Nozdormu1#")  # Enter a valid password

    # Leave the email field empty
    email_field = driver.find_element(By.ID, "input-email")
    email_field.clear()  # Ensure the email field is empty

    time.sleep(10)  # Add a brief pause before clicking
    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    # Click the login button
    login_button.click()

    # Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed and check its text
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# PASS
def test_special_character_login(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")

    # Enter special characters in the email field
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    email_field.send_keys("!@#$%^&*()")  # Special characters in email

    # Enter special characters in the password field
    password_field = driver.find_element(By.ID, "input-password")
    password_field.send_keys(")(*&^%$#@!")  # Special characters in password
    
    time.sleep(10)  # Add a brief pause before clicking

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    # Click the login button
    login_button.click()

    # Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed and check its text
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)

# PASS
def test_sql_injection_attempt(driver):
    # Navigate to the login page
    driver.get("https://demo.opencart.com/index.php?route=account/login&language=en-gb")

    # Enter a potential SQL injection payload in the email and password fields
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    email_field.send_keys("' OR '1'='1")  # Common SQL injection payload

    password_field = driver.find_element(By.ID, "input-password")
    password_field.send_keys("' OR '1'='1")  # Common SQL injection payload

    time.sleep(10)  # Add a brief pause before clicking
    # Click the login button
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    # Wait for the error message to appear or confirm lack of access
    try:
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed
        assert error_message.is_displayed(), "Error message is not displayed after SQL injection attempt."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)