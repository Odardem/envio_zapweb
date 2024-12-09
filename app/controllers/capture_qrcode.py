from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import os
import platform
#from .token import *
from time import sleep

plataforma = platform.system().lower()

#os.environ['GH_TOKEN'] = TOKEN

class ConexaoZap():
    WHATSAPP_URL = r'https://web.whatsapp.com'
    CLASSE_QRCODE = '//canvas[contains(@aria-label,"Scan ")]'
    #CLASSE_QRCODE = 'canvas[*="Scan "]'
    #CLASSE_QRCODE = '//canvas[@*="Scan this QR code to link a device!"]'
    CLASSE_SEND = '//button[@*="Enviar"]'
    CLASSE_TEXT_GROUP = '//div[@*="Digite uma mensagem"]'
    CLASSE_ATTACH_MENU = '//div[@*="Anexar"]'
    ATTACH_ARCHIVE = '//input[@*="file"]'
    SEND_ARCHIVE = '//span[@*="send"]'
    TIME_MAX_WAIT = 30
    CLASS_CHATS = '//div[@*="Chats"]'
    
    def __init__(self, user, driver=None):
        if driver is not None:
            self.driver = driver
        self.user = user
        self.driver = self.initializer_driver(self.user) 
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
    
    def wait_for_clickable_element(self, selector,max_time=None):
        if max_time is None:
            max_time = self.TIME_MAX_WAIT
        return WebDriverWait(self.driver, max_time).until(
            EC.element_to_be_clickable(selector)
        )
    
    def write_text(self,texto):
        ENTER = '\uE007'    # Codigo referente ao enter do teclado
        DELETE = '\uE017'
        CONTROL = '\uE051'
        try:
            ### Realizando loop para escrever letra a letra no zap
            text_input = self.wait_visible_element((By.XPATH, self.CLASSE_TEXT_GROUP))
            text_input.send_keys(CONTROL + 'a')
            text_input.send_keys(DELETE)
            for c in texto:
                if len(c) > 1:
                    c = c.lower()
                text_input.send_keys(c)
            #text_input.send_keys(ENTER)
            send_button = self.wait_for_clickable_element((By.XPATH, self.CLASSE_SEND))
            send_button.click()
            return True                       
        except:
            return False
        
    def send_archive_numero(self,file,numero):
        try:
            url = fr'{self.WHATSAPP_URL}/send?phone={numero}'
            self.driver.get(url)
            menu_input_archive = self.wait_for_clickable_element((By.XPATH,self.CLASSE_ATTACH_MENU))
            sleep(5)
            menu_input_archive.click()
            input_archive = self.wait_for_element((By.XPATH,self.ATTACH_ARCHIVE))
            input_archive.send_keys(file)
            send_button = self.wait_for_clickable_element((By.XPATH, self.SEND_ARCHIVE))
            send_button.click()
            return True
        except Exception as err:
            print(f'Deu erro {err}')
            return False
    
    def send_archive_group(self,file,id_grupo):
        try:
            url = fr'{self.WHATSAPP_URL}/accept?code={id_grupo}'
            self.driver.get(url)
            menu_input_archive = self.wait_for_clickable_element((By.XPATH,self.CLASSE_ATTACH_MENU))
            sleep(5)
            menu_input_archive.click()
            input_archive = self.wait_for_element((By.XPATH,self.ATTACH_ARCHIVE))
            input_archive.send_keys(file)
            send_button = self.wait_for_clickable_element((By.XPATH, self.SEND_ARCHIVE))
            send_button.click()
            return True
        except Exception as err:
            print(f'Deu erro {err}')
            return False

    def connect_whatsapp(self, archive=None):
        if archive is None:
            ARQUIVO_QRCODE =  os.path.join(os.getcwd(),'app','static','img','qrcode.png')
        else:
            ARQUIVO_QRCODE =  os.path.join(os.getcwd(),'app','static','img',archive,'qrcode.png')
        self.driver.get(self.WHATSAPP_URL)
        try:
            ### Extraindo QRCODE para realização de login
            extrair_qrcode = self.wait_for_element((By.XPATH, self.CLASSE_QRCODE))
            print(extrair_qrcode)
            valor = extrair_qrcode.screenshot_as_png
            print(ARQUIVO_QRCODE)
            with open(ARQUIVO_QRCODE, "wb") as file:
                file.write(valor)
            return True
        except:
            return False
        
    def envio_mesagem(self,numero,texto):
        ### Acessando o Contato para envio da mensagem
        url = fr'{self.WHATSAPP_URL}/send?phone={numero}'
        self.driver.get(url)
        write_msg = self.write_text(texto)
        return write_msg
    
    def envio_mesagem_grupo(self,id_grupo,texto):
        ### Acessando o Grupo para envio da mensagem
        url = fr'{self.WHATSAPP_URL}/accept?code={id_grupo}'
        self.driver.get(url)
        write_msg_group = self.write_text(texto)
        return write_msg_group

    @classmethod
    def initializer_driver(cls,profile=None):
        option = Options()
        #option.add_argument('-headless')
        option.add_argument("-profile")
        if profile is None:
            profile = os.path.join(os.getcwd(),'app','profiles','default')
        option.add_argument(profile)
        if plataforma == "windows":
            servico =  FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=servico,options=option)
            return driver
        elif plataforma == "linux":
            servico =  FirefoxService(executable_path=GeckoDriverManager().install())
            driver = webdriver.Firefox(service=servico,options=option)
            return driver
        else:
            raise OSError("Sistema operacional não suportado para inicializar o driver.")
        
    def test_connection(self):
        try: 
            sleep(30)
            self.wait_for_element((By.XPATH, self.CLASSE_CHAT))
            self.driver.close()
            return True
        except Exception as err:
            return False
        
    def check_fila(self,fila):
        print('checando fila')
        while True:
            print('checando fila')
            if len(fila) > 0:
                tipo,destino,payload = fila[1]
                print(f'''este é o tipo {tipo},
                    este é o destino {destino},
                    este é o payload {payload}''')
            break
        
       
                

if __name__ == "__main__":

    a = ConexaoZap
    a.connect_whatsapp()
    
