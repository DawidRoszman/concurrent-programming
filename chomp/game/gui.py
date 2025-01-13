import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import random
from game.game import Chomp
from network.network import NetworkChomp


class NetworkChompGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Networked Chomp")
        self.game = Chomp()
        self.network = NetworkChomp()
        
        self.setup_network_ui()
        self.create_game_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_network_ui(self):
        self.network_frame = tk.Frame(self)
        self.network_frame.pack(pady=100, padx=200)
        
        tk.Button(self.network_frame, text="Host Game", 
                 command=self.host_game).pack(pady=5)
        tk.Button(self.network_frame, text="Join Game", 
                 command=self.join_game).pack(pady=5)
                 
    def create_game_ui(self):
        self.game_frame = tk.Frame(self)
        self.buttons = []
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()
        self.restart_button = tk.Button(self, text="Restart Game", 
                                      command=self.request_restart)
        
    def host_game(self):
        port = simpledialog.askinteger("Host Game", "Enter port number:", 
                                     initialvalue=5000)
        if port:
            try:
                ip = self.network.host_game(port)
                messagebox.showinfo("Host Info", 
                                  f"Your IP: {ip}\nPort: {port}\n"
                                  "Waiting for opponent...")
                threading.Thread(target=self.accept_connection, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def accept_connection(self):
        try:
            addr = self.network.accept_client()
            # Host decides first turn
            first_turn = random.choice([True, False])
            self.network.send_message("game_start", {"host_starts": first_turn})
            self.game.start_game(first_turn)
            self.after(100, self.start_game_ui)
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except:
            messagebox.showerror("Error", "Connection failed")
            self.network.close()
        
    def join_game(self):
        host = simpledialog.askstring("Join Game", "Enter host IP:", initialvalue="0.0.0.0")
        port = simpledialog.askinteger("Join Game", "Enter port number:", 
                                     initialvalue=5000)
        if host and port:
            try:
                self.network.join_game(host, port)
                threading.Thread(target=self.receive_messages, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def start_game_ui(self):
        self.network_frame.pack_forget()
        self.game_frame.pack(padx=400,pady=400)
        self.restart_button.pack(pady=5)
        
        for i in range(self.game.height):
            row = []
            for j in range(self.game.width):
                btn = tk.Button(self.game_frame, width=2, height=1,
                              command=lambda x=j, y=i: self.make_move(x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)
        self.update_board()
        self.update_status()
        
    def make_move(self, x, y):
        if not self.game.game_running or not self.network.connected:
            return
            
        is_my_turn = (self.network.is_host == self.game.player_1_turn)
        if not is_my_turn:
            return
            
        if self.game.eat_chocolate(x, y):
            self.network.send_message("move", {"x": x, "y": y})
            self.handle_game_over(True)
        else:
            if self.network.send_message("move", {"x": x, "y": y}):
                self.update_board()
                self.update_status()
            else:
                self.handle_connection_lost()
                
    def receive_messages(self):
        while self.network.connected:
            message = self.network.receive_message()
            if not message:
                self.after(100, self.handle_connection_lost)
                break
                
            if message["type"] == "game_start":
                host_starts = message["data"]["host_starts"]
                self.game.start_game(host_starts)
                self.after(100, self.start_game_ui)
            elif message["type"] == "move":
                move = message["data"]
                if self.game.eat_chocolate(move["x"], move["y"]):
                    self.after(100, lambda: self.handle_game_over(False))
                else:
                    self.after(100, self.update_board)
                    self.after(100, self.update_status)
            elif message["type"] == "restart_request":
                self.after(100, self.handle_restart_request)
            elif message["type"] == "restart_accept":
                self.after(100, lambda: self.restart_game(message["data"]["host_starts"]))
            elif message["type"] == "restart_decline":
                self.after(100, lambda: messagebox.showinfo(
                    "Restart", "Opponent declined restart"))
                
    def request_restart(self):
        if self.network.send_message("restart_request", {}):
            messagebox.showinfo("Restart", "Restart request sent to opponent")
            
    def handle_restart_request(self):
        if messagebox.askyesno("Restart Game", "Opponent wants to restart. Accept?"):
            first_turn = random.choice([True, False])
            self.network.send_message("restart_accept", {"host_starts": first_turn})
            self.restart_game(first_turn)
        else:
            self.network.send_message("restart_decline", {})
            
    def restart_game(self, host_starts):
        self.game.start_game(host_starts)
        self.update_board()
        self.update_status()
            
    def handle_game_over(self, is_loser):
        result = "Victory!" if not is_loser else "Defeat!"
        messagebox.showinfo("Game Over", result)
        self.network.send_message("game_over", 
                                {"winner": self.network.is_host != (not is_loser)})
        self.update_board()
            
    def handle_connection_lost(self):
        if self.game.game_running:
            messagebox.showerror("Error", "Connection to opponent lost")
            self.game.game_running = False
            self.network.close()
            self.quit()
        
    def update_board(self):
        for i in range(self.game.height):
            for j in range(self.game.width):
                text = "🧪" if self.game.board[i][j] == self.game.poisoned_chocolate else \
                       "🍫" if self.game.board[i][j] == self.game.chocolate else " "
                self.buttons[i][j].config(text=text)
                
    def update_status(self):
        print(self.game.player_1_turn, self.network.is_host)
        turn = "Your turn" if (self.network.is_host == self.game.player_1_turn) else "Opponent's turn"
        self.status_label.config(text=turn)
        
    def on_closing(self):
        self.game.game_running = False
        self.network.close()
        self.quit()


