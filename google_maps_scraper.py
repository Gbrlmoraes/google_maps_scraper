# Bibliotecas

# Automação Web
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Web Scraping e manipulaçâo dos dados
from bs4 import BeautifulSoup
import re
import pandas as pd

# Auxiliares
from time import sleep
from datetime import datetime

class google_maps_scraper():

    # Função construtora
    def __init__(self, locais : list[str]):

        print('Iniciando Scraper...')
        self.__locais = locais


    # Função que clica no botão de ir para as avaliações
    def __clica_avaliacoes(self):
        # Constantes
        ELEM_AVAL = '//span[contains (text(), "avaliações")]'
        ELEM_AVAL_2 = '//*[contains (text(), "Avaliações")]'
        
        try:
            avaliacoes = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_AVAL)))
            avaliacoes = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, ELEM_AVAL)))
            avaliacoes.click()
            sleep(0.5)
        except:
            avaliacoes = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_AVAL_2)))
            avaliacoes = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, ELEM_AVAL_2)))
            avaliacoes.click()
            sleep(0.5)

    # Função para filtrar os comentários mais recentes
    def __filtra_recente(self):
        # Contantes
        ELEM_FILTRO = '//*[contains (text(), "Ordenar")]'
        ELEM_RECENTE = '//*[@id="action-menu"]/div[2]'
        ELEM_FILTRO_2 = '//*[contains (text(), "Mais relevantes")]'
        
        # Tenta clicar no botão de filtro padrão
        try:
            # Clicando no botão de filtro
            filtro = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_FILTRO)))
            filtro.click()
            sleep(0.25)

            # Clicando no botão de mais recente
            recente = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_RECENTE)))
            recente = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, ELEM_RECENTE)))
            recente.click()
            sleep(0.25)
            
        # Se não encontra, tenta clicar no outro tipo de botão
        except:
            try:
                # Clicando no botão de filtro
                filtro = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_FILTRO_2)))
                filtro.click()
                sleep(0.25)

                # Clicando no botão de mais recente
                recente = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_RECENTE)))
                recente = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, ELEM_RECENTE)))
                recente.click()
                sleep(0.25)
            except:
                print('Não foi possível fazer o filtro!')

    # Função que faz o scroll na página
    def __scroll(self):
        # Constantes
        ELEM_SCROLL = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
        
        try:
            scroll = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.XPATH, ELEM_SCROLL)))
            self.__driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                        scroll
                    )
            sleep(0.25)
        except:
            print('Não foi possível fazer o scroll!')

    # Função que inicia o processo
    def coletar(self, quantidade_de_comentarios : int):

        self.__quantidade_de_comentarios = quantidade_de_comentarios
        
        print(f'Horário de início: {datetime.now()}')

        URL_BASE = 'https://www.google.com.br/maps/search/'

        # Lista com os dados coletadost
        dd_notas = []
        dd_palavras = []
        df_comentarios = pd.DataFrame()
        
        # Iniciando webdriver
        self.__driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Percorrendo os locais
        for i in range(len(self.__locais)):

            # Coletando informação do momento da coleta
            now = datetime.now()
            stamp_coleta = now.strftime("%d/%m/%y %H:%M:%S")
            
            local = self.__locais[i]
            print('=' * 25)
            print(local)

            # Entrando na URL de cada local
            self.__driver.get(URL_BASE + local)
            sleep(0.25)

            try:

                try: 
                    # Clicando no botão para ir até as avaliações
                    self.__clica_avaliacoes()

                except:
                    try:
                        soup = BeautifulSoup(self.__driver.page_source, "html5lib")
                        link = soup.find('a', {'aria-label' : re.compile(local)}).get('href')
                        self.__driver.get(link)
                        self.__clica_avaliacoes()

                    except:               
                        print(f'Não foi possível encontrar o local de nome {local}')
                        continue

                # Coletando qtd comentários e avaliação geral do lugar
                sleep(2)
                soup = BeautifulSoup(self.__driver.page_source, "html5lib")
                html_comentarios = soup.find('div', text = re.compile('[0-9]+\.?[0-9]* comentários'))
                qtd_comentarios = str(html_comentarios.contents[0])

                # Tratando comentarios para coletar apenas o valor numerico na forma de "int"
                string_qtd = re.findall('[0-9]+\.?[0-9]*', qtd_comentarios)[0]
                if '.' in string_qtd:
                    string_qtd = string_qtd.replace('.', '')

                qtd_comentarios_num = int(string_qtd)

                html_nota = html_comentarios.find_previous_siblings()[-1]
                nota = html_nota.contents[0]

                dd_notas.append((
                    local,
                    nota,
                    qtd_comentarios_num,
                    stamp_coleta,
                ))

                # Coletando palavras-chave
                for html in soup.find_all(attrs = {'data-tooltip' : re.compile('\w+, mencionado em [0-9]+ avaliações')}):

                    palavra_chave = html.get('data-tooltip').split(',')[0]
                    mencoes_raw = html.get('data-tooltip').split(',')[1]
                    mencoes = mencoes_raw.replace('mencionado em', '').replace('avaliações', '').strip()

                    dd_palavras.append((local,
                                        palavra_chave,
                                        mencoes,
                                        stamp_coleta))

                # Verificando se é necessário coletar comentários
                if self.__quantidade_de_comentarios > 1:

                # Filtrando comentários pelos mais recentes
                    self.__filtra_recente()
                    sleep(1)

                    # Definindo a quantidade de comentários
                    min_comentarios = self.__quantidade_de_comentarios
                    
                    # Verificando se a quantidade de comentarios existentes é suficiente
                    if qtd_comentarios_num < min_comentarios:
                        min_comentarios = qtd_comentarios_num

                    contador = 0
                    qtd_texto = 0
                    lista_qtd = []
                    # Usando scroll na página
                    while qtd_texto < min_comentarios:

                        self.__scroll()

                        # Capturando comentários
                        html = self.__driver.page_source
                        soup = BeautifulSoup(html, "html.parser")

                        comentarios = soup.find_all('span', {'class' : 'wiI7pd'})
                        listas_comentarios = [comentario.contents for comentario in comentarios]

                        # Verificando quantidade de comentarios
                        qtd_texto = sum([len(lista) for lista in listas_comentarios])

                        if qtd_texto in lista_qtd:
                            contador += 1
                            if contador == 10:
                                print('O máximo de avaliações escritas foi coletado!')
                                break
                        else:
                            contador = 0

                        lista_qtd.append(qtd_texto)

                        print(f'qtd comentarios na página (min = {min_comentarios}): {qtd_texto}')

                    # Colocando os comentarios em um dataframe organizado
                    dd_comentarios = [comentario.contents[0] for comentario in comentarios if len(comentario) > 0]

                    df2 = pd.DataFrame({
                        'nome_do_estabelecimento' : local,
                        'comentario' : dd_comentarios,
                        'timestamp_coleta' : stamp_coleta,
                    })

                    df_comentarios = pd.concat([df_comentarios, df2])

                elif self.__quantidade_de_comentarios == 0:
                    df_comentarios = pd.DataFrame()

            except AttributeError as e:
                print(f'Ocorreu um erro em {local}')
                print(e)
                


        # Fechando navegador
        print(f'Coleta finalizada! Fechando navegador... (Horário: {datetime.now()})\n')
        self.__driver.quit()

        # Montando dataframe com as notas e qtd comentários
        df_notas = pd.DataFrame(dd_notas, columns = ['nome_do_estabelecimento',
                                                    'nota', 
                                                    'qtd_comentarios',
                                                    'timestamp_coleta',])
        
        # Montando dataframe com as palavras-chave
        df_palavras = pd.DataFrame(dd_palavras, columns = ['nome_do_estabelecimento',
                                                        'palavra_chave', 
                                                        'mencoes',
                                                        'timestamp_coleta'])
        
        # Salvando dados como um dicionário
        dados = {
            'notas' : df_notas,
            'palavras' : df_palavras,
            'comentarios' : df_comentarios
        }

        print(f'\nHorário de fim: {datetime.now()}')
        return dados