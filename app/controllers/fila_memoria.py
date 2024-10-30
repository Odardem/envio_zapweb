'''import threading
import queue
import time

class fila 
# Criando a fila
message_queue = queue.Queue()

# Função que simula o envio de mensagens para a fila (produtor)
def producer():
    for i in range(10):
        message = f"Mensagem {i+1}"
        print(f"Enviando: {message}")
        message_queue.put(message)  # Coloca a mensagem na fila
        time.sleep(1)  # Simula o tempo entre mensagens

# Função que simula o processamento de mensagens da fila (consumidor)
def consumer():
    while True:
        message = message_queue.get()  # Retira a mensagem da fila
        print(f"Processando: {message}")
        time.sleep(2)  # Simula o tempo de processamento
        message_queue.task_done()  # Indica que o processamento foi concluído

# Iniciando o produtor e o consumidor em threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer, daemon=True)  # Daemon para fechar com o programa

producer_thread.start()
consumer_thread.start()

# Aguarda o fim do produtor
producer_thread.join()
message_queue.join()  # Espera até que todas as mensagens sejam processadas
print("Todas as mensagens foram processadas.")'''
import threading
import queue
from time import sleep

class FilaEnvio():
    def __init__(self):
        self.message_queue = queue.Queue()
        self.consumer_started = False

    def produce(self, message):
       
        try:
            self.message_queue.put(message)
            return True
        except Exception as err:
            print(f'ocorreu o erro: {err}')
            return False


    def consume(self,driver):
        while True:
            message = self.message_queue.get()
            print(f"Processando: {message}")
            if 'numero' in message.keys() and "message" in message.keys():
                numero = message['numero']
                text = message['message']
                while True:     
                    if driver.envio_mesagem(numero,text):
                        print(f'Mensagem para o numero: {numero} ### Enviado com sucesso ###')
                        break                        
                    else:
                        print(f'Mensagem para o numero: {numero} ##### Falhou #####')
                    sleep(5)
                               
            elif 'grupo' in message.keys() and "message" in message.keys():
                grupo = message['grupo']
                text = message['message']
                while True:
                    if driver.envio_mesagem_grupo(grupo,text):
                        print(f'Mensagem para o grupo: {grupo} ### Enviado com sucesso ###')
                        break
                    else:
                        print(f'Mensagem para o grupo: {grupo} ##### Falhou #####')
                    sleep(5)

    '''
    def start_producer(self, messages):
        for message in messages:
            self.produce(message)
            time.sleep(1)  # Simula o tempo entre mensagens
    '''

    def start_consumer_thread(self,driver):
        if not self.consumer_started:
            consumer_thread = threading.Thread(target=self.consume, args=(driver,), daemon=True)
            consumer_thread.start()
            self.consumer_started = True
            print("Consumidor iniciado.")
        else:
            print("Consumidor já foi iniciado.")
        '''
        """Inicia o consumidor em uma thread separada."""
        consumer_thread = threading.Thread(target=self.consume(driver), daemon=True)
        consumer_thread.start()
        return consumer_thread
        '''

# Exemplo de uso da classe
if __name__ == "__main__":
    # Instancia a fila de mensagens
    message_queue = MessageQueue()

    # Lista de mensagens para enviar
    messages_to_send = [f"Mensagem {i+1}" for i in range(10)]

    # Inicia o consumidor em uma thread
    message_queue.start_consumer_thread()

    # Inicia o produtor
    message_queue.start_producer(messages_to_send)

    # Aguarda o processamento das mensagens
    message_queue.message_queue.join()
    print("Todas as mensagens foram processadas.")
