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
@pytest.mark.usefixtures("driver")  # Sử dụng fixture driver đã định nghĩa



def test_register_valid_data(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Fill in the registration form with valid data
        first_name = "John"
        last_name = "Doe"
        email = "johndoe@example.com"  # Use a unique email for each test run
        telephone = "1234567890"
        password = "SecurePassword123"
        confirm_password = "SecurePassword123"

        # Fill in the registration fields
        wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys(first_name)
        wait.until(EC.visibility_of_element_located((By.ID, "input-lastname"))).send_keys(last_name)
        wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
        wait.until(EC.visibility_of_element_located((By.ID, "input-telephone"))).send_keys(telephone)
        wait.until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys(password)
        wait.until(EC.visibility_of_element_located((By.ID, "input-confirm"))).send_keys(confirm_password)

        # Step 3: Agree to the Privacy Policy
        agree_checkbox = wait.until(EC.element_to_be_clickable((By.NAME, "agree")))
        agree_checkbox.click()

        # Step 4: Submit the registration form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()

        # Step 5: Wait for the success message and verify registration
        success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
        assert "Your Account Has Been Created!" in success_message.text, "Registration failed!"

        print("Test Passed: Registration successful with valid data.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_register_empty_required_input(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart registration page
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Leave required fields empty and try to submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()  # Attempt to submit the form without filling in required fields

        # Step 3: Verify that appropriate error messages are displayed for required fields
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger")
        
        assert "First Name must be between 1 and 32 characters!" in error_message.text, "Error message for First Name is not displayed!"
        assert "Last Name must be between 1 and 32 characters!" in error_message.text, "Error message for Last Name is not displayed!"
        assert "E-Mail Address does not appear to be valid!" in error_message.text, "Error message for Email is not displayed!"
        assert "Telephone must be between 3 and 32 characters!" in error_message.text, "Error message for Telephone is not displayed!"
        assert "Password must be between 4 and 20 characters!" in error_message.text, "Error message for Password is not displayed!"
        assert "Password confirmation does not match password!" in error_message.text, "Error message for Password confirmation is not displayed!"

        print("Test Passed: Appropriate error messages displayed for empty required fields.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_register_invalid_email(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart registration page
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Fill in the registration form with invalid email
        wait.until(EC.visibility_of_element_located((By.NAME, "firstname"))).send_keys("John")
        wait.until(EC.visibility_of_element_located((By.NAME, "lastname"))).send_keys("Doe")
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("invalid-email")  # Invalid email
        wait.until(EC.visibility_of_element_located((By.NAME, "telephone"))).send_keys("1234567890")
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Password123")
        wait.until(EC.visibility_of_element_located((By.NAME, "confirm"))).send_keys("Password123")

        # Step 3: Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()

        # Step 4: Verify that the appropriate error message is displayed
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger")

        assert "E-Mail Address does not appear to be valid!" in error_message.text, "Error message for invalid email is not displayed!"

        print("Test Passed: Appropriate error message displayed for invalid email.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_register_lower_boundary(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart registration page
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Fill in the registration form with lower boundary data
        wait.until(EC.visibility_of_element_located((By.NAME, "firstname"))).send_keys("A")  # Minimum valid first name
        wait.until(EC.visibility_of_element_located((By.NAME, "lastname"))).send_keys("B")  # Minimum valid last name
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@example.com")  # Valid email
        wait.until(EC.visibility_of_element_located((By.NAME, "telephone"))).send_keys("1234567890")  # Valid phone number
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Password123")  # Valid password
        wait.until(EC.visibility_of_element_located((By.NAME, "confirm"))).send_keys("Password123")  # Confirm password

        # Step 3: Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()

        # Step 4: Verify that the registration is successful
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
        success_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-success")

        assert "Your Account Has Been Created!" in success_message.text, "Registration was not successful with lower boundary input!"

        print("Test Passed: Registration successful with lower boundary input.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_register_above_upper_boundary(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart registration page
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Fill in the registration form with above upper boundary data
        long_first_name = "A" * 33  # 33 characters for first name
        long_last_name = "B" * 33  # 33 characters for last name
        
        wait.until(EC.visibility_of_element_located((By.NAME, "firstname"))).send_keys(long_first_name)
        wait.until(EC.visibility_of_element_located((By.NAME, "lastname"))).send_keys(long_last_name)
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@example.com")  # Valid email
        wait.until(EC.visibility_of_element_located((By.NAME, "telephone"))).send_keys("1234567890")  # Valid phone number
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Password123")  # Valid password
        wait.until(EC.visibility_of_element_located((By.NAME, "confirm"))).send_keys("Password123")  # Confirm password

        # Step 3: Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()

        # Step 4: Verify that the appropriate error message is displayed
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger")

        assert "First Name must be between 1 and 32 characters!" in error_message.text or \
               "Last Name must be between 1 and 32 characters!" in error_message.text, "No error message displayed for above upper boundary input!"

        print("Test Passed: Error message displayed for above upper boundary input.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_register_special_characters_in_name(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart registration page
        driver.get("https://demo.opencart.com/en-gb?route=account/register")

        # Step 2: Fill in the registration form with special characters
        special_first_name = "John@Doe#"
        special_last_name = "Smith$%"

        wait.until(EC.visibility_of_element_located((By.NAME, "firstname"))).send_keys(special_first_name)
        wait.until(EC.visibility_of_element_located((By.NAME, "lastname"))).send_keys(special_last_name)
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@example.com")  # Valid email
        wait.until(EC.visibility_of_element_located((By.NAME, "telephone"))).send_keys("1234567890")  # Valid phone number
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Password123")  # Valid password
        wait.until(EC.visibility_of_element_located((By.NAME, "confirm"))).send_keys("Password123")  # Confirm password

        # Step 3: Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        submit_button.click()

        # Step 4: Verify that the appropriate error message is displayed
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger")

        assert "First Name must be between 1 and 32 characters!" in error_message.text or \
               "Last Name must be between 1 and 32 characters!" in error_message.text or \
               "First Name must not contain special characters!" in error_message.text or \
               "Last Name must not contain special characters!" in error_message.text, "No error message displayed for special characters in name!"

        print("Test Passed: Error message displayed for special characters in name.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()