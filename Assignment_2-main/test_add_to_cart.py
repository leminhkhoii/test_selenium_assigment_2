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
from selenium.webdriver.common.action_chains import ActionChains

import pytest
@pytest.mark.usefixtures("driver")  # Sử dụng fixture driver đã định nghĩa


def test_add_to_cart():
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Or use the path to ChromeDriver if not in PATH
    driver.set_page_load_timeout(30)
    
    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=common/home")
        driver.maximize_window()
        
        # Step 2: Wait for "Add to Cart" button to be clickable and click it
        wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='content']//div[2]//button[contains(@onclick, 'cart.add')]")))
        
        # Scroll to make sure the button is in view and click it
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
        add_to_cart_button.click()
        
        # Step 3: Wait for and validate success message
        success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        assert "Success" in success_message.text, "Success message did not appear as expected."
        assert "iPhone" in success_message.text, "Product name not found in success message!"
        
        print("Test Passed: Product successfully added to cart.")
    
    except Exception as e:
        print(f"Test Failed: {e}")
    
    finally:
        # Close the browser after test
        driver.quit()

def test_add_two_products_to_cart():
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.maximize_window()

    try:
        # Step 1: Open OpenCart homepage
        driver.get("https://demo.opencart.com/en-gb?route=common/home")

        # Initialize wait
        wait = WebDriverWait(driver, 20)

        # Step 2: Add first product (iPhone)
        iphone_add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='content']//div[2]//button[contains(@onclick, 'cart.add')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iphone_add_to_cart_button)
        iphone_add_to_cart_button.click()
        
        # Wait for success message
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        time.sleep(2)  # Add a short delay to let the alert disappear if needed

        # Step 3: Add second product (MacBook)
        driver.get("https://demo.opencart.com/en-gb/product/macbook")
        macbook_add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", macbook_add_to_cart_button)
        macbook_add_to_cart_button.click()
        
        # Wait for success message
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert > div")))
        time.sleep(2)

        # Step 4: Open the cart and verify both products
        cart_button = driver.find_element(By.CSS_SELECTOR, "#header-cart > div > button")
        cart_button.click()
        time.sleep(3)  # Wait for the cart to open

        # Step 5: Verify the products in the cart
        product_names = driver.find_elements(By.CSS_SELECTOR, "#header-cart ul li table tbody tr td.text-start a")
        actual_product_names = [name.text for name in product_names]

        expected_product_names = ["iPhone", "MacBook"]
        assert sorted(expected_product_names) == sorted(actual_product_names), "Products in the cart do not match expected products."

        print("Test Passed: Both products successfully added to the cart.")
    
    except Exception as e:
        print(f"Test Failed: {e}")
    
    finally:
        # Close the browser after the test
        driver.quit()