import socket 
import threading
import configparser
import sys
   

received_messages = []

def workerThread(s, neighbors_ports):
    while True:
        print(f'\nMensagens atuais: {received_messages}')

        print('Aguardando Mensagem...')
        msg = s.recv(1024)
        if not msg: break

        decoded_message = msg.decode('UTF-8').strip()
        print('Mensagem recebida: ', decoded_message)
        
        try:
            has_message = False
            for received_message in received_messages:
                has_message = True if received_message == decoded_message else False 

            if has_message:    
                response = 'Já tenho essa mensagem.'
            else:
                response = 'Não tenho essa mensagem.'
                received_messages.append(decoded_message)

            print(response)
            s.send(response.encode('UTF-8'))  

            if not has_message:
                replicate_thread = threading.Thread(target=clientThread, args=[neighbors_ports, decoded_message, True])
                replicate_thread.start()
        except:
            print('Erro ao responder.')
            
    s.close()


def receiverThread(server_socket, neighbors_ports):
    print('\nThread de recebimento iniciada...')
    
    while True: 
        server_socket.listen()
        
        s, addr = server_socket.accept() 
        print('\nCliente Conectado:', addr[0], ':', addr[1])

        tw = threading.Thread(target=workerThread, args=[s, neighbors_ports])
        tw.start()

  
def clientThread(neighbors_ports, msg=None, break_at_finish=False):
    print('Thread de envio iniciada...')

    while True:
        if not msg:
            msg = input('Envie uma mensagem: ')
            received_messages.append(msg)

        for port in neighbors_ports:
            dest = ('127.0.0.1', int(port))
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)

            try:
                client_socket.connect(dest)
                client_socket.send(msg.encode('UTF-8'))

                response, server = client_socket.recvfrom(1024)
                print(f'Resposta recebida: {response.decode("UTF-8")}')
                
                client_socket.shutdown(socket.SHUT_RDWR)
            except:
                print('Ocorreu um erro...')
            
        msg = None
        if break_at_finish: break


def Main():
    print(' ___ ___  ___ ___   ___   _ _____ ___  ___ \n' 
        + '| __/ _ \| __/ _ \ / __| /_\_   _/ _ \| _ \ \n' 
        + '| _| (_) | _| (_) | (__ / _ \| || (_) |   / \n'
        + '|_| \___/|_| \___/ \___/_/ \_\_| \___/|_|_\ \n')

    # Obtendo configuracao passada por parametro
    config = configparser.RawConfigParser()
    config.read(sys.argv[1])

    print('\n------- Config -------')
    print(f'Id: {config.get("config", "id")}')
    print(f'Nó: {config.get("config", "node")}')
    print(f'Porta: {config.get("config", "port")}')
    print(f'IP: {config.get("config", "ip")}')
    neighbors_ports = [config.get("config", "neighbor1_port"), config.get("config", "neighbor2_port")]

    # Criando socket que estará ouvindo
    host = str(config.get("config", "ip"))
    port = int(config.get("config", "port"))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((host, port))
  
    receiver_thread = threading.Thread(target=receiverThread, args=[server_socket, neighbors_ports])
    receiver_thread.start()

    client_thread = threading.Thread(target=clientThread, args=[neighbors_ports])
    client_thread.start()

if __name__ == '__main__': 
    Main()