import random
import os
from cards import Card, create_deck

class Player:
    def __init__(self, name):
        self.name = name
        self.life = 20
        self.energy = 2
        self.deck = create_deck()
        self.hand = []
        self.board = []
        self.draw_initial_hand()
        self.attacked_this_turn = []

    def draw_initial_hand(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        if self.deck:
            self.hand.append(self.deck.pop())

    def play_card(self, card_index, opponent):
        card = self.hand[card_index]
        if card.cost <= self.energy:
            self.energy -= card.cost
            if card.card_type == 'creature':
                self.board.append(self.hand.pop(card_index))
            elif card.card_type == 'spell':
                self.cast_spell(card, opponent)
                self.hand.pop(card_index)
            elif card.card_type == 'equipment':
                self.equip_card(card)
                self.hand.pop(card_index)
            return card
        return None

    def cast_spell(self, card, opponent):
        if card.name == "Energy Boost":
            self.energy += 2
        elif card.name == "Spore Burst":
            opponent.life -= 3

    def equip_card(self, card):
        if self.board:
            target = self.board[0]  # Equip the first creature on the board
            if card.name == "Fungal Shield":
                target.defense += 1
            elif card.name == "Cyber Blade":
                target.attack += 2

    def attack(self, opponent):
        for card in self.board:
            if card.card_type == 'creature' and card not in self.attacked_this_turn:
                opponent.life -= card.attack
                self.attacked_this_turn.append(card)

    def reset_attacks(self):
        self.attacked_this_turn = []

    def __str__(self):
        return f"{self.name} - Life: {self.life}, Energy: {self.energy}, Deck: {len(self.deck)} cards"

class Game:
    def __init__(self):
        self.player1 = Player("Human")
        self.player2 = Player("AI")
        self.current_player = self.player1
        self.opponent = self.player2
        self.turn = 1
        self.game_log = []
        self.phase = "draw"

    def switch_turn(self):
        self.current_player, self.opponent = self.opponent, self.current_player
        self.current_player.energy += 1
        self.current_player.reset_attacks()
        self.turn += 1
        self.phase = "draw"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_game_state(self, full_log=False):
        self.clear_screen()
        print(f"\033[1;34m====================")
        print(f"      TURN {self.turn}      ")
        print(f"====================\033[0m")
        print(f"\033[1;31mAI - Life: {self.player2.life}, Energy: {self.player2.energy}, Deck: {len(self.player2.deck)} cards\033[0m")
        print("__________________________")
        print("GAMEBOARD HALF A")
        print("Opponent's board:", [f"{card.name} ({card.attack}/{card.defense})" for card in self.player2.board])
        print("GAMEBOARD HALF B")
        print("Your board:", [f"{card.name} ({card.attack}/{card.defense})" for card in self.player1.board])
        print("__________________________")
        print(f"\033[1;32mHuman - Life: {self.player1.life}, Energy: {self.player1.energy}, Deck: {len(self.player1.deck)} cards\033[0m")
        print("CARDS IN HAND:")
        for i, card in enumerate(self.player1.hand):
            print(f"{i}: {card}")
        print("__________________________")
        print("Game Log:")
        if full_log:
            for log in self.game_log:
                print(log)
        else:
            for log in self.game_log[-5:]:
                print(log)
        print("__________________________")

    def draw_phase(self):
        self.current_player.draw_card()
        self.game_log.append(f"{self.current_player.name} drew a card.")
        self.phase = "summon1"

    def summon_phase(self, phase_name):
        while True:
            self.display_game_state()
            action = input(f"{phase_name.capitalize()} Phase - Choose action: play, pass, help: ").strip().lower()
            if action == "play":
                card_index = int(input("Choose card index to play: "))
                card = self.current_player.play_card(card_index, self.opponent)
                if not card:
                    print("Not enough energy to play this card.")
                    self.game_log.append(f"{self.current_player.name} tried to play a card but didn't have enough energy.")
                else:
                    if card.card_type == 'creature':
                        self.game_log.append(f"{self.current_player.name} played {card}.")
                    elif card.card_type == 'spell':
                        self.game_log.append(f"{self.current_player.name} cast {card}.")
                    elif card.card_type == 'equipment':
                        self.game_log.append(f"{self.current_player.name} equipped {card}.")
            elif action == "pass":
                self.game_log.append(f"{self.current_player.name} passed the {phase_name} phase.")
                break
            elif action == "help":
                print("Available actions: play, pass, help")
                input("Press Enter to continue...")
            else:
                print("Invalid action.")
                self.game_log.append(f"{self.current_player.name} chose an invalid action.")

    def attack_phase(self):
        self.display_game_state()
        action = input("Attack Phase - Choose action: attack, pass, help: ").strip().lower()
        if action == "attack":
            self.current_player.attack(self.opponent)
            self.game_log.append(f"{self.current_player.name} attacked {self.opponent.name}.")
        elif action == "pass":
            self.game_log.append(f"{self.current_player.name} passed the attack phase.")
        elif action == "help":
            print("Available actions: attack, pass, help")
            input("Press Enter to continue...")
        else:
            print("Invalid action.")
            self.game_log.append(f"{self.current_player.name} chose an invalid action.")

    def end_phase(self):
        self.switch_turn()
        self.game_log.append(f"{self.current_player.name} ended their turn.")

    def ai_turn(self):
        self.current_player = self.player2
        self.opponent = self.player1
        self.draw_phase()
        # AI Summon Phase 1
        for i, card in enumerate(self.current_player.hand):
            if card.cost <= self.current_player.energy:
                self.current_player.play_card(i, self.opponent)
                self.game_log.append(f"{self.current_player.name} played {card}.")
                break
        # AI Attack Phase
        self.current_player.attack(self.opponent)
        self.game_log.append(f"{self.current_player.name} attacked {self.opponent.name}.")
        # AI Summon Phase 2
        for i, card in enumerate(self.current_player.hand):
            if card.cost <= self.current_player.energy:
                self.current_player.play_card(i, self.opponent)
                self.game_log.append(f"{self.current_player.name} played {card}.")
                break
        self.end_phase()
        self.current_player = self.player1
        self.opponent = self.player2

    def play(self):
        while self.player1.life > 0 and self.player2.life > 0:
            if self.current_player == self.player1:
                if self.phase == "draw":
                    self.draw_phase()
                elif self.phase == "summon1":
                    self.summon_phase("summon1")
                    self.phase = "attack"
                elif self.phase == "attack":
                    self.attack_phase()
                    self.phase = "summon2"
                elif self.phase == "summon2":
                    self.summon_phase("summon2")
                    self.phase = "end"
                elif self.phase == "end":
                    self.end_phase()
            else:
                self.ai_turn()
            if self.player1.life <= 0 or self.player2.life <= 0:
                break
        self.display_game_state()
        print("Game Over")
        if self.player1.life > 0:
            print("Human wins!")
        else:
            print("AI wins!")

    def handle_command(self, command):
        if command == "log":
            self.display_game_state(full_log=True)
            input("Press Enter to continue...")
        elif command == "board":
            self.display_game_state()
            input("Press Enter to continue...")
        elif command.startswith("info"):
            try:
                card_index = int(command.split()[1])
                print(self.current_player.hand[card_index])
                input("Press Enter to continue...")
            except (IndexError, ValueError):
                print("Invalid card index.")
                input("Press Enter to continue...")
        elif command == "help":
            print("Available commands: play, attack, pass, end turn, quit game, log, board, info <card index>, help")
            input("Press Enter to continue...")
        else:
            print("Invalid command.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.play()