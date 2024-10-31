import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("driver")  # Sử dụng fixture driver đã định nghĩa
def login(driver):
    # Mở trang đăng nhập
    driver.get("https://demo.opencart.com/index.php?route=account/login")

    # Khởi tạo WebDriverWait với thời gian chờ tối đa
    wait = WebDriverWait(driver, 10)  # Thay đổi 10 thành thời gian chờ tối đa bạn mong muốn

    # Chờ cho trường email có thể nhìn thấy và nhập email
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
    email_field.send_keys("quoctrung87377@gmail.com")

    # Chờ cho trường mật khẩu có thể nhìn thấy và nhập mật khẩu
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
    password_field.send_keys("Nozdormu1#")

    time.sleep(10)  # Chờ trang tải xong

    # Chờ cho nút đăng nhập có thể nhấp được và nhấn
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))
    login_button.click()

    # Chờ cho việc đăng nhập hoàn tất (kiểm tra tiêu đề trang hoặc một phần tử nào đó)
    wait.until(EC.title_contains("My Account"))  # Kiểm tra tiêu đề trang nếu đăng nhập thành công
    
    
    
def test_checkout_valid_info(driver):
    # login
    login(driver)
    # Choose product to add
    driver.get("https://demo.opencart.com/index.php?route=product/product&product_id=43")  
    wait = WebDriverWait(driver, 10)
    
    time.sleep(10)  # wait loading page
    # Add to cart
    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
    add_to_cart_button.click()
    time.sleep(10)  # wait loading page

    # Go to cart
    driver.get("https://demo.opencart.com/index.php?route=checkout/cart")
    
    time.sleep(10)  # wait for update update

    # Chọn nút thanh toán
    checkout_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))
    checkout_button.click()
    
    time.sleep(10)  

    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-firstname"))).send_keys("John")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-lastname"))).send_keys("Doe")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-address-1"))).send_keys("123 Main St")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-city"))).send_keys("New York")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-postcode"))).send_keys("10001")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-country"))).send_keys("United States")
    wait.until(EC.visibility_of_element_located((By.ID, "input-payment-zone"))).send_keys("New York")

    # Choose payment method
    payment_method_radio = wait.until(EC.element_to_be_clickable((By.NAME, "payment_method")))
    payment_method_radio.click()

    # Confirm order
    confirm_order_button = wait.until(EC.element_to_be_clickable((By.ID, "button-confirm")))
    confirm_order_button.click()

    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
    assert "Your order has been placed!" in success_message.text



