import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def start_chrome() -> WebDriver:
    # Path to your ChromeDriver executable
    webdriver_service = Service(r'C:\chromedriver\chromedriver.exe')
    webdriver_service.start()

    # Set up the Selenium driver with CDP enabled
    chrome_options = Options()

    # # Run Chrome in headless mode
    # chrome_options.add_argument('--headless')

    # Launch Chrome browser
    driver = webdriver.Chrome(
        service=webdriver_service,
        options=chrome_options
    )

    return driver


def close_chrome(driver: WebDriver):
    # Close the browser
    driver.quit()


def open_url(driver: WebDriver, url: str):
    # Open the specified URL
    driver.get(url)


def get_lr_table(grammar_str):
    # OPEN CHROME
    chrome = start_chrome()

    # OPEN JS MACHINEScd
    open_url(chrome, 'https://jsmachines.sourceforge.net/machines/slr.html')

    # GET THE GRAMMAR FIELD
    grammar_field = chrome.find_element(
        By.ID,
        'grammar'
    )

    # CLEAR FIELD
    chrome.execute_script("arguments[0].value = ''", grammar_field)

    # INSERT GRAMMAR
    grammar_field.send_keys(grammar_str)

    time.sleep(1)

    # CLICK ON THE BUTTON
    chrome.find_element(
        By.XPATH,
        '//input[@type="button"][@value=">>"]'
    ).click()

    time.sleep(2)

    # GET THE RESULT TABLE
    table_html = chrome.find_element(
        By.XPATH,
        '//*[@id="lrTableView"]'
    ).get_attribute('innerHTML')

    print(translate_table_to_states(table_html))

    time.sleep(200)

    # CLOSE CHROME
    close_chrome(chrome)

    return ''


def translate_table_to_states(table_html):
    soup = BeautifulSoup(table_html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    # Pega os símbolos não terminais do cabeçalho
    nao_terminais = [s.text for s in rows[2].find_all('th')]

    # Remove a última linha de cabeçalho
    del rows[:3]

    states = []

    while rows:
        cols = rows[0].find_all('td')
        numero_estado = int(cols[0].text)
        states.insert(numero_estado, dict())

        for index, transicao in enumerate(cols[1:]):
            if transicao.text != '\xa0':
                nao_terminal = nao_terminais[index]
                states[numero_estado][nao_terminal] = transicao.text

        del rows[0]

    return states
