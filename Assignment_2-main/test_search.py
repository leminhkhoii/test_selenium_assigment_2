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

def search_products(driver, search_query):
            # Open the homepage
            driver.get("https://demo.opencart.com/en-gb?route=common/home")
            try:
                # Locate the search input box
                search_box = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.NAME, "search"))
                )

                # Perform a search
                search_box.clear()
                search_box.send_keys(search_query + Keys.RETURN)  # Submit the search

                # Wait for the search results to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "content"))
                )

                # Locate product elements
                products = driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='product-thumb']")

                # List to store product details
                product_details = []

                # Check if products were found
                if not products:
                    print("No products found for the search query.")
                    return product_details  # Return an empty list if no products found

                for product in products:
                    # Extract product details
                    product_name = product.find_element(By.XPATH, ".//h4/a").text
                    product_price = product.find_element(By.XPATH, ".//span[@class='price-new']").text
                    product_link = product.find_element(By.XPATH, ".//h4/a").get_attribute('href')

                    # Store product details in a dictionary
                    product_details.append({
                        "name": product_name,
                        "price": product_price,
                        "link": product_link
                    })

                    # Print product details (optional)
                    print(f"Product Name: {product_name}")
                    print(f"Price: {product_price}")
                    print(f"Link: {product_link}")
                    print("=" * 40)  # Separator for better readability

                return product_details  # Return the list of product details

            except Exception as e:
                print(f"An error occurred: {e}")
                return []  # Return an empty list if an error occurs



def test_search_products(driver):
        existent_keyword = "MacBook"  # Example keyword
        results = search_products(driver, existent_keyword)
        assert len(results) > 0, "No products found for 'MacBook'"


def test_search_with_nonexistent_keyword(driver):
        nonexistent_keyword = "NonExistentProduct123"  # Example nonexistent keyword
        results = search_products(driver, nonexistent_keyword)

        # Verify that no products were found
        assert len(results) == 0, f"Expected no products for '{nonexistent_keyword}', but found some."
        print("Test for nonexistent keyword passed. No products were found.")

def test_search_with_uppercase_keyword(driver):
        uppercase_keyword = "MACBOOK"  # Example uppercase keyword
        results = search_products(driver, uppercase_keyword)

        # Verify that products were found (assuming "MacBook" exists in the catalog)
        assert len(results) > 0, f"Expected products for '{uppercase_keyword}', but none were found."
        print(f"Test for uppercase keyword '{uppercase_keyword}' passed. Products found: {len(results)}.")


def test_search_with_lowercase_keyword(driver):
        lowercase_keyword = "macbook"  # Example lowercase keyword
        results = search_products(driver, lowercase_keyword)

        # Verify that products were found (assuming "MacBook" exists in the catalog)
        assert len(results) > 0, f"Expected products for '{lowercase_keyword}', but none were found."
        print(f"Test for lowercase keyword '{lowercase_keyword}' passed. Products found: {len(results)}.")
        
        
def test_search_with_keyword_containing_special_characters(driver):
        special_characters_keyword = "!@#$%^&*()"  # Example keyword with special characters
        results = search_products(driver, special_characters_keyword)

        # Verify that no products are found for a search with special characters
        assert len(results) == 0, f"Expected no products for '{special_characters_keyword}', but found some."

        print(f"Test for special characters keyword '{special_characters_keyword}' passed. No products found.")

def test_search_with_keyword_surrounded_by_whitespace(driver):
        keyword_with_whitespace = "  MacBook  "  # Example keyword with surrounding whitespace
        results = search_products(driver, keyword_with_whitespace)

        # Verify that products are found for a search with whitespace surrounding the keyword
        assert len(results) > 0, f"Expected to find products for '{keyword_with_whitespace}', but found none."

        print(f"Test for keyword surrounded by whitespace '{keyword_with_whitespace}' passed. Products found.")


def test_search_empty_characters(driver):
        empty_search_query = ""  # Example of an empty search query
        results = search_products(driver, empty_search_query)

        # Verify that no products are found for an empty search
        assert len(results) == 0, f"Expected no products for an empty search, but found {len(results)} products."

        print("Test for empty search characters passed. No products found.")
        
def test_search_special_characters(driver):
        special_character_search_query = "!@#$%^&*()_+"  # Example of special characters
        results = search_products(driver, special_character_search_query)

        # Check if the results are as expected (typically should return no results)
        assert len(results) == 0, f"Expected no products for the special character search, but found {len(results)} products."

        print("Test for special character search passed. No products found.")



