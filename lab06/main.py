import sysv_ipc

# Stałe identyfikujące klucze pamięci i semaforów
MEMORY_KEY1 = 123456
MEMORY_KEY2 = 654321
SEM_PLAYER1_KEY = 11111
SEM_PLAYER2_KEY = 22222
SEM_SYNC1_KEY = 33333
SEM_SYNC2_KEY = 44444

class ThreeCardGame:
    def __init__(self):
        self.is_first_player = False
        self.setup_ipc()

    def setup_ipc(self):
        """Próba utworzenia zasobów IPC - wyścig procesów"""
        try:
            # Próba utworzenia pamięci współdzielonej
            self.memory1 = sysv_ipc.SharedMemory(MEMORY_KEY1, flags=sysv_ipc.IPC_CREX)
            self.memory2 = sysv_ipc.SharedMemory(MEMORY_KEY2, flags=sysv_ipc.IPC_CREX)
            self.is_first_player = True
        except sysv_ipc.Error:
            # Jeśli pamięć już istnieje, dołączamy jako drugi proces
            self.memory1 = sysv_ipc.SharedMemory(MEMORY_KEY1)
            self.memory2 = sysv_ipc.SharedMemory(MEMORY_KEY2)
            self.is_first_player = False

        # Analogicznie dla semaforów
        try:
            self.sem_player1 = sysv_ipc.Semaphore(SEM_PLAYER1_KEY, flags=sysv_ipc.IPC_CREX)
            self.sem_player2 = sysv_ipc.Semaphore(SEM_PLAYER2_KEY, flags=sysv_ipc.IPC_CREX)
            self.sem_sync1 = sysv_ipc.Semaphore(SEM_SYNC1_KEY, flags=sysv_ipc.IPC_CREX, initial_value=0)
            self.sem_sync2 = sysv_ipc.Semaphore(SEM_SYNC2_KEY, flags=sysv_ipc.IPC_CREX, initial_value=0)
        except sysv_ipc.Error:
            self.sem_player1 = sysv_ipc.Semaphore(SEM_PLAYER1_KEY)
            self.sem_player2 = sysv_ipc.Semaphore(SEM_PLAYER2_KEY)
            self.sem_sync1 = sysv_ipc.Semaphore(SEM_SYNC1_KEY)
            self.sem_sync2 = sysv_ipc.Semaphore(SEM_SYNC2_KEY)

    def play_game(self):
        player_score = 0
        opponent_score = 0

        for turn in range(1, 4):
            print(f"\n--- Tura {turn} ---")

            if self.is_first_player:
                # Gracz 1: Ustawienie wygrywającej karty
                winning_pos = self.get_player_input("Ustaw pozycję wygrywającej karty (1/2/3): ", [1, 2, 3])
                self.memory1.write(str(winning_pos).encode())
                
                # Czekanie na wybór przeciwnika
                self.sem_player2.acquire()
                opponent_choice = int(self.memory2.read().decode())
                print(f"Przeciwnik wybrał pozycję: {opponent_choice}")

                # Sprawdzenie wyniku
                if winning_pos == opponent_choice:
                    print("Przegrałeś tę turę!")
                    opponent_score += 1
                else:
                    print("Wygrałeś tę turę!")
                    player_score += 1

                # Zwolnienie semafora dla przeciwnika
                self.sem_player1.release()

            else:
                # Gracz 2: Odgadywanie pozycji
                opponent_pos = self.get_player_input("Wybierz pozycję (1/2/3): ", [1, 2, 3])
                self.memory2.write(str(opponent_pos).encode())
                
                # Zwolnienie semafora dla pierwszego gracza
                self.sem_player2.release()

                # Czekanie na ujawnienie pozycji przeciwnika
                self.sem_player1.acquire()
                winning_pos = int(self.memory1.read().decode())
                print(f"Przeciwnik ustawił pozycję: {winning_pos}")

                # Sprawdzenie wyniku
                if opponent_pos == winning_pos:
                    print("Wygrałeś tę turę!")
                    player_score += 1
                else:
                    print("Przegrałeś tę turę!")
                    opponent_score += 1

            # Wyświetlenie wyniku
            print(f"Aktualny wynik - Ty: {player_score}, Przeciwnik: {opponent_score}")

        # Zakończenie gry
        self.display_final_result(player_score, opponent_score)
        self.cleanup_ipc()

    def get_player_input(self, prompt, valid_choices):
        while True:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
            except ValueError:
                print("Proszę wprowadzić liczbę.")

    def display_final_result(self, player_score, opponent_score):
        print("\n--- Koniec gry ---")
        if player_score > opponent_score:
            print("Gratulacje! Wygrałeś całą grę!")
        elif player_score < opponent_score:
            print("Niestety, przegrałeś całą grę.")
        else:
            print("Remis!")
        print(f"Końcowy wynik - Ty: {player_score}, Przeciwnik: {opponent_score}")

    def cleanup_ipc(self):
        """Usuwanie zasobów IPC po zakończeniu gry"""
        try:
            self.memory1.remove()
            self.memory2.remove()
            self.sem_player1.remove()
            self.sem_player2.remove()
            self.sem_sync1.remove()
            self.sem_sync2.remove()
        except Exception as e:
            print(f"Błąd podczas usuwania zasobów IPC: {e}")

def main():
    try:
        game = ThreeCardGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\nGra przerwana przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()
