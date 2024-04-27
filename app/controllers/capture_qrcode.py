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
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from .token import *
import os
import qrcode
import platform

plataforma = platform.system().lower()



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
    WHATSAPP_URL = r'https://web.whatsapp.com'
    CLASSE_QRCODE = "//canvas[@aria-label='Scan me!']"
    CLASSE_SEND = '//button[@aria-label="Enviar"]'
    CLASSE_TEXT_GROUP = '//div[@title="Digite uma mensagem"]'
    TIME_MAX_WAIT = 30
     
    def __init__(self, driver=None):
        if driver is not None:
            self.driver = driver
        self.driver = self.initializer_driver() 
        self.driver.get(self.WHATSAPP_URL)
    
    def wait_for_element(self, selector,max_time=None):
        if max_time is None:
            max_time = self.TIME_MAX_WAIT
        return WebDriverWait(self.driver, max_time).until(
            EC.presence_of_element_located(selector)
        )
    
    def wait_visible_element(self,selector,max_time=None):
        if max_time is None:
            max_time = self.TIME_MAX_WAIT
        return WebDriverWait(self.driver, max_time).until(
            EC.visibility_of_element_located(selector))
    
    def write_text(self,texto):
        ENTER = '\uE007'    # Codigo referente ao enter do teclado
        DELETE = '\uE017'
        CONTROL = '\uE009'
        try:
            ### Realizando loop para escrever letra a letra no zap
            text_input = self.wait_visible_element((By.XPATH, self.CLASSE_TEXT_GROUP))
            for c in texto:
                if len(c) > 1:
                    c = c.lower()
                text_input.send_keys(c)
            
            text_input.send_keys(ENTER)
            return True                       
        except:
            return False

    def connect_whatsapp(self):
        self.driver.get(self.WHATSAPP_URL)
        #sleep(10)

        try:
            ### Extraindo QRCODE para realização de login
            #extrair_qrcode = self.driver.find_element(By.XPATH, CLASSE_QRCODE)
            extrair_qrcode = self.wait_for_element((By.XPATH, self.CLASSE_QRCODE))
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
        url = fr'{self.WHATSAPP_URL}/send?phone={numero}'
        self.driver.get(url)
        #sleep(15)
        write_msg = self.write_text(texto)
        return write_msg
    
    def envio_mesagem_grupo(self,id_grupo,texto):
        ### Acessando o Grupo para envio da mensagem
        url = fr'{self.WHATSAPP_URL}/accept?code={id_grupo}'
        self.driver.get(url)
        #sleep(10)
        write_msg_group = self.write_text(texto)
        return write_msg_group

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
    
