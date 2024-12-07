from flask import render_template, request
from app import app
from .capture_qrcode import ConexaoZap
from werkzeug.utils import secure_filename
import shutil
import os
import json

from .fila_memoria import FilaEnvio


UPLOADS_FOLDER = os.path.join(os.getcwd(),'app','uploads')
PROFILES = os.path.join(os.getcwd(),'app','profiles')
IMAGE = os.path.join(os.getcwd(),'app','static','img')

app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
app.config.update()

#driver = None
fila = FilaEnvio()
#fila.start_consumer_thread()


@app.route("/login/<user>")
def login(user):
    global driver
    print('iniciando processo')
    try:
        if not os.path.exists(os.path.join(UPLOADS_FOLDER,user)) and not os.path.exists(os.path.join(PROFILES,user)):
            print("Criando Diretorios")
            os.makedirs(os.path.join(UPLOADS_FOLDER,user))
            os.makedirs(os.path.join(PROFILES,user))
            os.makedirs(os.path.join(IMAGE,user))

        profile = os.path.join(PROFILES,user)
        user_image = f'{user}/qrcode.png'
        driver = ConexaoZap(user=profile)
        fila.start_consumer_thread(driver)
    except Exception as err:
        print(err)
        return "Ocorreu um erro tente novamente"

    if driver.connect_whatsapp(user):
       print('check ok')
       
       #shutil.move(os.path.join(os.getcwd(),'app','profiles','default'), profile)
       return render_template('index.html', image = user_image), export_driver(profile)
    else:
        return "erro"

def export_driver(user):
    ...

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/envio/<numero>&<texto>",methods=['POST'])
def send_message(numero,texto):
    print(f'Envio de mensagem para o numero: {numero}, Adicionado a Fila')
    '''driver.fila.appendleft(['numero',numero,texto])
    print(driver.fila)
    return "Mensagem adicionada a fila de envio"'''
    if driver.envio_mesagem(numero,texto):
        print(f'Mensagem para o numero: {numero} ### Enviado com sucesso ###')
        return "Mensagem Enviada"
    else:
        print(f'Mensagem para o numero: {numero} ##### Falhou #####')
        return "Mensagem não enviada"

@app.route("/enviogrupo/<id_grupo>&<texto>",methods=['POST'])
def send_message_group(id_grupo,texto):
    print(f'Enviando mensagem para o grupo: {id_grupo}')
    '''driver.fila.appendleft(['numero',id_grupo,texto])
    print(driver.fila)
    print(f'Envio de mensagem para o grupo: {id_grupo}, Adicionado a Fila')
    return "Mensagem adicionada a fila de envio"'''

    if driver.envio_mesagem_grupo(id_grupo,texto):
        print(f'Mensagem para o grupo: {id_grupo} ### Enviado com sucesso ###')
        return "Mensagem Enviada"
    else:
        print(f'Mensagem para o grupo: {id_grupo} ##### Falhou #####')
        return "Mensagem não enviada"
    
@app.route("/envio/json/<usuario>",methods=['POST'])
def envio_json(usuario):
    #fila.start_consumer_thread(driver)
    request_mensagem = request.get_json()
    if fila.produce(request_mensagem):
        return 'Mensagem adicionada na fila'
    else:
        return 'Ocorreu um erro'
    if 'numero' in request_mensagem.keys() and "message" in request_mensagem.keys():
        numero = request_mensagem['numero']
        text = request_mensagem['message']
        print(f'Envio para o numero: {numero} adicionado a fila')
        '''driver.fila.appendleft(['numero',numero,text])
        print(driver.fila)
        return "Mensagem adicionada a fila de envio"'''
        if driver.envio_mesagem(numero,text):
            print(f'Mensagem para o numero: {numero} ### Enviado com sucesso ###')
            return "Mensagem Enviada"
        else:
            print(f'Mensagem para o numero: {numero} ##### Falhou #####')
            return "Mensagem não enviada"
    
    elif 'grupo' in request_mensagem.keys() and "message" in request_mensagem.keys():
        grupo = request_mensagem['grupo']
        fila.produce(request_mensagem)

        text = request_mensagem['message']
        '''driver.fila.appendleft(['grupo',grupo,text])
        print(f'Envio de mensagem para o grupo: {grupo}, Adicionado a Fila')
        print(driver.fila)
        return "Mensagem adicionada a fila de envio"'''
        if driver.envio_mesagem_grupo(grupo,text):
            print(f'Mensagem para o grupo: {grupo} ### Enviado com sucesso ###')
            return "Mensagem Enviada"
        else:
            print(f'Mensagem para o grupo: {grupo} ##### Falhou #####')
            return "Mensagem não enviada"
    return "Mensagem não enviada"

@app.route("/envioarquivo/json/<usuario>",methods=['POST'])
def envio_arquivo(usuario):
    request_mensagem = request.form['metadata']
    if 'file' not in request.files:
        return 'Sem arquivo'
    #request_mensagem = request.get_json()
    mensagem = json.loads(request_mensagem)
    file = request.files['file']
    file_name = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],usuario,file_name))
    arquivo = os.path.join(app.config['UPLOAD_FOLDER'],usuario,file_name)
    #print(f'Enviando arquivo {file_name} para o numero: {numero}')
    if file.filename == '':
        return 'Sem arquivo'
    if 'numero' in mensagem.keys():
        print(mensagem['numero'])
        numero = mensagem['numero']
        '''driver.fila.appendleft(['arquivo_numero',arquivo,numero])
        print(f'Envio de arquivo para o numero: {numero}, Adicionado a Fila')
        return "Envio de arquivo adicionado a fila de envio"'''

        if driver.send_archive_numero(arquivo,numero):
        
            return "Arquivo enviado"
        else:
            return "Arquivo não enviado"
        
    if 'grupo' in mensagem.keys():
        print(mensagem['grupo'])
        grupo = mensagem['grupo']
        '''driver.fila.appendleft(['arquivo_grupo',arquivo,numero])
        print(f'Envio de grupo para o grupo: {grupo}, Adicionado a Fila')
        return "Envio de arquivo adicionado a fila de envio"'''

        if driver.send_archive_group(arquivo,grupo):
        
            return "Arquivo enviado"
        else:

            return "Arquivo não enviado"


'''def executar_fila():
    while True:
        if fila'''

if __name__ == "__main__":
    print('ola')