from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}


def interceptor(request):
    request.headers.update(headers)


options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.request_interceptor = interceptor
driver.get('https://www.linkedin.com/jobs/')


email = driver.find_element(By.ID,"session_key")
email.send_keys("kurwablyet25@gmail.com")
password = driver.find_element(By.ID,"session_password")
password.send_keys("LinkedinScraper!")
time.sleep(2)
password.send_keys(Keys.RETURN)


jobs_tab = driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')
jobs_tab.click()

element = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "jobs-search-box-keyword-id-ember21"))
)
search_bar_job = driver.find_element(By.ID,"jobs-search-box-keyword-id-ember21")
search_bar_job.click()
search_bar_job.send_keys("Summer Internship")
time.sleep(1)

search_bar_location = driver.find_element(By.ID,"jobs-search-box-location-id-ember21")
search_bar_location.click()
search_bar_location.send_keys("Türkiye")
time.sleep(2)
search_bar_location.send_keys(Keys.RETURN)
time.sleep(2)

ul_element = driver.find_element(By.CSS_SELECTOR,'ul.scaffold-layout__list-container')
# last_list_item_visible = ul_element.find_elements(By.TAG_NAME,'li')[-1]
all_li_items = ul_element.find_elements(By.TAG_NAME, 'li')
bottom_of_scrollable = driver.find_element(By.CLASS_NAME,'jobs-search-create-alert__bottom')

#scroll to last item
for li in all_li_items:
    driver.execute_script('arguments[0].scrollIntoView(true);', li)
    time.sleep(0.5)
# wait_until_last_job_loaded = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable(bottom_of_scrollable)
# )
driver.execute_script('arguments[0].scrollIntoView(true);', bottom_of_scrollable)
time.sleep(3)
web_elements = driver.find_elements(By.CLASS_NAME,'job-card-container__link')
print(len(web_elements))
keywords_intern = ["intern", "Intern", "Internship"]
links = {}

for element in web_elements:
    print(element.text)

for keyword in keywords_intern:
    for job in web_elements:
        if keyword in job.text:
            links[job.text] = job.get_attribute('href')


print(links)

# enable headless mode in Selenium
# options = Options()
# options.add_argument('--headless=new')
#
# driver = webdriver.Chrome(
#     options=options,
#     # other properties...
# )
