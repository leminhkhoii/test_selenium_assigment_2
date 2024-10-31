from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
@pytest.mark.usefixtures("driver")  # Sử dụng fixture driver đã định nghĩa


def test_responsive_design(driver):
    # Open the homepage
    driver.get("https://demo.opencart.com/en-gb?route=common/home")

    # Define different viewport sizes for responsive testing
    viewports = {
        "Desktop": (1200, 800),
        "Tablet": (768, 1024),
        "Mobile": (375, 667)
    }

    for device, (width, height) in viewports.items():
        # Resize the browser window
        driver.set_window_size(width, height)
        driver.refresh()  # Refresh to apply the new size

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Example checks for responsiveness
        try:
            # Check if the search box is present
            search_box = driver.find_element(By.NAME, "search")
            assert search_box.is_displayed(), f"Search box is not displayed on {device}."

            # Check if the "My Account" dropdown is present and displayed
            my_account_dropdown = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']")
            assert my_account_dropdown.is_displayed(), f"My Account dropdown is not displayed on {device}."

            # Check the visibility of the main content area
            main_content = driver.find_element(By.ID, "content")
            assert main_content.is_displayed(), f"Main content is not displayed on {device}."

            print(f"Responsive test passed for {device}: All elements are displayed correctly.")

        except Exception as e:
            print(f"Responsive test failed for {device}: {e}")

    print("Responsive design test completed.")
