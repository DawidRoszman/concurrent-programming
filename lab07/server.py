import socket

class RockPaperScissorsServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        
        # Słownik do przechowywania adresów i portów graczy
        self.players = {}
        
        # Punktacja graczy
        self.scores = {'player1': 0, 'player2': 0}
        
        # Aktualny stan gry
        self.player_choices = {}
        
        print(f"Serwer uruchomiony na {self.host}:{self.port}")

    def determine_winner(self, choice1, choice2):
        """Określa zwycięzcę rundy"""
        if choice1 == choice2:
            return 'remis'
        elif (
            (choice1 == 'k' and choice2 == 'n') or  # kamień > nożyce
            (choice1 == 'n' and choice2 == 'p') or  # nożyce > papier
            (choice1 == 'p' and choice2 == 'k')     # papier > kamień
        ):
            return 'player1'
        else:
            return 'player2'

    def run(self):
        while True:
            # Resetowanie stanu gry
            self.player_choices.clear()
            print("\nNowa rozgrywka - oczekiwanie na graczy...")

            # Oczekiwanie na wybory graczy
            while len(self.player_choices) < 2:
                data, addr = self.server_socket.recvfrom(1024)
                choice = data.decode().strip()

                # Rejestracja graczy
                if addr not in self.players.values():
                    player_name = f'player{len(self.players) + 1}'
                    self.players[player_name] = addr
                    print(f"Zarejestrowano {player_name} z adresu {addr}")

                # Obsługa końca gry
                if choice == 'koniec':
                    self.handle_game_end(addr)
                    self.players = {}
                    self.scores = {'player1': 0, 'player2': 0}
                    self.player_choices = {}
                    continue

                # Rejestracja wyboru gracza
                player_name = [name for name, player_addr in self.players.items() if player_addr == addr][0]
                self.player_choices[player_name] = choice
                print(f"Otrzymano wybór od {player_name}: {choice}")

            # Określenie zwycięzcy rundy
            winner = self.determine_winner(
                self.player_choices['player1'], 
                self.player_choices['player2']
            )

            # Aktualizacja punktacji
            if winner != 'remis':
                self.scores[winner] += 1

            # Wysyłanie wyników do graczy
            for player_name, addr in self.players.items():
                opponent_name = 'player2' if player_name == 'player1' else 'player1'
                opponent_choice = self.player_choices[opponent_name]
                
                result_message = (
                    f"Wybór przeciwnika: {opponent_choice}, "
                    f"Runde wygral: {winner}, "
                    f"Twój punkty: {self.scores[player_name]}, "
                    f"Punkty przeciwnika: {self.scores[opponent_name]}"
                )
                self.server_socket.sendto(result_message.encode(), addr)

            print(f"Wyniki rundy: {self.scores}")

    def handle_game_end(self, ending_player_addr):
        """Obsługa zakończenia gry"""
        # Czekaj na potwierdzenie zakończenia od drugiego gracza
        while True:
            data, addr = self.server_socket.recvfrom(1024)
            choice = data.decode().strip()

            if choice == 'koniec':
                # Jeśli drugi gracz też chce zakończyć, zresetuj stan
                print("Gra zakończona przez obu graczy.")
                self.scores = {'player1': 0, 'player2': 0}
                self.players.clear()
                break
            else:
                # Jeśli drugi gracz kontynuuje, powiadom go o końcu
                self.server_socket.sendto('koniec'.encode(), addr)
                print("Gra zakończona jednostronnie.",ending_player_addr)
                break

if __name__ == '__main__':
    server = RockPaperScissorsServer()
    server.run()
