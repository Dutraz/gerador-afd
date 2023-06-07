import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.reconhecedor.tabela_analise.estado import Estado
from src.reconhecedor.tabela_analise.tabela import TabelaAnalise


def start_chrome() -> WebDriver:
    # Path to your ChromeDriver executable
    webdriver_service = Service(r'C:\chromedriver\chromedriver.exe')
    webdriver_service.start()

    # Set up the Selenium driver with CDP enabled
    chrome_options = Options()

    # Run Chrome in headless mode
    chrome_options.add_argument('--headless')

    # Dont print logs
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

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

    # CLOSE CHROME
    close_chrome(chrome)

    return TabelaAnalise(
        html_para_estados(table_html)
    )


def html_para_estados(table_html):
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
        states.insert(numero_estado, Estado())

        for index, transicao in enumerate(cols[1:]):
            if transicao.text != '\xa0':
                states[numero_estado].set_acao(
                    nao_terminais[index],
                    transicao.text
                )

        del rows[0]

    return states
