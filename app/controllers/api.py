from flask import render_template, request
from app import app
from .capture_qrcode import ConexaoZap


driver = ConexaoZap() 

@app.route("/login")
def login():
    print('iniciando processo')
    if driver.connect_whatsapp():
       print('check ok')
       return render_template('index.html')
    else:
        return "erro"


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/envio/<numero>&<texto>",methods=['POST'])
def send_message(numero,texto):
    if driver.envio_mesagem(numero,texto):

        return "Mensagem Enviada"
    else:
        return "Mensagem não enviada"

@app.route("/enviogrupo/<id_grupo>&<texto>",methods=['POST'])
def send_message_group(id_grupo,texto):
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