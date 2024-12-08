import socket

class RockPaperScissorsClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        
        # Utwórz gniazdo UDP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Automatycznie wybierz losowy port lokalny
        self.client_socket.bind(('127.0.0.1', 0))
        
        # Punktacja
        self.score = 0
        self.opponent_score = 0

    def play(self):
        """Główna pętla gry"""
        while True:
            print("\nWybierz: k (kamień), p (papier), n (nożyce) lub 'koniec'")
            choice = input("Twój wybór: ").strip().lower()

            # Sprawdzenie poprawności wyboru
            if choice not in ['k', 'p', 'n', 'koniec']:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
                continue

            # Wysłanie wyboru do serwera
            try:
                self.client_socket.sendto(
                    choice.encode(), 
                    (self.server_host, self.server_port)
                )
                
                # Zakończenie gry, jeśli wybrano 'koniec'
                if choice == 'koniec':
                    print("Wysłano żądanie zakończenia gry.")
                    break

                # Oczekiwanie na wynik
                self.client_socket.settimeout(10)  # Limit czasu na odpowiedź
                data, _ = self.client_socket.recvfrom(1024)
                result = data.decode()

                # Obsługa komunikatu końca gry
                if result == 'koniec':
                    print("Gra została zakończona przez serwer.")
                    break

                # Wyświetlenie wyniku rundy
                print("\n" + result)

            except socket.timeout:
                print("Upłynął limit czasu oczekiwania na serwer.")
            except Exception as e:
                print(f"Błąd: {e}")

if __name__ == '__main__':
    client = RockPaperScissorsClient()
    client.play()
