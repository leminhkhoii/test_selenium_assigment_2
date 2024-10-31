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
from selenium.webdriver.support.ui import Select

import pytest
@pytest.mark.usefixtures("driver")  # Sử dụng fixture driver đã định nghĩa


def test_checkout_with_guest_account():
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.maximize_window()

    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=common/home")
        
        # Initialize wait
        wait = WebDriverWait(driver, 20)

        # Step 2: Add a product to the cart (e.g., iPhone)
        iphone_add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='content']//div[2]//button[contains(@onclick, 'cart.add')]")))
        iphone_add_to_cart_button.click()

        # Wait for success message
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        time.sleep(2)  # Add a short delay to let the alert disappear if needed

        # Step 3: Go to the cart
        cart_button = driver.find_element(By.CSS_SELECTOR, "#header-cart > div > button")
        cart_button.click()
        time.sleep(3)  # Wait for the cart to open

        # Step 4: Proceed to checkout
        checkout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))
        checkout_button.click()

        # Step 5: Fill in guest checkout details
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Checkout']")))

        # Fill in personal details
        first_name_input = driver.find_element(By.ID, "input-payment-firstname")
        last_name_input = driver.find_element(By.ID, "input-payment-lastname")
        email_input = driver.find_element(By.ID, "input-payment-email")
        telephone_input = driver.find_element(By.ID, "input-payment-telephone")
        
        # Fill in valid details
        first_name_input.send_keys("John")
        last_name_input.send_keys("Doe")
        email_input.send_keys("john.doe@example.com")
        telephone_input.send_keys("1234567890")

        # Fill in address details
        address_input = driver.find_element(By.ID, "input-payment-address-1")
        city_input = driver.find_element(By.ID, "input-payment-city")
        postcode_input = driver.find_element(By.ID, "input-payment-postcode")
        country_dropdown = driver.find_element(By.ID, "input-payment-country")
        region_dropdown = driver.find_element(By.ID, "input-payment-zone")

        # Fill in valid address
        address_input.send_keys("123 Main St")
        city_input.send_keys("New York")
        postcode_input.send_keys("10001")

        # Select country and region
        driver.execute_script("arguments[0].value='United States';", country_dropdown)
        time.sleep(2)  # Wait for regions to load
        driver.execute_script("arguments[0].value='New York';", region_dropdown)

        # Step 6: Agree to terms and continue
        agree_checkbox = driver.find_element(By.NAME, "agree")
        agree_checkbox.click()
        continue_button = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary")
        continue_button.click()

        # Step 7: Complete order
        confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
        confirm_button.click()

        # Step 8: Verify successful order placement
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Your order has been placed!']")))
        success_message = driver.find_element(By.XPATH, "//h1[text()='Your order has been placed!']")
        assert success_message.is_displayed(), "Order confirmation message is not displayed!"
        print("Test Passed: Order successfully placed as a guest account.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_guest_account_upper_boundary(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=common/home")
        
        # Step 2: Add a product to the cart (e.g., MacBook)
        macbook_add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='content']//div[2]//button[contains(@onclick, 'cart.add')]")))
        macbook_add_to_cart_button.click()

        # Wait for success message
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        time.sleep(2)  # Add a short delay to let the alert disappear if needed

        # Step 3: Go to the cart
        cart_button = driver.find_element(By.CSS_SELECTOR, "#header-cart > div > button")
        cart_button.click()
        time.sleep(3)  # Wait for the cart to open

        # Step 4: Proceed to checkout
        checkout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))
        checkout_button.click()

        # Step 5: Fill in guest checkout details with maximum character lengths
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Checkout']")))

        # Use long strings for each field
        long_first_name = "J" * 32  # Maximum length for first name
        long_last_name = "D" * 32   # Maximum length for last name
        long_email = "johndoe" + ("@" + "example.com") * 4  # Max length for email
        long_telephone = "1" * 15    # Maximum length for telephone
        long_address = "123 Main St " * 5  # Maximum address length
        long_city = "New York City" * 2  # Maximum length for city
        long_postcode = "1000" * 5  # Maximum length for postcode

        first_name_input = driver.find_element(By.ID, "input-payment-firstname")
        last_name_input = driver.find_element(By.ID, "input-payment-lastname")
        email_input = driver.find_element(By.ID, "input-payment-email")
        telephone_input = driver.find_element(By.ID, "input-payment-telephone")
        
        # Fill in valid details with upper boundary lengths
        first_name_input.send_keys(long_first_name)
        last_name_input.send_keys(long_last_name)
        email_input.send_keys(long_email)
        telephone_input.send_keys(long_telephone)

        # Fill in address details
        address_input = driver.find_element(By.ID, "input-payment-address-1")
        city_input = driver.find_element(By.ID, "input-payment-city")
        postcode_input = driver.find_element(By.ID, "input-payment-postcode")
        country_dropdown = driver.find_element(By.ID, "input-payment-country")
        region_dropdown = driver.find_element(By.ID, "input-payment-zone")

        # Fill in valid address
        address_input.send_keys(long_address)
        city_input.send_keys(long_city)
        postcode_input.send_keys(long_postcode)

        # Select country and region
        driver.execute_script("arguments[0].value='United States';", country_dropdown)
        time.sleep(2)  # Wait for regions to load
        driver.execute_script("arguments[0].value='New York';", region_dropdown)

        # Step 6: Agree to terms and continue
        agree_checkbox = driver.find_element(By.NAME, "agree")
        agree_checkbox.click()
        continue_button = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary")
        continue_button.click()

        # Step 7: Verify if an error message appears for invalid input
        error_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert alert-danger')]")))
        assert error_message.is_displayed(), "Error message is not displayed for upper boundary input!"

        print("Test Passed: Error message displayed for upper boundary inputs.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()

def test_guest_account_lower_boundary(driver):
    # Initialize WebDriver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=common/home")
        
        # Step 2: Add a product to the cart (e.g., MacBook)
        macbook_add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='content']//div[2]//button[contains(@onclick, 'cart.add')]")))
        macbook_add_to_cart_button.click()

        # Wait for success message
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        time.sleep(2)  # Add a short delay to let the alert disappear if needed

        # Step 3: Go to the cart
        cart_button = driver.find_element(By.CSS_SELECTOR, "#header-cart > div > button")
        cart_button.click()
        time.sleep(3)  # Wait for the cart to open

        # Step 4: Proceed to checkout
        checkout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))
        checkout_button.click()

        # Step 5: Fill in guest checkout details with minimum character lengths
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Checkout']")))

        # Use minimum strings for each field
        min_first_name = "A"  # Minimum length for first name
        min_last_name = "B"   # Minimum length for last name
        min_email = "a@b.c"   # Minimum valid email format
        min_telephone = "1"    # Minimum length for telephone
        min_address = "A"      # Minimum address length
        min_city = "C"         # Minimum length for city
        min_postcode = "123"   # Minimum length for postcode

        first_name_input = driver.find_element(By.ID, "input-payment-firstname")
        last_name_input = driver.find_element(By.ID, "input-payment-lastname")
        email_input = driver.find_element(By.ID, "input-payment-email")
        telephone_input = driver.find_element(By.ID, "input-payment-telephone")
        
        # Fill in valid details with lower boundary lengths
        first_name_input.send_keys(min_first_name)
        last_name_input.send_keys(min_last_name)
        email_input.send_keys(min_email)
        telephone_input.send_keys(min_telephone)

        # Fill in address details
        address_input = driver.find_element(By.ID, "input-payment-address-1")
        city_input = driver.find_element(By.ID, "input-payment-city")
        postcode_input = driver.find_element(By.ID, "input-payment-postcode")
        country_dropdown = driver.find_element(By.ID, "input-payment-country")
        region_dropdown = driver.find_element(By.ID, "input-payment-zone")

        # Fill in valid address
        address_input.send_keys(min_address)
        city_input.send_keys(min_city)
        postcode_input.send_keys(min_postcode)

        # Select country and region
        driver.execute_script("arguments[0].value='United States';", country_dropdown)
        time.sleep(2)  # Wait for regions to load
        driver.execute_script("arguments[0].value='New York';", region_dropdown)

        # Step 6: Agree to terms and continue
        agree_checkbox = driver.find_element(By.NAME, "agree")
        agree_checkbox.click()
        continue_button = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary")
        continue_button.click()

        # Step 7: Verify if an error message appears for invalid input
        error_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert alert-danger')]")))
        assert error_message.is_displayed(), "Error message is not displayed for lower boundary input!"

        print("Test Passed: Error message displayed for lower boundary inputs.")

    except Exception as e:
        print(f"Test Failed: {e}")

    finally:
        # Close the browser after the test
        driver.quit()