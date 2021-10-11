import socket 
import threading
import configparser
import sys
   
def workerThread(s):
    while True: 
        msg = s.recv(1024)
        if not msg: break
        print('O cliente enviou: ', msg.decode())
        msg = msg[::-1] #Inverte a String
        try:
           s.send(msg)
        except:
            print('Erro ao responder.')
    s.close()

def receiverThread(server_socket):
    print('\nThread de recebimento iniciada')
    server_socket.listen()
    while True: 
        s, addr = server_socket.accept() 
        print('Cliente Conectado:', addr[0], ':', addr[1])  
        tw = threading.Thread(target=workerThread, args=[s])
        tw.start()
  
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
    print(f'Vizinho 1 porta: {config.get("config", "neighbor1_port")}')
    print(f'Vizinho 2 porta: {config.get("config", "neighbor2_port")}')


    # Criando socket que estará ouvindo
    host = str(config.get("config", "ip"))
    port = int(config.get("config", "port"))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((host, port)) 
     
  
    print("\nServidor inicializado na porta " + str(port))

    #
    receiver_thread = threading.Thread(target=receiverThread, args=[server_socket])
    receiver_thread.start()

    while True:
        msg = input('\nInforme a fofoca: ')
        print(msg)
        
        dest = (host, int(config.get("config", "neighbor1_port"))) 
        print(f'Destino: {dest}')
        server_socket.settimeout(5)
        server_socket.connect(dest)
        server_socket.send(msg.encode('ascii'))

        try:
            response, servidor = server_socket.recvfrom(1024)
            print('Resposta do vizinho: ', response.decode())
            # Tratamento da resposta do vizinho
        except: 
            print('Ocorreu um erro...')

        #server_socket.close() #Fecha a conexão com o servidor

if __name__ == '__main__': 
    Main()