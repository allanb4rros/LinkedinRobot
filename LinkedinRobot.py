from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from openpyxl import Workbook
import requests


def linkedin_jobs(url, url_jobs):

    driver_path = 'C:\\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors') #Ignora erro de certificado
    chrome_options.add_argument('--disable-popup-blocking')  # Desativa o bloqueio de pop-ups
    chrome_options.add_argument('--disable-notifications')  # Desativa o bloqueio de notificações

    driver = webdriver.Chrome(options=chrome_options)

    # Abre a página no navegador
    
    driver.get(url)

    # Identifica input username e password

    username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='session_key']")))
    password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='session_password']")))

    # Envia username e password
    username_input.send_keys("Seu login")
    password_input.send_keys("Sua senha")

    # Identifica botão submit e loga
    login_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    sleep(5)

    # Redirecionada para pagina linkedin jobs

    driver.get(url_jobs)

    # Identifica header para input de vaga
    input_jobs_search = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//header//input")))
    sleep(5)
    # Envia vaga desejada
    input_jobs_search.send_keys("Analista de requisitos") #Vaga que deseja pesquisar 
    sleep(5)
    input_jobs_search.send_keys(Keys.ENTER)
    sleep(5)

    # Identifica lista de resultado pesquisado 
    ul_element = driver.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
    sleep(5)

    # Identifica e interage com botão de time vagas
    timeposted_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='searchFilter_timePostedRange']")))
    timeposted_button.click()
    sleep(5)

    # Seleciona as ultimas 24 horas 
    lasthours = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*/text()[normalize-space(.)='Últimas 24 horas']/parent::*")))
    lasthours.click()
    sleep(5)
    
    # Realiza busca 24 horas 
    lasthoursSearchButton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//fieldset/div[2]/button[2]/span")))
    lasthoursSearchButton.click()

    sleep(5)

    #Função para lidar com scroll das vagas 
    def scroll_list(pixels):
        driver.execute_script(f"arguments[0].scrollTop+={pixels};", ul_element)
        sleep(2)

    links = []

    for _ in range(25):
        scroll_list(200)
        links = driver.find_elements(By.XPATH, "//main//div/div//ul//li//a[@data-control-id]")
        print(len(links))
        if len(links) >= 25:
            print(f"Numero maximo listado de vagas por pagina {len(links)}")
            break
        
        
    spreadsheet = Workbook()

    sheet = spreadsheet.active

    sheet['A1'] = "Nome Vaga"
    sheet['B1'] = "Link Vaga"

    next_line = sheet.max_row + 1

    for link in links:
        text = link.text
        url_link = link.get_attribute("href")
    
    

        sheet[f'A{next_line}'] = text
        sheet[f'B{next_line}'] = url_link
        next_line += 1
        TOKEN = "seu token"
        chat_id = "seu chat id"
        message = f'VAGA:{text}\n{url_link}'
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}" 
        print(requests.get(url).json()) #Envia mensagem telegram 

    spreadsheet.save("vagas_link.xlsx")
    print('Planilha criada')


#Enviando via arquivo

  # a = open('vagas_link.xlsx', 'rb')
  #  send_document = 'https://api.telegram.org/bot' + TOKEN +'/sendDocument?'
    #data = {
     #'chat_id': chat_id,
     #'parse_mode':'HTML',
     #'caption':'Vagas atualizadas'
    #}

   # r = requests.post(send_document, data=data, 
   # files={'document': open('vagas_link.xlsx','rb')}, stream=True)
    #return r.json()


linkedin_jobs("https://www.linkedin.com/", "https://www.linkedin.com/jobs/")

