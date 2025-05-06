import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random
import json

# Load card data
try:
    with open('kartes_dati.json', 'r') as file:
        data = json.load(file)
    print("Data loaded successfully:", data)
except FileNotFoundError:
    messagebox.showerror("Error", "JSON file not found!")
    data = {"cards": []}

LANGUAGES = {
    "ENG": {
        "pin": "PIN:",
        "withdraw": "Withdraw",
        "deposit": "Deposit",
        "check_balance": "Check Balance",
        "exit": "Exit",
        "success": "Success",
        "error": "Error",
        "invalid_pin": "Invalid PIN!",
        "insufficient_balance": "Insufficient balance!",
        "withdrawn": "Withdrawn ${amount}. New balance: ${balance}",
        "deposited": "Deposited ${amount}. New balance: ${balance}",
        "balance": "Your current balance is: ${balance}",
        "enter_amount_withdraw": "Enter amount to withdraw:",
        "enter_amount_deposit": "Enter amount to deposit:",
        "account_info": "Account Information",
        "name": "Name:",
        "card_number": "Card Number:",
        "view_account_info": "View Account Info",
        "blackjack": "Play Blackjack",
        "blackjack_title": "Blackjack",
        "dealer": "Dealer:",
        "player": "Player:",
        "hit": "Hit",
        "stand": "Stand",
        "new_game": "New Game",
        "bet": "Place Bet",
        "chips": "Chips:",
        "status": "Place your bet to start!",
        "blackjack_win": "Blackjack! You win!",
        "bust": "Bust! You went over 21.",
        "win": "You win!",
        "lose": "Dealer wins!",
        "tie": "Push! It's a tie.",
        "enter_bet": "Enter your bet amount:",
        "insufficient_chips": "Not enough chips!",
    },
    "LV": {
        "pin": "PIN:",
        "withdraw": "Izņemt naudu",
        "deposit": "Iemaksāt naudu",
        "check_balance": "Pārbaudīt atlikumu",
        "exit": "Iziet",
        "success": "Veiksmīgi",
        "error": "Kļūda",
        "invalid_pin": "Nepareizs PIN!",
        "insufficient_balance": "Nepietiekams atlikums!",
        "withdrawn": "Izņemti ${amount}. Jauns atlikums: ${balance}",
        "deposited": "Iemaksāti ${amount}. Jauns atlikums: ${balance}",
        "balance": "Jūsu pašreizējais atlikums ir: ${balance}",
        "enter_amount_withdraw": "Ievadiet izņemamo summu:",
        "enter_amount_deposit": "Ievadiet iemaksājamo summu:",
        "account_info": "Konta informācija",
        "name": "Vārds:",
        "card_number": "Kartes numurs:",
        "view_account_info": "Skatīt konta informāciju",
        "blackjack": "Spēlēt Blackjack",
        "blackjack_title": "Blackjack",
        "dealer": "Dīleris:",
        "player": "Spēlētājs:",
        "hit": "Vēl kārti",
        "stand": "Pietiek",
        "new_game": "Jauna spēle",
        "bet": "Veikt likmi",
        "chips": "Fipi:",
        "status": "Ievieto likmi, lai sāktu!",
        "blackjack_win": "Blackjack! Tu uzvarēji!",
        "bust": "Pārsniedzi 21!",
        "win": "Tu uzvarēji!",
        "lose": "Dīleris uzvar!",
        "tie": "Neizšķirts!",
        "enter_bet": "Ievadi likmes summu:",
        "insufficient_chips": "Nepietiek fipu!",
    },
    "RUS": {
        "pin": "ПИН:",
        "withdraw": "Снять деньги",
        "deposit": "Внести деньги",
        "check_balance": "Проверить баланс",
        "exit": "Выйти",
        "success": "Успех",
        "error": "Ошибка",
        "invalid_pin": "Неверный ПИН!",
        "insufficient_balance": "Недостаточно средств!",
        "withdrawn": "Снято ${amount}. Новый баланс: ${balance}",
        "deposited": "Внесено ${amount}. Новый баланс: ${balance}",
        "balance": "Ваш текущий баланс: ${balance}",
        "enter_amount_withdraw": "Введите сумму для снятия:",
        "enter_amount_deposit": "Введите сумму для внесения:",
        "account_info": "Информация о счете",
        "name": "Имя:",
        "card_number": "Номер карты:",
        "view_account_info": "Просмотреть информацию о счете",
        "blackjack": "Играть в Блэкджек",
        "blackjack_title": "Блэкджек",
        "dealer": "Дилер:",
        "player": "Игрок:",
        "hit": "Ещё карту",
        "stand": "Хватит",
        "new_game": "Новая игра",
        "bet": "Сделать ставку",
        "chips": "Фишки:",
        "status": "Сделайте ставку для начала!",
        "blackjack_win": "Блэкджек! Вы выиграли!",
        "bust": "Перебор! Вы превысили 21.",
        "win": "Вы выиграли!",
        "lose": "Дилер выиграл!",
        "tie": "Ничья!",
        "enter_bet": "Введите сумму ставки:",
        "insufficient_chips": "Недостаточно фишек!",
    }
}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()
        self.image = self._load_image()

    def _get_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)

    def _load_image(self):
        try:
            image_path = f"cards/{self.rank}_of_{self.suit.lower()}.png"
            img = Image.open(image_path)
            img = img.resize((100, 145), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            # Create a simple card representation if image not found
            img = Image.new('RGB', (100, 145), color='white')
            return ImageTk.PhotoImage(img)

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            # If deck is empty, create a new shuffled deck
            self.__init__()
            self.shuffle()
            return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class BlackjackGame:
    def __init__(self, parent, language, balance_callback):
        self.parent = parent
        self.current_language = language
        self.update_balance_callback = balance_callback
        self.current_bet = 0
        self.game_over = False

        self.window = tk.Toplevel(parent)
        self.window.title(LANGUAGES[self.current_language]["blackjack_title"])
        self.window.geometry("1000x700")
        self.window.configure(bg='green')

        # Game frames
        self.dealer_frame = tk.Frame(self.window, bg='green')
        self.dealer_frame.pack(pady=20)

        self.player_frame = tk.Frame(self.window, bg='green')
        self.player_frame.pack(pady=20)

        # Labels
        self.dealer_label = tk.Label(self.dealer_frame, text=LANGUAGES[self.current_language]["dealer"],
                                     bg='green', fg='white', font=('Arial', 14))
        self.dealer_label.pack(anchor='w')

        self.dealer_cards = tk.Frame(self.dealer_frame, bg='green')
        self.dealer_cards.pack()

        self.player_label = tk.Label(self.player_frame, text=LANGUAGES[self.current_language]["player"],
                                     bg='green', fg='white', font=('Arial', 14))
        self.player_label.pack(anchor='w')

        self.player_cards = tk.Frame(self.player_frame, bg='green')
        self.player_cards.pack()

        # Buttons
        self.button_frame = tk.Frame(self.window, bg='green')
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text=LANGUAGES[self.current_language]["hit"],
                                    width=10, command=self.hit, state=tk.DISABLED)
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.button_frame, text=LANGUAGES[self.current_language]["stand"],
                                      width=10, command=self.stand, state=tk.DISABLED)
        self.stand_button.grid(row=0, column=1, padx=10)

        self.bet_button = tk.Button(self.button_frame, text=LANGUAGES[self.current_language]["bet"],
                                    width=10, command=self.place_bet)
        self.bet_button.grid(row=0, column=2, padx=10)

        self.new_game_button = tk.Button(self.button_frame, text=LANGUAGES[self.current_language]["new_game"],
                                         width=10, command=self.new_game)
        self.new_game_button.grid(row=0, column=3, padx=10)

        # Status and chips
        self.status_var = tk.StringVar()
        self.status_var.set(LANGUAGES[self.current_language]["status"])
        self.status_label = tk.Label(self.window, textvariable=self.status_var,
                                     bg='green', fg='white', font=('Arial', 14))
        self.status_label.pack()

        self.chips_var = tk.StringVar()
        self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
        self.chips_label = tk.Label(self.window, textvariable=self.chips_var,
                                    bg='green', fg='white', font=('Arial', 14))
        self.chips_label.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.new_game()

    def get_balance(self):
        return self.update_balance_callback("get")

    def update_balance(self, amount):
        return self.update_balance_callback("update", amount)

    def close_window(self):
        if not self.game_over and self.current_bet > 0:
            if messagebox.askyesno(LANGUAGES[self.current_language]["exit"],
                                   "Are you sure you want to quit? You'll lose your current bet."):
                self.window.destroy()
        else:
            self.window.destroy()

    def new_game(self):
        # Clear card displays
        for widget in self.dealer_cards.winfo_children():
            widget.destroy()
        for widget in self.player_cards.winfo_children():
            widget.destroy()

        # Reset game state
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.current_bet = 0
        self.game_over = False

        # Update UI
        self.status_var.set(LANGUAGES[self.current_language]["status"])
        self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
        self.dealer_label.config(text=f"{LANGUAGES[self.current_language]['dealer']} ?")
        self.player_label.config(text=f"{LANGUAGES[self.current_language]['player']} 0")

        # Enable betting button
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)

    def place_bet(self):
        balance = self.get_balance()
        bet = simpledialog.askinteger(
            LANGUAGES[self.current_language]["bet"],
            LANGUAGES[self.current_language]["enter_bet"],
            parent=self.window,
            minvalue=1,
            maxvalue=balance
        )

        if bet and bet <= balance:
            self.current_bet = bet
            self.update_balance(-bet)
            self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
            self.status_var.set(f"Bet: {self.current_bet}")

            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.bet_button.config(state=tk.DISABLED)

            self.deal_initial_cards()
        elif bet:
            messagebox.showerror(LANGUAGES[self.current_language]["error"],
                                 LANGUAGES[self.current_language]["insufficient_chips"])

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.show_cards()

        # Check for blackjack
        if self.player_hand.value == 21:
            self.blackjack()

    def show_cards(self, reveal_dealer=False):
        # Show dealer cards
        for i, card in enumerate(self.dealer_hand.cards):
            if i == 0 and not reveal_dealer:
                # Show card back for first dealer card
                img = Image.new('RGB', (100, 145), color='blue')
                card_back = ImageTk.PhotoImage(img)
                label = tk.Label(self.dealer_cards, image=card_back, bg='green')
                label.image = card_back
                label.grid(row=0, column=i, padx=5)
            else:
                label = tk.Label(self.dealer_cards, image=card.image, bg='green')
                label.image = card.image
                label.grid(row=0, column=i, padx=5)

        # Show player cards
        for i, card in enumerate(self.player_hand.cards):
            label = tk.Label(self.player_cards, image=card.image, bg='green')
            label.image = card.image
            label.grid(row=0, column=i, padx=5)

        # Update values
        if reveal_dealer:
            self.dealer_label.config(text=f"{LANGUAGES[self.current_language]['dealer']} {self.dealer_hand.value}")
        else:
            self.dealer_label.config(text=f"{LANGUAGES[self.current_language]['dealer']} ?")

        self.player_label.config(text=f"{LANGUAGES[self.current_language]['player']} {self.player_hand.value}")

    def hit(self):
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.adjust_for_ace()
        self.show_cards()

        if self.player_hand.value > 21:
            self.bust()

    def stand(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        # Reveal dealer's hidden card
        self.show_cards(reveal_dealer=True)

        # Dealer plays
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.adjust_for_ace()
            self.show_cards(reveal_dealer=True)
            self.window.update()
            self.window.after(1000)  # Pause for 1 second between dealer hits

        self.check_winner()

    def blackjack(self):
        self.game_over = True
        winnings = int(self.current_bet * 2.5)  # Blackjack pays 3:2
        self.update_balance(winnings)
        self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
        self.show_cards(reveal_dealer=True)
        self.status_var.set(LANGUAGES[self.current_language]["blackjack_win"])
        messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                            LANGUAGES[self.current_language]["blackjack_win"])
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)

        # Reset the game after a short delay
        self.window.after(2000, self.new_game)

    def bust(self):
        self.game_over = True
        self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
        self.show_cards(reveal_dealer=True)
        self.status_var.set(LANGUAGES[self.current_language]["bust"])
        messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                            LANGUAGES[self.current_language]["bust"])
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)

        # Reset the game after a short delay
        self.window.after(2000, self.new_game)

    def check_winner(self):
        self.game_over = True
        balance_change = 0

        if self.dealer_hand.value > 21:
            balance_change = self.current_bet * 2
            self.status_var.set(LANGUAGES[self.current_language]["win"])
            messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                                LANGUAGES[self.current_language]["win"])
        elif self.dealer_hand.value > self.player_hand.value:
            balance_change = 0
            self.status_var.set(LANGUAGES[self.current_language]["lose"])
            messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                                LANGUAGES[self.current_language]["lose"])
        elif self.player_hand.value > self.dealer_hand.value:
            balance_change = self.current_bet * 2
            self.status_var.set(LANGUAGES[self.current_language]["win"])
            messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                                LANGUAGES[self.current_language]["win"])
        else:
            balance_change = self.current_bet
            self.status_var.set(LANGUAGES[self.current_language]["tie"])
            messagebox.showinfo(LANGUAGES[self.current_language]["blackjack_title"],
                                LANGUAGES[self.current_language]["tie"])

        if balance_change > 0:
            self.update_balance(balance_change)

        self.chips_var.set(f"{LANGUAGES[self.current_language]['chips']} {self.get_balance()}")
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)

        # Reset the game after a short delay to see the final cards
        self.window.after(2000, self.new_game)


class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank ATM")
        self.root.geometry("1500x800")
        self.root.configure(bg="purple")

        self.PIN_var = tk.StringVar()
        self.current_card = None
        self.transaction_window = None
        self.current_language = "ENG"
        self.balance = 0  # Will be set when card is validated

        self.create_frames()
        self.create_widgets()
        self.create_buttons()

    def create_frames(self):
        self.PIN_frame = tk.Frame(self.root, bg="purple")
        self.lang_frame = tk.Frame(self.root, bg="purple")
        self.button_frame = tk.Frame(self.root, bg="purple")
        self.button_frame_1 = tk.Frame(self.root, bg="purple")
        self.button_frame_2 = tk.Frame(self.root, bg="purple")
        self.button_frame_3 = tk.Frame(self.root, bg="purple")

    def create_widgets(self):
        self.PIN_label = tk.Label(self.PIN_frame, text=LANGUAGES[self.current_language]["pin"],
                                  bg="purple", fg="white", font=("Arial", 35, "bold"))
        self.PIN_entry = tk.Entry(self.PIN_frame, show="*", font=("Arial", 15), textvariable=self.PIN_var)

        # Pack widgets
        self.PIN_label.pack(side="left", padx=10)
        self.PIN_entry.pack(side="left", padx=10)
        self.PIN_frame.pack(pady=20)

    def create_buttons(self):
        self.load_language_buttons()
        self.lang_frame.pack(pady=10)

        self.create_number_buttons()
        self.button_frame.pack(pady=10)
        self.button_frame_1.pack(pady=10)
        self.button_frame_2.pack(pady=10)
        self.button_frame_3.pack(pady=10)

    def load_language_buttons(self):
        try:
            self.eng_img = self.load_image("images/eng.png", (50, 30))
            self.lv_img = self.load_image("images/lv.png", (50, 30))
            self.rus_img = self.load_image("images/rus.jpeg", (50, 30))

            self.eng_btn = tk.Button(self.lang_frame, image=self.eng_img, text="ENG",
                                     compound="center", bg="black", font="bold",
                                     command=lambda: self.switch_language("ENG"))
            self.eng_btn.pack(side="left", padx=5)
            self.lv_btn = tk.Button(self.lang_frame, image=self.lv_img, text="LV",
                                    compound="center", bg="black", font="bold",
                                    command=lambda: self.switch_language("LV"))
            self.lv_btn.pack(side="left", padx=5)
            self.rus_btn = tk.Button(self.lang_frame, image=self.rus_img, text="RUS",
                                     compound="center", bg="black", font="bold",
                                     command=lambda: self.switch_language("RUS"))
            self.rus_btn.pack(side="left", padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load images: {e}")
            # Fallback to text buttons if images fail
            self.eng_btn = tk.Button(self.lang_frame, text="ENG",
                                     command=lambda: self.switch_language("ENG"))
            self.eng_btn.pack(side="left", padx=5)
            self.lv_btn = tk.Button(self.lang_frame, text="LV",
                                    command=lambda: self.switch_language("LV"))
            self.lv_btn.pack(side="left", padx=5)
            self.rus_btn = tk.Button(self.lang_frame, text="RUS",
                                     command=lambda: self.switch_language("RUS"))
            self.rus_btn.pack(side="left", padx=5)

    def load_image(self, path, size):
        image = Image.open(path)
        image = image.resize(size)
        return ImageTk.PhotoImage(image)

    def create_number_buttons(self):
        buttons = [
            ("1", "2", "3", self.button_frame),
            ("4", "5", "6", self.button_frame_1),
            ("7", "8", "9", self.button_frame_2),
            ("DEL", "0", "Enter", self.button_frame_3)
        ]

        for row in buttons:
            for text in row[:3]:
                if text == "Enter":
                    btn = tk.Button(row[3], text=text, height=5, width=10, command=self.enter_func)
                elif text == "DEL":
                    btn = tk.Button(row[3], text=text, height=5, width=10, command=self.delete_func)
                else:
                    btn = tk.Button(row[3], text=text, height=5, width=10, command=lambda t=text: self.append_pin(t))
                btn.configure(bg="white", borderwidth=9)
                btn.pack(side="left", padx=5, pady=5)

    def append_pin(self, value):
        current_pin = self.PIN_var.get()
        self.PIN_var.set(current_pin + value)

    def delete_func(self):
        current_pin = self.PIN_var.get()
        self.PIN_var.set(current_pin[:-1])

    def enter_func(self):
        entered_pin = self.PIN_var.get()

        if self.validate_pin(entered_pin):
            messagebox.showinfo(LANGUAGES[self.current_language]["success"], "PIN is correct!")
            self.open_transaction_window()
        else:
            messagebox.showerror(LANGUAGES[self.current_language]["error"],
                                 LANGUAGES[self.current_language]["invalid_pin"])

    def validate_pin(self, entered_pin):
        for card in data.get("cards", []):
            if card.get("pin") == entered_pin:
                self.current_card = card
                self.balance = card.get("balance", 0)
                return True
        return False

    def open_transaction_window(self):
        self.root.withdraw()

        self.transaction_window = tk.Toplevel(self.root)
        self.transaction_window.title("Transaction Window")
        self.transaction_window.geometry("1500x800")
        self.transaction_window.configure(bg="purple")

        self.transaction_window.protocol("WM_DELETE_WINDOW", self.close_transaction_window)

        withdraw_btn = tk.Button(self.transaction_window, text=LANGUAGES[self.current_language]["withdraw"],
                                 font=("Arial", 20), command=self.withdraw)
        withdraw_btn.pack(pady=10)

        deposit_btn = tk.Button(self.transaction_window, text=LANGUAGES[self.current_language]["deposit"],
                                font=("Arial", 20), command=self.deposit)
        deposit_btn.pack(pady=10)

        balance_btn = tk.Button(self.transaction_window, text=LANGUAGES[self.current_language]["check_balance"],
                                font=("Arial", 20), command=self.check_balance)
        balance_btn.pack(pady=10)

        account_info_btn = tk.Button(self.transaction_window,
                                     text=LANGUAGES[self.current_language]["view_account_info"],
                                     font=("Arial", 20), command=self.show_account_info)
        account_info_btn.pack(pady=10)

        blackjack_btn = tk.Button(self.transaction_window, text=LANGUAGES[self.current_language]["blackjack"],
                                  font=("Arial", 20), command=self.play_blackjack)
        blackjack_btn.pack(pady=10)

        exit_btn = tk.Button(self.transaction_window, text=LANGUAGES[self.current_language]["exit"],
                             font=("Arial", 20), command=self.close_transaction_window)
        exit_btn.pack(pady=10)

    def close_transaction_window(self):
        self.transaction_window.destroy()
        self.root.deiconify()

    def withdraw(self):
        amount = simpledialog.askinteger(
            LANGUAGES[self.current_language]["withdraw"],
            LANGUAGES[self.current_language]["enter_amount_withdraw"],
            parent=self.transaction_window
        )
        if amount is not None:
            if amount > self.balance:
                messagebox.showerror(LANGUAGES[self.current_language]["error"],
                                     LANGUAGES[self.current_language]["insufficient_balance"])
            else:
                self.balance -= amount
                self.update_card_balance()
                messagebox.showinfo(LANGUAGES[self.current_language]["success"],
                                    LANGUAGES[self.current_language]["withdrawn"].format(
                                        amount=amount, balance=self.balance))

    def deposit(self):
        amount = simpledialog.askinteger(
            LANGUAGES[self.current_language]["deposit"],
            LANGUAGES[self.current_language]["enter_amount_deposit"],
            parent=self.transaction_window
        )
        if amount is not None:
            self.balance += amount
            self.update_card_balance()
            messagebox.showinfo(LANGUAGES[self.current_language]["success"],
                                LANGUAGES[self.current_language]["deposited"].format(
                                    amount=amount, balance=self.balance))

    def check_balance(self):
        messagebox.showinfo(LANGUAGES[self.current_language]["balance"],
                            LANGUAGES[self.current_language]["balance"].format(balance=self.balance))

    def show_account_info(self):
        account_info_window = tk.Toplevel(self.transaction_window)
        account_info_window.title(LANGUAGES[self.current_language]["account_info"])
        account_info_window.geometry("400x200")
        account_info_window.configure(bg="purple")

        name_label = tk.Label(account_info_window,
                              text=f"{LANGUAGES[self.current_language]['name']} {self.current_card['name']}",
                              font=("Arial", 16), bg="purple")
        name_label.pack(pady=10)

        card_number_label = tk.Label(account_info_window,
                                     text=f"{LANGUAGES[self.current_language]['card_number']} {self.current_card['card_number']}",
                                     font=("Arial", 16), bg="purple")
        card_number_label.pack(pady=10)

        ok_button = tk.Button(account_info_window, text="OK", font=("Arial", 16),
                              command=account_info_window.destroy)
        ok_button.pack(pady=20)

    def play_blackjack(self):
        # Pass a callback function to manage the balance
        def balance_callback(action, amount=0):
            if action == "get":
                return self.balance
            elif action == "update":
                self.balance += amount
                self.update_card_balance()
                return self.balance

        BlackjackGame(self.transaction_window, self.current_language, balance_callback)

    def update_card_balance(self):
        # Update the balance in the data structure
        for card in data.get("cards", []):
            if card.get("pin") == self.current_card["pin"]:
                card["balance"] = self.balance
                break

        # Save to file
        try:
            with open('kartes_dati.json', 'w') as file:
                json.dump(data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def switch_language(self, language):
        self.current_language = language
        self.update_ui_text()

    def update_ui_text(self):
        self.PIN_label.config(text=LANGUAGES[self.current_language]["pin"])
        if hasattr(self, 'transaction_window') and self.transaction_window:
            for widget in self.transaction_window.winfo_children():
                if isinstance(widget, tk.Button):
                    if widget["text"] == LANGUAGES["ENG"]["withdraw"]:
                        widget.config(text=LANGUAGES[self.current_language]["withdraw"])
                    elif widget["text"] == LANGUAGES["ENG"]["deposit"]:
                        widget.config(text=LANGUAGES[self.current_language]["deposit"])
                    elif widget["text"] == LANGUAGES["ENG"]["check_balance"]:
                        widget.config(text=LANGUAGES[self.current_language]["check_balance"])
                    elif widget["text"] == LANGUAGES["ENG"]["view_account_info"]:
                        widget.config(text=LANGUAGES[self.current_language]["view_account_info"])
                    elif widget["text"] == LANGUAGES["ENG"]["blackjack"]:
                        widget.config(text=LANGUAGES[self.current_language]["blackjack"])
                    elif widget["text"] == LANGUAGES["ENG"]["exit"]:
                        widget.config(text=LANGUAGES[self.current_language]["exit"])


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
