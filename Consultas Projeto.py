from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import requests

print('•API 1 - consulta de IP')
print('•API 2 - consulta de IP - opção 2')
print('•API 3 - consulta de IP - um pouco mais lental, porém mais precisa')
print('•Opção 4 - Busca por ID da PSN')
print('')

while True:
    try:
        NUM_API = int(input('Qual opção deseja utilizar? +++ [ 1 ] - [ 2 ] - [ 3 ] - [ 4 ] +++'))
        if NUM_API not in range(1, 5):
            print('=+=' * 40)
            print('\033[31mpor favor escolha uma opção válida\033[m')
            print('=+=' * 40)
        else:
            break
    except:
        print('=+=' * 40)
        print('\033[31mpor favor escolha uma opção válida\033[m')
        print('=+=' * 40)

if NUM_API == 1:
    while True:
        try:
            ip = input('digite o endereço de IP para consulta').strip()

            requisição = requests.get(f'http://ip-api.com/json/{ip}')
            dic_requisição = requisição.json()

            pais = dic_requisição['country']
            cidade = dic_requisição['city']
            estado = dic_requisição['regionName']
            break
        except:
            print('\033[31mNão conseguimos obter nenhum resultado!'
                  'Por favor digite um endereço de IP válido\033[m')

    if ip == '':
        print('o IP consultado foi -> \033[32m"IP local"\033[m')
    else:
        print(f'o IP consultado foi -> {ip}')
    print(f'país -> \033[32m {pais} \033[m')
    print(f'estado -> \033[32m{estado} \033[m')
    print(f'a cidade é -> \033[32m{cidade} \033[m<- ou região')

elif NUM_API == 2:
    while True:
        try:
            ip = input('digite o endereço de IP para consulta').strip()

            requisição = requests.get(
                f'https://api.ipgeolocation.io/ipgeo?apiKey=2e247cbb1a7e4ef7abaf8444d83f2e78&ip={ip}')
            dic_requisição = requisição.json()

            pais = dic_requisição['country_name']
            cidade = dic_requisição['city']
            estado = dic_requisição['state_prov']
            break
        except:
            print('\033[31mNão conseguimos obter nenhum resultado!'
                  'Por favor digite um endereço de IP válido\033[m')

    if ip == '':
        print('o IP consultado foi -> \033[32m"IP local"\033[m')
    else:
        print(f'o IP consultado foi -> {ip}')
    print(f'país -> \033[32m {pais} \033[m')
    print(f'estado -> \033[32m{estado} \033[m')
    print(f'a cidade é -> \033[32m{cidade} \033[m<- ou região')

elif NUM_API == 3:
    import re

    service = Service(ChromeDriverManager().install())
    padrao = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$"
    meu_ip = requests.get("https://api.ipify.org/").text

    while True:
        IP = input('digite o IP que deseja buscar')
        if re.search(padrao, IP):
            break
        else:
            print('\033[31mOps! isso não parece um ip válido pra mim, digite novamente\033[m')
    # tratamento de erro para validar se o ip digitado é válido

    print('\033[36mAguarde enquanto buscamos as informações isso pode levar alguns segundos...\033[m')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    navegador = webdriver.Chrome(service=service, options=options)

    navegador.get('https://www.opentracker.net/feature/ip-tracker/')

    navegador.find_element('xpath', '//*[@id="search_ip_value"]').send_keys(IP)
    navegador.find_element('xpath', '//*[@id="search_ip_value"]').send_keys(Keys.RETURN)
    ip_buscado = navegador.find_element('xpath', '//*[@id="search_ip_pix1"]/ul/li[1]/b')

    if ip_buscado == meu_ip:
        print('o ip rastreado foi o seu')

    pais = navegador.find_element('xpath', '//*[@id="search_ip_pix1"]/ul/li[4]')
    estado = navegador.find_element('xpath', '//*[@id="search_ip_pix1"]/ul/li[3]')
    cidade = navegador.find_element('xpath', '//*[@id="search_ip_pix1"]/ul/li[2]/b')

    print(f'o país é -> \033[32m{pais.text[14:]}\033[m')
    print(f'o estado é -> \033[32m{estado.text[13:]}\033[m')
    print(f'a cidade é -> \033[32m{cidade.text}\033[m')

elif NUM_API == 4:
    service = Service(ChromeDriverManager().install())

    while True:
        IDPS4 = input('digite a id que deseja buscar').strip()
        if len(IDPS4) < 3:
            print('\033[31mdigite uma id com mais de 3 caracteres\033[m')
        else:
            break

    print('\033[36mAguarde enquanto buscamos as informações isso pode levar alguns segundos...\033[m')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    navegador = uc.Chrome(service=service, options=options)

    navegador.get('https://xresolver.com/playstation')
    navegador.refresh()
    navegador.fullscreen_window()
    navegador.find_element('name', 'psnUsername').send_keys(IDPS4)
    navegador.find_element('name', 'psnUsername').send_keys(Keys.RETURN)

    while True:
        try:
            mensagem_resposta = navegador.find_element('xpath', '//*[@id="result"]/div/div').text
            break
        except:
            continue

    if mensagem_resposta == "Oh no! Seems like that user was not found in our database. Get OctoSniff to grab anyone's"\
                            " IP on any game/console!":

        print('\033[31mUsuário não encontrado no banco de dados\033[m')

    elif mensagem_resposta == "Voila! Here's the information we found on the requested user.":
        print('Usuário encontrado com sucesso!, aqui estão as principais informações')
        ip = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[3]/td')
        pais = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[9]')
        estado = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[11]')
        cidade = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[8]')
        cep = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[7]')
        provedor_de_internet = navegador.find_element('xpath', '//*[@id="result"]/table/tbody/tr[4]')

        print(f'O ip do usuário é \033[32m{ip.get_attribute("textContent")}\033[m')
        print(f'O país é \033[32m{pais.get_attribute("textContent")[7:]}\033[m')
        print(f'O estado é \033[32m{estado.get_attribute("textContent")[6:]}\033[m')
        print(f'A cidade é \033[32m{cidade.get_attribute("textContent")[4:]}\033[m')
        print(f'O CEP é \033[32m{cep.get_attribute("textContent")[11:]}\033[m')
        print(f'O provedor de internet é \033[32m{provedor_de_internet.get_attribute("textContent")[25:]}\033[m')

    elif mensagem_resposta == "Calm down! You can only resolve 1 user every 30 minutes.":
        print('\033[31mCalma, você só pode fazer uma busca de usuário a cada 30 minutos\033[m')

    else:
        print('\033[31merro\033[31m')
