#Raphaella Brandão Jacques, Rafael Torres Nantes

class Player_Class:
    def __init__(self, name='NAME_N'):
        # Manipular informações aaqui
        self.name = name
        self.inGame = True
        # Variáveis do Game
        self.player_points = 0
        self.player_hand = []
        self.ultrapass_limit = False

    def pegar_carta(self, baralho):
        card = baralho.pop()
        self.player_hand.append(card)
        self.calcular_pontuacao(card)
    
    def calcular_pontuacao(self, card):
        '''
        1º Condição: Se for um digito, o número estará entre o intervalo: [2, 3, 4 ... 10]
        2º Condição: O valor será uma das figuras. Sendo: ['J', 'Q' e 'K'] que valem 10
        3º Condição: Restando apenas o 'A' que apresenta o valor 11
        '''
        if card.isdigit():
            self.player_points += int(card)       
        elif (card == 'J') or (card == 'Q') or (card == 'K'):
            self.player_points += 10
        else:
            self.player_points += 11

    def ultrapassar_limite(self):
        # Check se os pontos do Player/Dealer teve um valor acima de 21 Pontos
        return self.player_points > 21

    def verificar_vitoria(self, another_player):
        if self.ultrapass_limit:
            return False

        return (self.player_points > another_player.player_points) or another_player.ultrapass_limit
        
        # Check se o Player teve um valor acima do Dealer e se o não superou o limite de 21 Ponto
        #return (self.player_points > another_player.player_points) and self.ultrapass_limit
    
    def Score(self):
        # Imprime o Score do Jogador e as Cartas na sua mão
        return(f"[{self.name}]\nScore: ['{self.player_points}'] \nCartas na mão: '{self.player_hand}'")