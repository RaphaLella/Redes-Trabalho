#Raphaella Brandão Jacques, Rafael Torres Nantes

import socket
import threading
import json
import logging

# Configuração do logger
logging.basicConfig(filename='game_log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Função para registrar eventos no servidor
def log_event(event):
    logger.info(event)

'''
Dicionário para armazenar informações de:
    1º Usuários;
    2º Usuários Online;
    3º Jogos em Andamento;
    4º Convites Pendentes;
'''
user_data = {}
user_online = {}
games = {}
invitations = {}

def handle_user(client_socket, addr):
    '''
    Função para lidar com a autenticação e registro de usuários
    '''   
    print(f"[Nova conexao] {addr} conectou.")
    lock_account = True

    while True:
        try:
            data = client_socket.recv(1024).decode()
            data = json.loads(data)
            print(f"[{addr}] {data}")

            if lock_account:
                # Registrar Usuários
                if data['action'] == 'register': 
                    
                    # Registra o Cliente que não está cadastrado no Servidor
                    if not(data['username'] in user_data):
                        name = data['name']
                        username = data['username']
                        password = data['password']
                        user_data[username] = {'name': name, 'password': password}
                        user_online[username] = {'status': 'INATIVO', 'ip': addr[0], 'porta': addr[1], 'socket' : client_socket}
                        
                        # SERVER informa ao usuário que o cadastro foi bem sucedido
                        client_socket.send("Registro bem-sucedido".encode())

                        # Escreve os valores no Arquivo JSON
                        with open("data.json", "w") as f:
                            json.dump(user_data, f)

                        # LOG_EVENT informa que o usuário cadastrou-se
                        log_event(f"{username} realizou cadastro")
                        log_event(f"{username} ficou inativo")
                        lock_account = False

                    # Cliente já está cadastrado no Servidor !!!
                    else:
                        client_socket.send('Nome de usuário já está em uso. Escolha outro nome de usuário.'.encode())
                
                # Autenticação de Usuários
                elif data['action'] == 'login': 
                    username = data['username']
                    password = data['password']
                    
                    # Confirma as informações do Cliente, se o USERNAME e PASSWRORD estão corretos
                    if username in user_data and user_data[username]['password'] == password:
                        user_online[username] = {'status': 'INATIVO' , 'ip' : addr[0], 'porta' : addr[1], 'socket' : client_socket}
                        client_socket.send('Autenticacao bem-sucedida'.encode())
                        log_event(f"{username} conectou-se")
                        log_event(f"{username} ficou inativo")
                        lock_account = False
                    # Caso falhe na autentificação de USERNAME e PASSWRORD
                    else:
                        client_socket.send('Falha na autenticacao'.encode())

                # O Cliente utilizou alguma opção inválida para o LOCK_ACCOUNT       
                else:
                    client_socket.send('Escolha um opcao valida'.encode())
                    
            # Esta parte do código verifica se a lock_account está Desligado.
            # Se estiver, permite que o Cliente faça outras ações.

            if lock_account == False:
                # Lista os usuários online
                if data['action'] == 'list_online':
                    list_users_online(client_socket)

                # Lista os usuários jogando
                elif data['action'] == 'list_playing':
                    list_users_playing(client_socket)

                # Inicia um jogo
                elif data['action'] == 'game_ini':
                    start_game(data['opponent'], data['invite'], client_socket)

                # Sai do jogo
                elif data['action'] == 'sair':
                    sair(username, client_socket)
                    return

                # Recebe uma resposta a um convite
                elif data['action'] == 'resposta':
                    invite_res(data['opponent'], client_socket, data['message'])

                # Obtém as informações do socket de um usuário
                elif data['action'] == 'socket':
                    get_socket_info(data['username'], client_socket)

                # Informa ao servidor que o jogo terminou
                elif data['action'] == 'game_over':
                    game_over(data['username'])

                # Informa ao servidor que o usuário está ativo
                elif data['action'] == 'ativa':
                    ativa(data['username'])

                # Caso o usuário escolha uma ação inválida
                else:
                    print(f"{data['action']} ?")
        
        # Esta parte do código verifica se o CLIENTE enviou uma mensagem ao SERVER.
        # Se não, o usuário é removido da lista de usuários online e a conexão é encerrada.
        except (ConnectionResetError, OSError) as e:
            '''
            1º - Registra o evento de desligamento do usuário
            2º - Encerra a conexão com o cliente
            3º - Deleta o usuário da lista de usuários online
            '''
            log_event(f"{username} nao responde ('morreu')")
            print(f"Conexao com {addr} perdida.")
            del user_online[username]
            break

def list_users_online(client_socket):
    '''
    Função para listar usuários online
    '''   
    online_users_info = [(username, data) for username, data in user_online.items()]
    online_users_str = '\n'.join([f'{username} ({data["status"]}) - IP: {data["ip"]}, Porta: {data["porta"]}' for username, data in online_users_info])
    client_socket.send(online_users_str.encode())


def list_users_playing(client_socket):
    '''
    Função para listar usuários jogando 
    '''
    # Cria uma lista de tuplas, onde cada tupla contém o nome de usuário e os dados de um jogo em andamento, para todos os jogos em andamento.
    games_info = [(username, data) for username, data in games.items()]

    # Cria uma string que contém a lista de jogos em andamento, formatada de maneira legível.
    games_str = "Jogos em andamento:\n"
    for username, data in games_info:
        opponent = data['opponent']

        # Verifica se o Cliente e seu oponente estão online.
        if username in user_online and opponent in user_online:

            # Obtém os dados de conexão do Cliente e de seu oponente.
            user_data = user_online[username]
            opponent_data = user_online[opponent]

            # Adiciona a informação do jogo à string.
            game_info_str = f'{username} (IP: {user_data["ip"]}, Porta: {user_data["porta"]}) X {opponent} (IP: {opponent_data["ip"]}, Porta: {opponent_data["porta"]})'
            games_str += game_info_str + '\n'
    
    # Envia a string para o cliente.
    client_socket.send(games_str.encode())


def start_game(opponent, data, client_socket):
    '''
    Função para lidar com o convite para iniciar um jogo
    '''
    # Verifica se o oponente já está na lista de convites pendentes.
    if opponent not in invitations:
        # Adiciona o convite à lista.
        invitations[opponent] = data

        # Verifica se o oponente está online.
        if opponent in user_online:
            '''
            1º - Obtém o socket do oponente.
            2º - Envia uma mensagem para o oponente informando que ele recebeu um convite.
            3º - Informa ao Cliente que o convite foi enviado para o oponente.
            '''
            opponent_client_socket = user_online[opponent]['socket']
            opponent_client_socket.send(f"Você recebeu um convite de {data} para um jogo.".encode())
            client_socket.send(f"O convite para {opponent} foi enviado".encode())
        
        # Informa ao Cliente que o oponente não está online.
        else:
            client_socket.send(f"O {opponent} não está online".encode())
    
    # Informa ao Cliente que o convite já está pendente.
    else:
        client_socket.send(f"O convite para {opponent} já está pendente".encode())

def invite_res(opponent, client_socket, response):

    '''
    Função para lidar com a resposta a um convite para iniciar um jogo.
    '''
    # Obtém o nome de quem convidou.
    convite = invitations[opponent]

    # Remove o convite da lista.
    del invitations[opponent]

    # Verifica se o usuário que enviou o convite está online.
    if convite in user_online:

        # Verifica a resposta do convite.
        if response == 'GAME_ACK':

            # Altera o status dos jogadores para ativo.
            if user_online[convite]['status'] == 'INATIVO':
                user_online[convite]['status'] = 'ATIVO'
                log_event(f"{convite} ficou ativo")
            user_online[opponent]['status'] = 'ATIVO'
            log_event(f"{opponent} ficou ativo")

            # Adiciona os jogadores à lista de jogos.
            games[convite] = {'opponent': opponent}
            log_event(f"Usuarios {convite} e {opponent}: PLAYING")

        # Envia a mensagem de resposta para quem convidou.
        convite_client_socket = user_online[convite]['socket']  # Obtém o socket de quem convidou
        convite_client_socket.send(response.encode())

def sair(username, client_socket):
    '''
    Função para desconectar um usuário da rede:
        1º Remove o usuário do dicionário user_online
        2º Registra o evento de desligamento do usuário.
        3º Fecha o socket do usuário.
    '''
    user_online.pop(username)
    log_event(f"{username} desconectou-se da rede")
    client_socket.close()

def get_socket_info(username, client_socket):
    '''
    Função que devolve o socket de um usuário específico.
    '''

    # Verifica se o usuário está online.
    if username in user_online:
        # Obtém os dados de conexão do usuário.
        opponent_data = user_online[username]

        # Cria um dicionário com as informações de conexão do usuário.
        socket_info = {
            'ip': opponent_data['ip'],
            'porta': opponent_data['porta']
        }
        # Serializa o dicionário para JSON.
        socket_info_json = json.dumps(socket_info)

        # Envia o JSON para o cliente.
        client_socket.send(socket_info_json.encode())
    
    # Informa ao cliente que o usuário está desconectado.
    else:
        client_socket.send(f"Oponente {username} desconectou.".encode())

def game_over(username):
    '''
    Função para realizar o termino do jogo
    '''
    # Obtém o nome de quem convidou
    jogador = games[username]['opponent']

    # Remove o jogo atual da lista
    del games[username]

    # Altera o status dos jogadores para inativo
    user_online[username]['status'] = 'INATIVO'
    user_online[jogador]['status'] = 'INATIVO'

     # Registra o evento de término do jogo
    log_event(f"{username} ficou inativo")
    log_event(f"{jogador} ficou inativo")

def ativa(username):
    '''
    Função para alterar o status de um Cliente para ATIVO.
    '''
    # Verifica se o status do Cliente é inativo
    if user_online[username]['status'] == 'INATIVO':
         # Altera o status para ativo
        user_online[username]['status'] = 'ATIVO'
        # Registra o evento de ativação do status
        log_event(f"{username} ficou ativo")

def main():
    '''
    Função principal para lidar com as conexões dos clientes
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVIDOR = socket.gethostbyname(socket.gethostname())
    server.bind((SERVIDOR, 8080))
    server.listen(5)
    print(f"Servidor SAI esperando por conexoes em {SERVIDOR} ...")

    # Armazena IP e PORTA no addr, usamos o cliente_socket
    while True:
        client_socket, addr = server.accept()
        print(f'Conexao de {addr[0]}:{addr[1]}')

        # Thread separada para lidar com cada cliente
        client_handler = threading.Thread(target=handle_user, args=(client_socket, addr))
        client_handler.start()
        print(f"[Conexoes ativas] {threading.active_count() - 1}")


main()
