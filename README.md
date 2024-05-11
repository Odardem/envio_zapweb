# BrainWhatsapi

Envio de mensagens no Whatsapp web via API. 
Utilizando Waitress para realziar o deploy da aplicação.
Como utilizar acompanhe **[Utilização](#⚙️-utilização)**

## 🚀 Começando

Realize o clone deste projeto, para começar a utiliza-lo!

```
git clone https://github.com/Odardem/envio_zapweb.git
```

### 📋 Pré-requisitos

É necessario realizar a instação do Firefox, na maquina na qual a api for ser utilizada.
Caso utilize Docker o arquivo [Dockerfile](https://github.com/Odardem/envio_zapweb/blob/main/Dockerfile) ja contempla tudo necessario para execução da api.

Depois é so seguir os passos da **[Instalação](#🔧-instalação)**

### 🔧 Instalação

Caso esteja testando não esqueca de criar seu ambiente virtual.

Para instalar utilize o arquivo requirements.txt. 

```
pip install -r  requirements.txt

```

No caso de utilizar o dockerfile contido no projeto as configurações já contemplam todos requisitos necessarios

Dentro do diretorio execute.

```
docker build -t "nome_da_imagem" .
```

## ⚙️ Utilização

Pode ser iniciado diretamente no chamando o arquivo run.py

``` 
python run.py
```

Chamando via wiatress

```
waitress-serve.exe --host=* --port=5000 --no-ipv6 app:app
```

## Consumindo API

A api irá rodar na porta 5000 as solicitações seram um GET e POST

### Conectando ao Web Whatsapp

Utilize o ip do seu servidor ou o localhost.

EX: GET

> http://127.0.0.1:5000/login

Sera exibido o qrcode do whatsapp para conexão

enviado mensagens texto:

http://127.0.0.1:5000/envio/json/usuario



## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Selenium](https://www.selenium.dev) - Utilizado para webscraping e automação web
* [Flask](https://flask.palletsprojects.com/en/3.0.x/) - framework web
* [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) - wsgi deploy flak


## 📌 Versão

Nós usamos [SemVer](http://semver.org/) para controle de versão. Para as versões disponíveis, observe as [tags neste repositório](https://github.com/suas/tags/do/projeto). 

## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Um desenvolvedor** - *Trabalho Inicial* - [umdesenvolvedor](https://github.com/linkParaPerfil)
* **Fulano De Tal** - *Documentação* - [fulanodetal](https://github.com/linkParaPerfil)

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 Expressões de gratidão

* Conte a outras pessoas sobre este projeto 📢;
* Convide alguém da equipe para uma cerveja 🍺;
* Um agradecimento publicamente 🫂;
* etc.


---
⌨️ por [Vinicius Medrado](https://gist.github.com/Odardem) 