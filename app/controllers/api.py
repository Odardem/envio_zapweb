from flask import render_template
from .capture_qrcode import ConexaoZap
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from app import app
from flask import request
import platform

#app = Flask(__name__)
WHATSAPP = r'https://web.whatsapp.com'

plataforma = platform.system()
url = WHATSAPP
option = Options()
if plataforma == "Windows":
    teste = r'.\app\profiles'
    option.add_argument('-headless')
    option.add_argument("-profile")
    option.add_argument(teste)
    servico =  FirefoxService(GeckoDriverManager().install())
    driver = ConexaoZap(webdriver.Firefox(service=servico,options=option))
elif  plataforma == "Linux":
    teste = r'app/profiles'
    option.add_argument('-headless')
    option.set_preference('-profile', teste)
    servico =  FirefoxService(executable_path=GeckoDriverManager().install())
    driver = ConexaoZap(webdriver.Firefox(service=servico,options=option))
else:
    print("erro")

@app.route("/login")
def ola():
    print('iniciando processo')
    if driver.connect_whatsapp():
       print('check ok')
       return render_template('index.html')
    else:
        return "erro"
    #return render_template('index.html')

@app.route("/")
def teste():
    return render_template('index.html')

@app.route("/envio/<numero>&<texto>",methods=['POST'])
def envio(numero,texto):
    if driver.envio_mesagem(numero,texto):

        return "Mensagem Enviada"
    else:
        return "Mensagem não enviada"

@app.route("/enviogrupo/<id_grupo>&<texto>",methods=['POST'])
def envio_grupo(id_grupo,texto):
    if driver.envio_mesagem_grupo(id_grupo,texto):
        return "Mensagem Enviada"
    else:
        return "Mensagem não enviada"
    
@app.route("/envio/json/<usuario>",methods=['POST'])
def envio_json(usuario):
    request_mensagem = request.get_json()
    if 'numero' in request_mensagem.keys() and "message" in request_mensagem.keys():
        numero = request_mensagem['numero']
        text = request_mensagem['message']
        print(f'Enviando mensagem para o numero:{numero}')
        if driver.envio_mesagem(numero,text):
             return "Mensagem Enviada"
        else:
            return "Mensagem não enviada"
    elif 'grupo' in request_mensagem.keys() and "message" in request_mensagem.keys():
        grupo = request_mensagem['grupo']
        text = request_mensagem['message']
        print(f'Enviando mensagem para o grupo: {grupo}')
        if driver.envio_mesagem_grupo(grupo,text):
            return "Mensagem Enviada"
        else:
            return "Mensagem não enviada"

    return "Mensagem não enviada"


if __name__ == "__main__":
    print('ola')