import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import random
import time
from PIL import Image, ImageTk

# Constants
BOARD_SIZE = 600
TILE_SIZE = BOARD_SIZE // 10
PLAYER_RADIUS = 15

# Snakes and Ladders (start: end)
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0
        self.token = None

class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")

        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()

        self.players = []
        self.current_player = 0

        self.board_image = Image.open("board.png").resize((BOARD_SIZE, BOARD_SIZE))
        self.board_photo = ImageTk.PhotoImage(self.board_image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.board_photo)

        self.setup_players()

        self.dice_label = tk.Label(root, text="", font=("Arial", 24))
        self.dice_label.pack(pady=10)
        self.roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)

    def setup_players(self):
        num_players = simpledialog.askinteger("Players", "Enter number of players (2-4):", minvalue=2, maxvalue=4)
        for i in range(num_players):
            name = simpledialog.askstring("Player Info", f"Enter name for Player {i+1}:")
            color = colorchooser.askcolor(title=f"Choose color for {name}")[1]
            player = Player(name, color)
            self.players.append(player)
            player.token = self.canvas.create_oval(0, 0, PLAYER_RADIUS*2, PLAYER_RADIUS*2, fill=color, outline="black")
        self.update_tokens()

    def position_to_coord(self, position):
        if position == 0:
            return (0, BOARD_SIZE - TILE_SIZE)
        row = (position - 1) // 10
        col = (position - 1) % 10
        x = col * TILE_SIZE
        if row % 2 == 1:
            x = BOARD_SIZE - TILE_SIZE - x
        y = BOARD_SIZE - (row + 1) * TILE_SIZE
        return (x, y)

    def update_tokens(self):
        for i, player in enumerate(self.players):
            x, y = self.position_to_coord(player.position)
            offset_x = (i % 2) * PLAYER_RADIUS
            offset_y = (i // 2) * PLAYER_RADIUS
            self.canvas.coords(player.token, x + offset_x, y + offset_y, x + PLAYER_RADIUS*2 + offset_x, y + PLAYER_RADIUS*2 + offset_y)

    def roll_dice(self):
        self.roll_button.config(state=tk.DISABLED)
        self.dice_label.config(text="Rolling...")
        self.root.update()
        time.sleep(0.5)

        dice = random.randint(1, 6)
        self.dice_label.config(text=f"{self.players[self.current_player].name} rolled a {dice}")
        self.move_player(dice)

    def move_player(self, dice):
        player = self.players[self.current_player]
        for _ in range(dice):
            if player.position < 100:
                player.position += 1
                self.update_tokens()
                self.root.update()
                time.sleep(0.2)

        if player.position in SNAKES:
            messagebox.showinfo("Snake!", f"{player.name} got bitten by a SNAKE!")
            player.position = SNAKES[player.position]
        elif player.position in LADDERS:
            messagebox.showinfo("Ladder!", f"{player.name} climbed a LADDER!")
            player.position = LADDERS[player.position]

        self.update_tokens()
        self.check_winner()

        self.current_player = (self.current_player + 1) % len(self.players)
        self.roll_button.config(state=tk.NORMAL)

    def check_winner(self):
        player = self.players[self.current_player]
        if player.position == 100:
            messagebox.showinfo("Game Over", f"{player.name} wins!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadder(root)
    root.mainloop()
