# 🌎 Google Maps Scraper 
_Extraia dados sobre locais no Google Maps de forma simples_

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=Finalizado&color=GREEN&style=for-the-badge"/>
</p>

## 🎲 Dados Coletáveis
- Nota geral
- Quantidade de comentários total
- Palavras que mais aparecem nos comentários e a quantidade de vezes que aparecem
- Comentários mais recentes

## 🧙‍♂️ Tutorial e Exemplo de uso

### 🛠️ Passo 1:
Baixe o arquivo __google_maps_scraper.py__ e faça a importação do objeto no seu código.
```python
from google_maps_scraper import google_maps_scraper
```

### 🛠️ Passo 2: 
Crie uma variável usando o objeto e passe uma lista de locais que você deseja receber informações.
```python
wizard = google_maps_scraper(['Beach Park', 'Petverso Café'])
```
output:
```
Iniciando Scraper...
```

### 🛠️ Passo 3:
Na sua variável criada passe o comando ".coletar" e diga quantos comentários você deseja coletar. A variável criada vai receber um dicionário com os dados coletados.
- _Você pode passar 0 para pular a etapa de coleta de comentários_
```python
dados = wizard.coletar(5)
```
output:
- _Note que o valor 5 é o mínimo de comentários que serão coletados, isso acontece já que o código coleta uma determinada quantidade de comentários sempre que realiza um scroll na automação, e isso pode resultar em uma quantidade de comentários um pouco maior_
```
Horário de início: 2023-02-27 21:34:30.912689
=========================
Beach Park
qtd comentarios na página (min = 5): 5
=========================
Petverso Café
qtd comentarios na página (min = 5): 7
Coleta finalizada! Fechando navegador... (Horário: 2023-02-27 21:35:12.031818)


Horário de fim: 2023-02-27 21:35:14.171001
```

### 🛠️ Passo 4:
Agora basta ver os dados coletados!
- 📃 Dados de nota geral e quantidade de comentários
```python
print(dados['notas'])
```
output:
```
  nome_do_estabelecimento nota  qtd_comentarios   timestamp_coleta
0              Beach Park  4,5              759  27/02/23 21:34:32
1           Petverso Café  4,4               39  27/02/23 21:35:04
```

- 📃 Dados das palavras com mais menções nos comentários
```python
print(dados['palavras'])
```
output:
```
   nome_do_estabelecimento    palavra_chave mencoes   timestamp_coleta
0               Beach Park            preço      38  27/02/23 21:34:32
1               Beach Park         diversão      13  27/02/23 21:34:32
2               Beach Park  parque aquático       9  27/02/23 21:34:32
3               Beach Park              mar       9  27/02/23 21:34:32
4               Beach Park          salgado       7  27/02/23 21:34:32
5               Beach Park       brinquedos       6  27/02/23 21:34:32
6               Beach Park         crianças       6  27/02/23 21:34:32
7               Beach Park          valores       5  27/02/23 21:34:32
8               Beach Park          serviço       5  27/02/23 21:34:32
9               Beach Park           férias       3  27/02/23 21:34:32
10           Petverso Café         ambiente      11  27/02/23 21:35:04
11           Petverso Café         gatinhos       8  27/02/23 21:35:04
12           Petverso Café            preço       4  27/02/23 21:35:04
13           Petverso Café        decoração       3  27/02/23 21:35:04
14           Petverso Café           espaço       3  27/02/23 21:35:04
15           Petverso Café             bolo       3  27/02/23 21:35:04
```

- 📃 Comentários coletados
```python
print(dados['comentarios'])
```
output:
```
  nome_do_estabelecimento                                         comentario  \
0              Beach Park  Espaço incrível. Conforto nota 10.\nSuper priv...   
1              Beach Park          (Tradução do Google) OK\n\n(Original)\nOk   
2              Beach Park  Maravilhoso! Ambiente a beira da praia, lounge...   
3              Beach Park  Preço salgado e a seleta de frutos do mar R$40...   
4              Beach Park  Excelente opção, atendimento muito bom e tudo ...   
0           Petverso Café  Ambiente massa,comidas maravilhosas e lindos a...   
1           Petverso Café                                Proposta inovadora.   
2           Petverso Café  Levei minha filha que ficou encantada com os g...   
3           Petverso Café              Excelente 👏👏👏. Voltarei e recomendo …   
4           Petverso Café  Fui nesse local para conhecer os gatinhos e ac...   
5           Petverso Café  Ótima comida, e depois de comer você ainda pod...   
6           Petverso Café  Fomos conhecer a cafeteira que tem um espaço r...   

    timestamp_coleta  
0  27/02/23 21:34:32  
1  27/02/23 21:34:32  
2  27/02/23 21:34:32  
3  27/02/23 21:34:32  
4  27/02/23 21:34:32  
0  27/02/23 21:35:04  
1  27/02/23 21:35:04  
2  27/02/23 21:35:04  
3  27/02/23 21:35:04  
4  27/02/23 21:35:04  
5  27/02/23 21:35:04  
6  27/02/23 21:35:04  
```

## 🐍 Como usar o arquivo requirements.txt
Esse arquivo permite que você instale os pacotes necessários para usar o código no seu ambiente, pra isso masta rodar o comando abaixo no seu notebook Jupyter, ou no seu prompt de comando sem o "!".
```
!pip install -r "C:\Caminho\Do\Seu\Arquivo\requirements.txt"
```
