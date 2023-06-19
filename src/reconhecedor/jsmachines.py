import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.reconhecedor.tabela_analise.acao import Empilhamento, Reducao, Salto, Aceite
from src.reconhecedor.tabela_analise.estado import Estado
from src.reconhecedor.tabela_analise.tabela import TabelaAnalise


def iniciar_chrome() -> WebDriver:
    # Caminho para o executável do ChromeDriver
    servico = Service(r'C:\chromedriver\chromedriver.exe')
    servico.start()

    # Inicia o chrome em background
    opcoes = Options()
    opcoes.add_argument('--headless')

    # Não imprime logs
    opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Abre o chrome
    driver = webdriver.Chrome(
        service=servico,
        options=opcoes
    )

    return driver


def fechar_chrome(driver: WebDriver):
    # Fecha o navegador
    driver.quit()


def abrir_url(driver: WebDriver, url: str):
    # Abre a url especificada
    driver.get(url)


def get_tabela_lr(gramatica_str, recarregar):
    # Se for necessário recarregar a tabela lr, raspa a página jsmachines
    if recarregar:
        tabela_lr = raspar_tabela_lr(gramatica_str)

        # Salva o arquivo a tabela em um pickle em cache
        salvar_cache_tabela_lr('arquivos/cache/estruturas.pkl', tabela_lr)

        return tabela_lr

    # Se não, pega do arquivo pickle em cache
    return get_cache_tabela_lr('arquivos/cache/estruturas.pkl')


def salvar_cache_tabela_lr(path: str, tabela):
    with open(path, 'wb') as file:
        pickle.dump(tabela, file)


def get_cache_tabela_lr(path: str):
    with open(path, 'rb') as file:
        tabela = pickle.load(file)
    return tabela


def raspar_tabela_lr(gramatica_str) -> TabelaAnalise:
    # ABRIR CHROME
    chrome = iniciar_chrome()

    # ABRIR JS MACHINES
    abrir_url(chrome, 'https://jsmachines.sourceforge.net/machines/slr.html')

    # PEGA O CAMPO DAS GRAMÁTICAS
    campo_gramatica = chrome.find_element(
        By.ID,
        'grammar'
    )

    # LIMPA O CAMPO
    chrome.execute_script("arguments[0].value = ''", campo_gramatica)

    # INSERE A GRAMÁTICA
    campo_gramatica.send_keys(gramatica_str)

    time.sleep(1)

    # CLICA NO BOTÃO PARA GERAR A TABELA
    chrome.find_element(
        By.XPATH,
        '//input[@type="button"][@value=">>"]'
    ).click()

    time.sleep(2)

    # PEGA O HTML DA TABELA GERADA
    html_tabela = chrome.find_element(
        By.XPATH,
        '//*[@id="lrTableView"]'
    ).get_attribute('innerHTML')

    # FECHA O CHROME
    fechar_chrome(chrome)

    return TabelaAnalise(
        html_para_estados(html_tabela)
    )


def html_para_estados(html_tabela):
    soup = BeautifulSoup(html_tabela, 'html.parser')
    tabela = soup.find('table')
    linhas = tabela.find_all('tr')

    # Pega os símbolos não terminais do cabeçalho
    nao_terminais = [s.text for s in linhas[2].find_all('th')]

    # Remove a última linha de cabeçalho
    del linhas[:3]

    estados = []

    while linhas:
        cols = linhas[0].find_all('td')
        numero_estado = int(cols[0].text)
        estados.insert(numero_estado, Estado())

        for index, transicao in enumerate(cols[1:]):
            transicao = transicao.text
            if transicao != '\xa0':
                estados[numero_estado].set_acao(
                    nao_terminais[index],
                    Aceite() if 'acc' in transicao else
                    Empilhamento(transicao.replace('s', '')) if 's' in transicao else
                    Reducao(transicao.replace('r', '')) if 'r' in transicao else
                    Salto(transicao)
                )

        del linhas[0]

    return estados
