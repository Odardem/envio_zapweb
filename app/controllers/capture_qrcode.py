from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from .token import *
import os
import qrcode
import platform

plataforma = platform.system().lower()

WHATSAPP = r'https://web.whatsapp.com'
CLASSE_QRCODE = "/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas"
if plataforma == "windows":
    #os.op
    ARQUIVO_QRCODE =  r'app\static\img\qrcode.png'
elif  plataforma == "Linux":
    ARQUIVO_QRCODE =  r'app/static/img/qrcode.png'



os.environ['GH_TOKEN'] = TOKEN
'''class Driver():
    
    def drive(usuario=None):   
        
        servico = FirefoxService(GeckoDriverManager().install())
        url = WHATSAPP
        option = Options()
        
        if usuario != None:
            option.add_argument("-profile")
            option.add_argument(usuario)
            driver = webdriver.Firefox(service=servico,options=option)
        else:
            teste = r'.\app\profiles'
            option.add_argument("-profile")
            option.add_argument(teste)
            driver = webdriver.Firefox(service=servico,options=option)
        
        return driver'''
    
class ConexaoZap():
    def __init__(self, driver=None):
        if driver is not None:
            self.driver = driver
        self.driver = self.initializer_driver() 
        self.driver.get(WHATSAPP)
    
    def connect_whatsapp(self):
        ### Conectando ao Wathsapp
        self.driver.get(WHATSAPP)
        sleep(10)

        try:
            ### Extraindo QRCODE para realização de login
            extrair_qrcode = self.driver.find_element(By.XPATH, CLASSE_QRCODE)
            valor = extrair_qrcode.screenshot_as_png
            with open(ARQUIVO_QRCODE, "wb") as file:
                file.write(valor)
            '''gerar_qrcode = qrcode.make(extrair_qrcode.get_attribute('data-ref'))
            gerar_qrcode.save(ARQUIVO_QRCODE)
            save_qrcode = Image.open(ARQUIVO_QRCODE)'''
            return True
        except:
            return False
        
    def envio_mesagem(self,numero,texto):
        ### Acessando o Contato para envio da mensagem
        url = fr'https://web.whatsapp.com/send?phone={numero}&text={texto}'
        self.driver.get(url)
        sleep(10)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
            return True
        except:
            return False
        
    def envio_mesagem_grupo(self,id_grupo,texto):
        ### Acessando o Grupo para envio da mensagem
        url = fr'https://web.whatsapp.com/accept?code={id_grupo}'
        self.driver.get(url)
        sleep(10)
        try:
            ### Realizando loop para escrever letra a letra no zap
            for c in texto:
                if len(c) > 1:
                    c = c.lower()
                self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div').send_keys(c)
            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
            return True
        except:
            return False

    @staticmethod
    def initializer_driver():

        option = Options()
        if plataforma == "windows" or plataforma == "linux":
            #option.add_argument('-headless')
            option.add_argument("-profile")
            profile = os.path.join(os.getcwd(),'app','profiles')
            option.add_argument(profile)
            servico =  FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=servico,options=option)
            return driver
        else:
            raise OSError("Sistema operacional não suportado para inicializar o driver.")
        

if __name__ == "__main__":

    a = ConexaoZap
    a.connect_whatsapp()
    
