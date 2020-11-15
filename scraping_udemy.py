"""
  Este scrip trata-se de um estudo prático sobre Web Scrapping.
  Ele faz a busca por uma palavra específica na plataforma Udemy e coleta alguns dados.
  São eles: título do curso, avaliação, duração, quantidade de alunos e o endereço.
  E, por fim, estrai todas as informações em um arquivo CSV.
"""

### Importando as bibliotecas ###

import requests # Requests HTTP Library
import json # JavaScript Object Notatio used as a lightweight data interchange format
import csv # CSV parsing and writing
import random # Random variable generators
import time # This module provides various functions to manipulate time values.
import re # This module provides regular expression matching operations similar to those found in Perl.
from bs4 import BeautifulSoup
import pandas as pd

headers = { # configuração dos navegadores necessária para acessar a página "meus cursos"
    "Authorization": "COLE AQUI A SUA CHAVE AUTORIZAÇÃO", # chave privada de acesso à API da Udemy
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}

busca = 'android' # palavra pela qual deseja pesquisar cursos
lista_urls = []
counter = 1
exit = 0
qtty = 1000 # serão listados até 1000 cursos

while(1):
  params = (
    ('search', busca),
    ('page', str(counter)),
    ('page_size', '2'),
    ('language', 'pt'),
    ('ratings', 4.5),
    ('sort','highest-rated'),
    )

  resposta = requests.get('https://www.udemy.com/api-2.0/courses/', headers=headers, params=params)
  json_data = json.loads(resposta.text) # carrega todo o resultado em um json

  if "results" in json_data:
      for data in json_data['results']:
        if "/draft/" in data['url']: # guarda as URLs dos cursos
          continue
        lista_urls.append("https://www.udemy.com"+data['url']) # lista dos cursos adquiridos
  counter+=1
  lista_urls = list(dict.fromkeys(lista_urls))
  if exit == len(lista_urls) or exit >= qtty - 20:
    break
  else:
    exit = len(lista_urls)
print("Total de cursos encontrados: ", len(lista_urls))

### Coletando os dados ###

count = 0
dados = []
for endereco in lista_urls:
  sleep_time = random.randint(1, 50)/100
  time.sleep(sleep_time) # tempo de espera
  r = requests.get(endereco) # faz a requisição do HTML da página do curso
  #soup = BeautifulSoup(r.text, 'html.parser')
  soup = BeautifulSoup(r.text.encode("utf-8"), 'html.parser') # organiza o códigoo HTML e converte para a codificação utf8
  titulo = soup.title.text[0:-8] # obtendo o título do curso
  titulo = titulo.replace('"', '') # tratamento do texto do título
  titulo = titulo.replace("'", '')
  titulo = titulo.replace(",", '')
  if titulo == "Online Courses - Anytime, Anywhere":
    titulo = "This is private course"
    duracao=""
    qtdd_alunos=""
    avaliacao=""
    dados.append((titulo, avaliacao, duracao, qtdd_alunos, endereco)) # estruturação da lista
    continue
  try:
    duracao = soup.find_all('span', attrs={'class':'curriculum--content-length--1XzLS'}) # busca a exata divisão <span> que contem o campo horas
    stats = [(i.contents[0], i.contents[1].text) for i in duracao]
    stats=stats[0]
    stats=stats[1]
    stats=stats.replace("\xa0", ' ') # retira possíveis trechos no dado
    stats=stats.replace(" total length", '')
    duracao=stats.replace("Duração total: ", '')
    temp=duracao.split()
    try:
      temp[1].count('m') or temp[1].count('min') 
      temp0 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[0])]
      temp1 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[1])]
      duracao = temp0[0] + round(temp1[0]/60,1)
    except:
      temp[0].count('h') 
      temp0 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[0])]
      duracao = float(temp0[0])
  except:
    try:
      duracao = soup.find('span', attrs={'data-purpose':'video-content-length'}).contents[0] # busca a exata divisão <span> que contem o campo horas
      duracao = str(duracao)
      duracao = duracao.replace(" duracao on-demand video", '')
      duracao = duracao.replace(" horas de vídeo sob demanda", 'h')
      temp=duracao.split()
      try:
        temp[1].count('m') or temp[1].count('min') 
        temp0 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[0])]
        temp1 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[1])]
        duracao = temp0[0] + round(temp1[0]/60,1)
      except:
        temp[0].count('h') 
        temp0 = [int(s) for s in re.findall(r'-?\d+\.?\d*', temp[0])]
        duracao = float(temp0[0])
    except:
      duracao = ""     
  try:
    qtdd_alunos = soup.find('div', attrs={'data-purpose':'enrollment'}).text
    qtdd_alunos = qtdd_alunos.replace("\n", '')[:-7].strip()
    qtdd_alunos = qtdd_alunos.replace(" s", '').strip()
  except:
    qtdd_alunos = "" 
  try:
    avaliacao = soup.find('div', attrs={'class':'rate-count'}).contents[1].find('span').contents[0] # busca o exato campo <div> que contem o campo avaliacao
    avaliacao = avaliacao.replace(",", ".")
  except:
    avaliacao = soup.find('span', attrs={'data-purpose':'rating-number'}).contents[0] # busca o exato campo <span> que contem o campo avaliacao
    avaliacao = avaliacao.replace(",", ".") 
  dados.append((titulo, avaliacao, duracao, qtdd_alunos, endereco)) # carrega os datos nas suas respectivas colunas
  titulo = ""
  duracao=""
  qtdd_alunos=""
  avaliacao=""
  r=""
  count = count + 1
  print("remaining = ", (len(lista_urls) - count)) # cursos que ainda faltam ser coletados
  
### Salvando o arquivo CSV ###

df = pd.DataFrame(records, columns=['titulo', 'avaliacao', 'duracao', 'qtdd_alunos', 'endereco'])
df['avaliacao'] = pd.to_numeric(df['avaliacao'])
df.to_csv('lista_cursos.csv', index=False, encoding='utf-8')