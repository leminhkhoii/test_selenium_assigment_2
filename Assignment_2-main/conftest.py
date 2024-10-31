import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

@pytest.fixture
def driver():
  driver = webdriver.Chrome()
  driver.maximize_window()
  yield driver
  driver.quit()


# @pytest.fixture
# def driver():
#     options = Options()
#     # WebDriverManager sẽ tự động tải và quản lý phiên bản WebDriver
#     service = Service(EdgeChromiumDriverManager().install())
#     driver = webdriver.Edge(service=service, options=options)
#     yield driver