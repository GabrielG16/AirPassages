# Imports

from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from datetime import datetime

import time
import pandas as pd

options123 = Options()
optionsGoogle = Options()

optionsGoogle.add_argument('--start-maximized')
# optionsGoogle.add_argument('--headless')
optionsGoogle.add_argument("--remote-debugging-port=9222")
optionsGoogle.add_argument('--no-sandbox')

options123.add_argument('--window-size=(1920,1080)')
# options123.add_argument('--headless')
options123.add_argument("--remote-debugging-port=9222")
options123.add_argument('--no-sandbox')


def realiza_pesquisa_123(cidade_origem, cidade_destino, data_partida, data_retorno):

    navegador = webdriver.Chrome(options=options123)

    navegador.get('https://123milhas.com/')

    time.sleep(3)

    origem = navegador.find_element_by_xpath(
        '//*[@id="__next"]/div/main/div[2]/form/div/div[2]/div[1]/div[1]/div/div[1]/input')
    origem.send_keys(cidade_origem)
    time.sleep(1)
    origem.send_keys(Keys.ENTER)

    destino = navegador.find_element_by_xpath(
        '//*[@id="__next"]/div/main/div[2]/form/div/div[2]/div[1]/div[3]/div/div[1]/input')
    destino.send_keys(cidade_destino)
    time.sleep(1)
    destino.send_keys(Keys.ENTER)

    data_ida = navegador.find_element(by='id', value='datepicker-ida')
    data_ida.send_keys(data_partida)

    data_volta = navegador.find_element(by='id', value='datepicker-volta')
    data_volta.send_keys(data_retorno)

    data_volta.send_keys(Keys.ENTER)

    navegador.switch_to.window(navegador.window_handles[1])
    try:
        WebDriverWait(navegador, timeout=36).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="frmPriceGroup306"]/div[2]/card-header/div/div')))
    except:
        print('Timeout!')
    df = fetch_123(navegador)
    navegador.close()
    return df


def fetch_123(navegador):
    voos = []

    soup = BeautifulSoup(navegador.page_source, 'lxml')

    for item in soup.find_all('div', class_='flight-price-card__grid-box'):

        preco = item.find('div', class_='price-details__item-holder price-details__item-holder--highlighted').find_all('span')[1].text.split()[0]

        # lista de voos de ida
        for ida in item.find_all('div', class_='flight-holder__container')[0].find_all('label',
                                                                                       class_='flight-time-holder flight-time-holder--thin theme-text--body-3 theme-text--fake-black flight-time-itens__label flight-time__flight-search'):
            aero_ida = ida.find('div', class_='flight-time__legs').p.text
            comp_ida = ida.find('label', class_='flight-time__cia-label theme-text--caption-1').text
            horario_ida = ida.find('div', class_='flight-time__legs').span.text.split()[0]
            aero_chegada = ida.find_all('p')[1].text
            duracao = ida.find('div', class_='flight-time__legs').find_all('span')[2].text
            horario_chegada = ida.find('div', class_='flight-time__legs').find_all('span')[3].div.text.split()[0]

            voos.append(['123M', 'IDA', aero_ida, comp_ida, horario_ida, duracao, horario_chegada, aero_chegada, preco])

        # Lista de voos de volta
        for volta in item.find_all('div', class_='flight-holder__container')[1].find_all('label',
                                                                                         class_='flight-time-holder flight-time-holder--thin theme-text--body-3 theme-text--fake-black flight-time-itens__label flight-time__flight-search'):
            comp_volta = volta.find('label', class_='flight-time__cia-label theme-text--caption-1').text
            horario_volta = volta.find('div', class_='flight-time__legs').span.text.split()[0]
            horario_volta_chegada = volta.find_all('div', class_='theme-text--subtitle-1')[1].text.split()[0]
            aero_volta = volta.find('div', class_='flight-time__legs').p.text
            aero_volta_ida = volta.find('div', class_='flight-time__legs').find_all('p')[1].text
            duracao_volta = volta.find('div', class_='flight-time__legs').find_all('span')[2].text

            voos.append(
                ['123M', 'VOLTA', aero_volta_ida, comp_volta, horario_volta, duracao_volta, horario_volta_chegada, aero_volta,
                 preco])
        voos.append(['-', '-', '-', '-', '-', '-', '-', '-'])
    fetch = pd.DataFrame(voos, columns=['src', 'SENTIDO', 'Aero Saída', 'Companhia Saída', 'Hora Saída', 'Duração',
                                        'Horario chegada', 'Aero Chegada', 'Preco'])

    navegador.quit()
    return fetch


def realiza_pesquisa_google(cidade_origem, cidade_destino, data_partida, data_retorno):

    navegador = webdriver.Chrome(options=optionsGoogle)
    navegador.implicitly_wait(5)

    navegador.get('https://www.google.com/travel/flights')
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i6"]/div[1]/div/div/div[1]/div/div/input')))time.sleep(1)

    # ORIGEM
    origem = navegador.find_element_by_tag_name('input')
    origem.clear()
    clicker = navegador.find_element_by_xpath('//*[@id="i15"]/div[1]/div/div/div[1]/div/div')
    clicker.click()
    text_fill = navegador.find_element_by_xpath('//*[@id="i15"]/div[6]/div[2]/div[2]/div[1]/div/input')
    text_fill.send_keys(cidade_origem)  # origem_texto = navegador.find_elements_by_tag_name('input')
    text_fill.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    # DESTINO
    destino = navegador.find_elements_by_tag_name('input')[2]
    destino.clear()
    clicker = navegador.find_element_by_xpath('//*[@id="i15"]/div[4]/div')
    clicker.click()
    text_fill = navegador.find_element_by_xpath('//*[@id="i15"]/div[6]/div[2]/div[2]/div[1]/div/input')
    text_fill.send_keys(cidade_destino)
    time.sleep(1)
    text_fill.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    # DATAS
    fpartida, fretorno = google_ftime(data_partida, data_retorno)

    campo_ida = navegador.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div')
    campo_ida.click()

    # RESET
    WebDriverWait(navegador, timeout=5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ow60"]/div[2]/div/div[2]/div[1]/div[2]/div[2]/button/span')))
    time.sleep(1)
    navegador.find_element_by_xpath('//*[@id="ow60"]/div[2]/div/div[2]/div[1]/div[2]/div[2]/button/span').click()

    # DATA_PARTIDA
    time.sleep(1)
    data_ida = navegador.find_element_by_xpath('//*[@id="ow60"]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input')
    data_ida.send_keys(fpartida)
    time.sleep(0.5)

    # DATA_VOLTA
    data_volta = navegador.find_element_by_xpath('//*[@id="ow60"]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input')
    data_volta.send_keys(fretorno, Keys.ENTER)
    time.sleep(0.5)
    navegador.find_element_by_xpath('//*[@id="ow60"]/div[2]/div/div[3]/div[3]/div/button').click()

    time.sleep(3)

    fetch = fetch_google(navegador)
    navegador.close()

    return fetch


def fetch_google(navegador):
    idas = []
    voltas = []

    soup = BeautifulSoup(navegador.page_source, 'lxml')

    for ida in soup.find('div', class_='VKb8lb H4aYKc').find_all('div', class_='mz0jqb taHBqe Qpcsfe'):

        preco = ida.find('div', class_='BVAVmf tPgKwe').span.text
        hora_partida = ida.find('div', class_='wtdjmc YMlIz ogfYpf tPgKwe').text
        aero_partida = ida.find('div', class_='G2WY5c sSHqwe ogfYpf tPgKwe').text
        hora_chegada = ida.find('div', class_='XWcVob YMlIz ogfYpf tPgKwe').text
        aero_chegada = ida.find('div', class_='c8rWCd sSHqwe ogfYpf tPgKwe').text
        duracao_ida = ida.find('div', class_='hF6lYb sSHqwe ogfYpf tPgKwe').find_all('span')[4].text
        compania_ida = ida.find('div', class_='hF6lYb sSHqwe ogfYpf tPgKwe').find('span', class_='h1fkLb').span.text

        idas.append(['GFlights', 'IDA', aero_partida, compania_ida, hora_partida, duracao_ida, hora_chegada, aero_chegada, preco])

    # MUDAR PARA TELA DE RETORNOS
    navegador.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div/div[1]').click()

    time.sleep(2)
    soup2 = BeautifulSoup(navegador.page_source, 'lxml')

    for volta in soup2.find('div', class_='VKb8lb H4aYKc').find_all('div', class_='mz0jqb taHBqe Qpcsfe'):
        preco = volta.find('div', class_='BVAVmf tPgKwe').span.text
        hora_retorno = volta.find('div', class_='wtdjmc YMlIz ogfYpf tPgKwe').text
        aero_retorno = volta.find('div', class_='G2WY5c sSHqwe ogfYpf tPgKwe').text
        hora_chegada_retorno = volta.find('div', class_='XWcVob YMlIz ogfYpf tPgKwe').text
        aero_chegada_retorno = volta.find('div', class_='c8rWCd sSHqwe ogfYpf tPgKwe').text
        duracao_volta = volta.find('div', class_='hF6lYb sSHqwe ogfYpf tPgKwe').find_all('span')[4].text
        compania_volta = volta.find('div', class_='hF6lYb sSHqwe ogfYpf tPgKwe').find('span', class_='h1fkLb').span.text

        voltas.append(
            ['GFlights', 'VOLTA', aero_retorno, compania_volta, hora_retorno, duracao_volta, hora_chegada_retorno, aero_chegada_retorno, preco])
    columns = ['src', 'SENTIDO', 'Aero Saída', 'Companhia Saída', 'Hora Saída', 'Duração', 'Horario chegada', 'Aero Chegada',
               'Preco']

    return pd.concat([pd.DataFrame(idas, columns=columns), pd.DataFrame(voltas, columns=columns)])


def google_ftime(data_partida, data_retorno):
    datetime_partida = datetime.strptime(data_partida, '%d/%m/%Y')
    fpartida = datetime_partida.strftime('%a, %b %d')

    datetime_retorno = datetime.strptime(data_retorno, '%d/%m/%Y')
    fretorno = datetime_retorno.strftime('%a, %b %d')

    return fpartida, fretorno
