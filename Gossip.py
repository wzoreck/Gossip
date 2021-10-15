import socket 
import threading
import configparser
import sys
   

received_messages = []

def workerThread(s):
    while True:
        print(f'\nMensagens atuais: {received_messages}')

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
                received_messages.append(decoded_message)
                response = 'Não tenho essa mensagem.'

            print(response)
            s.send(response.encode('UTF-8'))  
        except:
            print('Erro ao responder.')
            
    s.close()


def receiverThread(server_socket):
    print('\nThread de recebimento iniciada...')
    
    while True: 
        server_socket.listen()
        
        s, addr = server_socket.accept() 
        print('\nCliente Conectado:', addr[0], ':', addr[1])

        tw = threading.Thread(target=workerThread, args=[s])
        tw.start()

  
def client_thread(neighbors_ports, socket_port=None):
    print('Thread de envio iniciada...')

    while True:
        msg = input('Envie uma mensagem: ')
        received_messages.append(msg)

        for port in neighbors_ports:
            dest = ('127.0.0.1', int(port))
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect(dest)
            client_socket.send(msg.encode('UTF-8'))

            try:
                response, server = client_socket.recvfrom(1024)
                print(f'Resposta recebida: {response.decode("UTF-8")}')
            except:
                print('Ocorreu um erro...')
            
            client_socket.shutdown(socket.SHUT_RDWR)


def Main(): 
    print('\n')
    print('███████╗ ██████╗ ███████╗ ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗ ')
    print('██╔════╝██╔═══██╗██╔════╝██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗')
    print('█████╗  ██║   ██║█████╗  ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝')
    print('██╔══╝  ██║   ██║██╔══╝  ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗')
    print('██║     ╚██████╔╝██║     ╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║')
    print('╚═╝      ╚═════╝ ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝')

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
  
    receiver_thread = threading.Thread(target=receiverThread, args=[server_socket])
    receiver_thread.start()

    client_threa = threading.Thread(target=client_thread, args=[neighbors_ports])
    client_threa.start()

if __name__ == '__main__': 
    Main()