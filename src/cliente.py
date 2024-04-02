#Raphaella Brandão Jacques, Rafael Torres Nantes

from game_playerClass import Player_Class
import random
import time
import socket
import json
import sys

# Classe do jogo
class BlackJack_Class:
    def __init__(self, name='BLACK_JACK_GAME'):
        # Manipular informações aqui
        self.name = name
        self.players = []
        self.deck_Cards = []

    def embaralhar_baralho(self):
        # Embaralha as cartas do Baralho
        random.shuffle(self.deck_Cards)

    '''
    Cria um Deck de Cartas para o BlackJack com prints organizados
    Além de embaralhar as cartas do Deck
    '''
    def criar_baralho(self):
        organizar_Linhas(1)
        print("[BLACKJACK_GAME] Embaralhando as cartas !!!")
        self.deck_Cards = [str(i) for i in range(2, 10 + 1)] + ['J', 'Q', 'K', 'A']
        self.embaralhar_baralho()

    def iniciar_Jogo(self, players):

        # Cria o Deck de Cartas do BlackJack Game
        self.criar_baralho()

        # Inicio do Game, cada player irá receber 2 Cartas do baralho
        for player_n in players:
            player_n.pegar_carta(self.deck_Cards)
            player_n.pegar_carta(self.deck_Cards)

# Função para autenticar o usuário
def login(username, password):
    data = {'action': 'login', 'username': username, 'password': password}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para registrar um novo usuário
def register(name, username, password):
    data = {'action': 'register', 'name' : name, 'username': username, 'password': password}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para listar usuários online
def list_users_online():
    data = {'action': 'list_online'}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para listar usuários em jogos
def list_users_playing():
    data = {'action': 'list_playing'}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para iniciar um jogo com outro usuário
def game_ini(username, name):
    data = {'action': 'game_ini', 'opponent': username, 'invite': name}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para desconectar
def sair():
    data = {'action': 'sair'}
    client_socket.send(json.dumps(data).encode())

# Função para mudar o status para ativo
def ativa(username):
    data = {'action': 'ativa', 'username': username}
    client_socket.send(json.dumps(data).encode())


def receive_messages(message, username):
    """
    Função para receber mensagens do servidor.

    Returns:
        A mensagem recebida do servidor.
    """
    # Itera infinitamente
    while True:
        # Recebe uma mensagem do servidor

        try:
            # Verifica o conteúdo da mensagem
            if "Você recebeu um convite" in message:

                # Informa ao usuário que ele recebeu um convite
                print(message)

                # Solicita ao usuário que aceite ou recuse o convite
                while True:
                    print("1. GAME_ACK")
                    print("2. GAME_NEG")
                    response = input("Aceitar convite? (1/2): ")
                    if response == "1":

                        # Envia uma mensagem de resposta ao servidor
                        data = {
                            'action': 'resposta',
                            'message': 'GAME_ACK',
                            'opponent': username
                        }
                        client_socket.send(json.dumps(data).encode())

                        # Retorna a mensagem de resposta
                        return "GAME_ACK"
                    elif response == "2":

                        # Envia uma mensagem de resposta ao servidor
                        data = {
                            'action': 'resposta',
                            'message': 'GAME_NEG',
                            'opponent': username
                        }
                        client_socket.send(json.dumps(data).encode())

                        # Retorna a mensagem de resposta
                        return "GAME_NEG"
                    else:
                        print("Escolha uma opção válida (1 ou 2).")

            elif message == 'GAME_ACK':
                # Informa ao usuário que o convite foi aceito
                print("Convite aceito")

            elif message == 'GAME_NEG':
                # Informa ao usuário que o convite foi recusado
                print("Convite negado")

            # Retorna a mensagem recebida
            return message
        
        except ConnectionResetError:
            print("Conexão com o servidor perdida.")
            return False

def receber():
    """
    Função que recebe mensagens do servidor.

    Returns: A mensagem recebida do servidor, ou 'False' se não houver mensagem.
    """
    # Define "OK" como FALSE
    # Define um tempo limite de 2 segundos para o soquete
    ok = False
    client_socket.settimeout(2) 

    # Tenta receber uma mensagem do servidor.
    try:
        message = client_socket.recv(1024).decode()
        # Define a variável 'ok' como 'True' para indicar que uma mensagem foi recebida.
        if message:
            ok = True
    # Se o tempo limite for esgotado, significa que não há convites pendentes.
    except socket.timeout:
        pass
    
    # Restabelece o tempo limite do soquete para 20 segundos.
    client_socket.settimeout(20)

    # Se a variável `ok` estiver definida como 'True', retorna a mensagem recebida.
    if ok:
        return message
    
    # Caso contrário, retorna 'False'.
    return False

# Função para receber socket de outro usuário
def get_socket(username):
    data = {'action': 'socket', 'username': username}
    client_socket.send(json.dumps(data).encode())
    response = client_socket.recv(1024).decode()
    return response

def receive_messages_Game():
    msg = receber()
    if msg != False:
        jogo = receive_messages(msg, username)
        
        if jogo == "GAME_NEG":
            return "GAME_NEG"
        if jogo == "GAME_ACK":
            return "GAME_ACK"
#----------------------------------------------------Def do jogo---------------------------------------------------------

# Função para encerrar o jogo pelo cliente-oponente
def end_game():
    data = {'action': 'end_game'}
    opponent_socket.send(json.dumps(data).encode())

# Função para receber carta
def sim():
    data = {'action': 'sim'}
    opponent_socket.send(json.dumps(data).encode())

# Função para não receber carta
def nao():
    data = {'action': 'nao'}
    opponent_socket.send(json.dumps(data).encode())

# Função para encerrar o jogo pelo cliente-servidor
def game_over():
    data = {'action': 'game_over', 'username': oponente}
    conn.close()
    client_socket.send(json.dumps(data).encode())

# Imprime um cabeçalho para organizar
def organizar_Linhas(seg=2):
    print(40 * '+-')
    time.sleep(seg)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVIDOR = socket.gethostbyname(socket.gethostname()) #supondo que servidor e cliente estao na mesma maquina
    client_socket.connect((SERVIDOR, 8080)) # ip e porta do SAI 
    # Abrindo um socket para jogar
    # Configurar o socket do cliente
    client_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Definir a opção para reutilizar o endereço (opcional)
    client_listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincular o socket a um endereço e porta locais
    local_ip = client_socket.getsockname()[0]
    local_port = client_socket.getsockname()[1]
    client_listen_socket.bind((local_ip, local_port))

    client_listen_socket.listen(1)  # Permita apenas uma conexão entrante
    jogo = False

    # Loop infinito para permitir que o usuário faça login ou se registre
    while True:

        # Exibe as opções ao usuário
        print("1. Login")
        print("2. Register")
        choice = input("Escolha a opção (1/2): ")

        if choice == '1':
            # Solicita as informações de registro do usuário
            username = input("Nome de usuário: ")
            password = input("Senha: ")
            response = login(username, password)
            print(response) 
            # Verifica se o login foi bem-sucedido
            if response != "Falha na autenticacao":
                break

        # Solicita as informações de registro do usuário
        elif choice == '2':
            name = input("Nome: ")
            username = input("Nome de usuário: ")
            password = input("Senha: ")
            response = register(name, username, password)
            print(response) 

            # Verifica se o registro foi bem-sucedido
            if response == "Registro bem-sucedido":
                break
        # Exibe uma mensagem de erro
        else:
            print("Escolha uma opção válida.")

    while True:
        
        oponente = username
        
        while True:
            
            # Verifica se o jogo já está em andamento.
            if jogo == "GAME_ACK":
                break
            
            # Recebe mensagens do servidor.
            message_Game = receive_messages_Game()

            # Verifica se há mensagens recebidas
            if message_Game == "GAME_NEG":
                oponente = username
            elif message_Game == "GAME_ACK":
                break

            # Exibe as opções ao usuário
            print("1. Listar usuários online")
            print("2. Listar usuários jogando")
            print("3. Iniciar um jogo")
            print("4. Sair")
            choice = input("Escolha a opção (1/2/3/4): ")

            # Verifica a opção do usuário.
            # Solicita ao servidor uma lista de usuários online
            if choice == '1':
                message_Game = receive_messages_Game()
                if message_Game == "GAME_NEG":
                    oponente = username
                elif message_Game == "GAME_ACK":
                    break

                # Solicita ao servidor uma lista de usuários online
                response = list_users_online()

                # Verifica se a resposta não foi um convite para jogar
                jogo = receive_messages(response, username)
                
                # Exibe a resposta do servidor
                print(response)
            
            # Verifica a opção 2
            # Envia uma mensagem ao servidor solicitando a lista de usuários jogando
            elif choice == '2':
                message_Game = receive_messages_Game()
                if message_Game == "GAME_NEG":
                    oponente = username
                elif message_Game == "GAME_ACK":
                    break

                # Recebe uma resposta do servidor com a lista de usuários jogando
                response = list_users_playing()

                # Exibe a resposta do servidor
                print(response)
            
            # Verifica a opção 3
            # Verifica se o jogo já foi iniciado
            elif choice == '3':

                # Verifica se o oponente já foi definido
                if oponente == username:

                    # Solicita ao usuário o nome do oponente
                    opponent = input("Nome de usuário do oponente: ")

                    # Envia uma mensagem ao servidor solicitando o jogo
                    message_Game = receive_messages_Game()
                    if message_Game == "GAME_NEG":
                        oponente = username
                    elif message_Game == "GAME_ACK":
                        break

                    response = game_ini(opponent, username)
                    print(response)
                    
                    # Verifica se a resposta do servidor é um convite para o jogo
                    if "O convite para" in response:
                        oponente = opponent
                else:
                    print("Um convite já foi enviado, aguarde a resposta")

            # Desconecta o usuário do servidor
            elif choice == '4':
                sair()
                print('Desconectado.')
                sys.exit(0)

            # Exibe uma mensagem de erro, caso a opção seja inválida
            else:
                print("Escolha uma opção válida.")


        player = False
        # Verifica se o oponente é diferente do jogador atual
        if oponente != username:

            # Conecta com socket do oponente se enviou convite
            opponent = get_socket(oponente)

            # Verifica se o oponente desconectou
            if "desconectou" in opponent:
                print(opponent)
                continue  # Retorna ao início do while
                
            # Carrega o dicionário JSON com as informações do oponente
            opponent = json.loads(opponent)
            print(opponent)

            # Obtém o endereço IP e a porta do oponente
            opponent_ip, opponent_port = opponent['ip'], opponent['porta']

            # Verifica se o oponente tem um endereço IP e uma porta válidos
            if opponent_ip and opponent_port:
                
                # Criar um socket e se conectar ao oponente
                opponent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                opponent_socket.connect((opponent_ip, opponent_port))
                opponent_socket.send(username.encode())

                # Imprime as instruções do jogo
                organizar_Linhas(1)
                msg = ''' 
                Jogo: BlackJack
                Objetivo: ter o total de pontos mais proximo de 21 sem ultrapassa-lo
                Regras:
                1º: Se for um digito, o valor é o proprio número no intervalo: [2, 3, 4 ... 10]
                2º: As figuras. Sendo: ['J', 'Q' e 'K'] que valem 10\n
                3º: A carta 'A' tem valor 11
                '''
                print(msg)
                organizar_Linhas(1)
                
                # Imprime as informações dos Jogadores
                print(f"[BLACKJACK_GAME] Jogador [{1}]: {oponente}")
                organizar_Linhas(1)
                print(f"[BLACKJACK_GAME] Jogador [{2}]: {username}")
            # Define a variável `player` como 'True' para indicar que o jogador atual é o anfitrião
            player = True
            
        # Espera conexão no socket se recebeu convite
        else:
            
            # Aguarde uma conexão entrante
            try:
                conn, addr = client_listen_socket.accept()
                
                # Imprime uma mensagem de boas-vindas ao oponente
                print(f"Jogando com {addr}")
                ativa(username)

                # Inicia o jogo do BlackJack
                organizar_Linhas(1)
                msg = '''
                Jogo: BlackJack
                Objetivo: ter o total de pontos mais proximo de 21 sem ultrapassa-lo
                Regras:
                1º: Se for um digito, o valor é o proprio número no intervalo: [2, 3, 4 ... 10]
                2º: As figuras. Sendo: ['J', 'Q' e 'K'] que valem 10
                3º: A carta 'A' tem valor 11"
                '''
                print(msg)
            except KeyboardInterrupt:
                print("Interrupção do teclado (Ctrl+C) detectada. Encerrando o programa.")


            # Recebe o nome do oponente
            oponente = conn.recv(1024).decode()

            # iniciando o jogo
            organizar_Linhas(1)

            # Imprime as informações dos Jogadores
            print(f"[BLACKJACK_GAME] Jogador [{1}]: {username}")
            organizar_Linhas(1)
            print(f"[BLACKJACK_GAME] Jogador [{2}]: {oponente}")
            player_1 = Player_Class(username)
            player_2 = Player_Class(oponente)

            #------------------------------------como encerra o jogo----------------------------------------------
            blackJack = BlackJack_Class(username)
            blackJack.iniciar_Jogo([player_1, player_2])
            
        # Inicia o loop principal do cliente-oponente:
        if player:
            while True:

                jogo = False

                # Verifica se recebeu alguma mensagem de jogo
                message_Game = receive_messages_Game()
                if message_Game == "GAME_NEG":
                    oponente = username

                # Se o jogo foi aceito, sai do jogo atual
                elif message_Game == "GAME_ACK":
                    print(f"Jogo encerrado por {username} \n Iniciando outro jogo")
                    end_game()
                    jogo = message_Game
                    break

                #jogo
                #ações do jogo e pra terminar o jogo

                # Cliente-Oponente opponent_socket --> .send()
                # Verifica se há mensagens recebidas
                try: 
                    organizar_Linhas()
                    msg = opponent_socket.recv(1024).decode()
                    print(msg)
                    if "encerrado" in msg or "BLACKJACK_GAME_FIM" in msg:
                        jogo = False
                        break
                    
                    # Pergunta ao jogador se deseja comprar mais uma carta:
                    msg_str = '''[BLACKJACK_GAME] Deseja comprar mais uma carta?"\n1. Sim\n2. Nao\n3. Sair do jogo'''
                    print(msg_str)

                    # **Verifica se a opção escolhida é válida:
                    choice = input("Escolha a opção (1/2/3): ")
                    while not(choice == '1' or choice == '2' or choice == '3'):
                        print("Escolha uma opção válida.")
                        choice = input("Escolha a opção (1/2/3): ")

                    # Ação do cliente-oponente de acordo com a opção escolhida:
                    # Compra uma carta do baralho
                    if choice == '1':
                        sim()
                        # Envia a carta recebida para o servidor:
                        msg = opponent_socket.recv(1024).decode()
                        print(msg)
                        # Envia a carta recebida para o servidor:
                        msg = opponent_socket.recv(1024).decode()
                        print(msg)

                    # Não compra a carta ou passa a vez
                    elif choice == '2':
                        nao()

                    # Encerra o jogo atual 
                    elif choice == '3':
                        print(f"Jogo encerrado por {username}")
                        end_game()
                        jogo = False
                        break
                
                # Lidar com exceções de conexão fechada
                except (ConnectionResetError, OSError) as e:
                    print(f"Conexao com {oponente} perdida.")
                    oponente = username
                    game_over()
                    jogo = False
                    break

        #Ações do cliente-servidor
        else:
            while True:

                jogo = False

                # Verifica se recebeu alguma mensagem de jogo
                message_Game = receive_messages_Game()
                if message_Game == "GAME_NEG":
                    oponente = username

                # Se o jogo foi aceito, sai do jogo atual
                elif message_Game == "GAME_ACK":
                    print(f"Jogo encerrado por {username} \n Iniciando outro jogo")
                    end_game()
                    jogo = message_Game
                    break
    
                try:
                    '''
                    Para cada jogador em campo, enquanto não ultrapassem do valor de 21 Pontos, faz eles receberem um INPUT
                    Se o jogador não desejar comprar mais uma carta, ele para a jogada dele com o Deck e a Pontuação restante.
                    Caso contrário, ele continua comprando até se satisfazer
                    '''
                    organizar_Linhas()
                    print(player_1.Score())
                    # Ação do cliente-servidor no jogo

                    # Pergunta ao jogador se deseja comprar mais uma carta:
                    msg_str = '''[BLACKJACK_GAME] Deseja comprar mais uma carta?"\n1. Sim\n2. Nao\n3. Sair do jogo'''
                    print(msg_str)

                    if not(player_1.ultrapass_limit):
                        # Verifica se a opção escolhida é válida:
                        choice = input("Escolha a opção (1/2/3): ")
                        while not(choice == '1' or choice == '2' or choice == '3'):
                            print("Escolha uma opção válida.")
                            choice = input("Escolha a opção (1/2/3): ")
                    
                    else:
                        choice = 2

                    # Ação do cliente-servidor de acordo com a opção escolhida:
                    if choice == '1':
                        # Compra uma carta do baralho
                        player_1.pegar_carta(blackJack.deck_Cards)

                        # Imprime os valores das cartas que são compradas pelos jogadores
                        print(f"\n[BLACKJACK_GAME] A carta de {player_1.name}: [{player_1.player_hand[-1]}]")

                        # Caso o jogador ultrapasse 21 Pontos, ele recebe um player_n.bust = TRUE
                        if player_1.ultrapassar_limite():
                            print(f"[BLACKJACK_GAME] {player_1.name} ESTOUROUU O LIMITEE !!! \nScore: ['{player_1.player_points}']")
                            player_1.ultrapass_limit = True
                            
                        else:
                            print(player_1.Score())
                    
                    # Encerra o jogo atual
                    elif choice == '3':
                        print(f"Jogo encerrado por {username}")
                        conn.send(f"Jogo encerrado por {username}".encode())
                        game_over()
                        jogo = False
                        break
                    
                    conn.send(player_2.Score().encode())
                    data = conn.recv(1024).decode()
                    data = json.loads(data)

                    if data['action'] == 'end_game':
                        print(f"Jogo encerrado por {oponente}")
                        game_over()
                        jogo = False
                        break
                    
                    elif data['action'] == 'sim':
                        player_2.pegar_carta(blackJack.deck_Cards)

                        conn.send(f"\n[BLACKJACK_GAME] A carta de {player_2.name}: [{player_2.player_hand[-1]}]".encode())

                        if player_2.ultrapassar_limite():
                            conn.send(f"[BLACKJACK_GAME] {player_2.name} ESTOUROUU O LIMITEE !!! \nScore: ['{player_2.player_points}']".encode())
                            player_2.ultrapass_limit = True
                        else:
                            conn.send(player_2.Score().encode())
                    '''
                    Para cada player, a repetição irá checkar se o player/dealer venceram
                    1º Condição: Check se os Players empataram o Valor de Pontos, criando uma GAMBIARRA para o Empate
                    2º Condição: Check se o Player[0] venceu o Player[1], assumindo o Player 0 como VENCEDOR
                    3º Condição: Caso contrário, o Player[1] é o VENCEDOR
                    ''' 
                    
                    if (choice == '2' and data['action'] == 'nao'):
                        organizar_Linhas(5)
                        best_Score = 0

                        if(player_1.player_points == player_2.player_points):
                            best_Score = 0
                        elif player_1.verificar_vitoria(player_2):
                            best_Score = player_1
                        else:
                            best_Score = player_2
                        
                        try:
                            msg = f"[BLACKJACK_GAME_FIM] O ganhador do Jogo foi: {best_Score.name}\n {best_Score.Score()}"
                            print(msg)
                        
                        except:
                            msg = f"[BLACKJACK_GAME_FIM] EMPATOU O JOGO !!!"
                            print(msg)
                
                        conn.send(msg.encode())
                        game_over()
                        jogo = False
                        break

                # Lidar com exceções de conexão fechada
                except (ConnectionResetError, OSError) as e:
                    
                    print(f"Conexão com {oponente} perdida.")
                    game_over()
                    jogo = False
                    break
            