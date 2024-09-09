import random
import os
import uuid
from cards import Card, create_deck

class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.life = 20
        self.energy = 2
        self.deck = create_deck()
        self.hand = []
        self.board = []
        self.draw_initial_hand()
        self.attacked_this_turn = []
        self.is_human = is_human

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
                if self.board:
                    if self.is_human:
                        self.equip_card(card, card_index)
                    else:
                        self.ai_equip_card(card, card_index)
                else:
                    print("No creatures to equip the card to.")
                    self.energy += card.cost  # Refund energy if no valid target
            return card
        return None

    def cast_spell(self, card, opponent):
        if card.name == "Energy Boost":
            self.energy += 2
        elif card.name == "Spore Burst":
            opponent.life -= 3

    def equip_card(self, card, card_index):
        while True:
            try:
                target_index = int(input(f"Choose a creature to equip {card.name} to (index): ")) - 1
                if 0 <= target_index < len(self.board):
                    target = self.board[target_index]
                    if card.name == "Fungal Shield":
                        target.defense += 1
                    elif card.name == "Cyber Blade":
                        target.attack += 2
                    self.hand.pop(card_index)
                    break
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")

    def ai_equip_card(self, card, card_index):
        if self.board:
            target = random.choice(self.board)
            if card.name == "Fungal Shield":
                target.defense += 1
            elif card.name == "Cyber Blade":
                target.attack += 2
            self.hand.pop(card_index)

    def attack(self, opponent, game):
        if self.is_human:
            attackers = self.choose_attackers(game)
        else:
            attackers = self.ai_choose_attackers()

        if not attackers:
            print("No creatures to attack with.")
            return

        game.game_log.append(f"\033[1;31m{self.name} is attacking with {[i+1 for i in range(len(attackers))]}.\033[0m")

        if not opponent.board:
            for attacker in attackers:
                opponent.life -= attacker.attack
                self.attacked_this_turn.append(attacker)
            game.game_log.append(f"\033[1;31m{self.name} attacked {opponent.name} directly with {len(attackers)} creatures.\033[0m")
        else:
            if opponent.is_human:
                blockers = opponent.choose_blockers(game, attackers)
            else:
                blockers = opponent.ai_choose_blockers()

            for attacker, blocker in zip(attackers, blockers):
                if blocker:
                    game.game_log.append(f"\033[1;34m{blocker.name} blocks {attacker.name}.\033[0m")
                    attacker.defense -= blocker.attack
                    blocker.defense -= attacker.attack
                    if attacker.defense <= 0:
                        game.game_log.append(f"\033[1;31m{attacker.name} is destroyed.\033[0m")
                        self.board.remove(attacker)
                    if blocker.defense <= 0:
                        game.game_log.append(f"\033[1;31m{blocker.name} is destroyed.\033[0m")
                        opponent.board.remove(blocker)
                    self.attacked_this_turn.append(attacker)
                else:
                    opponent.life -= attacker.attack
                    self.attacked_this_turn.append(attacker)

            game.game_log.append(f"\033[1;31m{self.name} attacked {opponent.name} with {len(attackers)} creatures, {len([b for b in blockers if b])} were blocked.\033[0m")

    def choose_attackers(self, game):
        attackers = []
        while True:
            game.display_game_state()
            action = input(f"{self.name}, choose attackers (comma separated indices) or 'done': ").strip().lower()
            if action == 'done':
                break
            try:
                indices = list(map(lambda x: int(x) - 1, action.split(',')))
                for index in indices:
                    if 0 <= index < len(self.board) and self.board[index] not in self.attacked_this_turn:
                        attackers.append(self.board[index])
                break
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        return attackers

    def choose_blockers(self, game, attackers):
        blockers = [None] * len(attackers)
        while True:
            game.display_game_state()
            action = input(f"{self.name}, choose attackers to block (comma separated indices) or 'done' to skip: ").strip().lower()
            if action == 'done':
                return blockers  # No blockers, attack goes through
            try:
                indices = list(map(lambda x: int(x) - 1, action.split(',')))
                if all(0 <= index < len(attackers) for index in indices):
                    break
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        
        while True:
            game.display_game_state()
            action = input(f"{self.name}, assign blockers (comma separated indices): ").strip().lower()
            try:
                blocker_indices = list(map(lambda x: int(x) - 1, action.split(',')))
                if len(blocker_indices) == len(indices):
                    for blocker_index, attacker_index in zip(blocker_indices, indices):
                        if 0 <= blocker_index < len(self.board):
                            blockers[attacker_index] = self.board[blocker_index]
                    break
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        return blockers

    def ai_choose_attackers(self):
        return random.sample(self.board, min(len(self.board), random.randint(1, 3)))

    def ai_choose_blockers(self):
        return [random.choice(self.board) if random.random() > 0.5 else None for _ in range(len(self.board))]

    def reset_attacks(self):
        self.attacked_this_turn = []

    def __str__(self):
        return f"{self.name} - Life: {self.life}, Energy: {self.energy}, Deck: {len(self.deck)} cards"

class Game:
    def __init__(self):
        self.player1 = Player("Human")
        self.player2 = Player("AI", is_human=False)
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
        print("Opponent's board:", [f"{i+1}: {card.name} ({card.attack}/{card.defense})" for i, card in enumerate(self.player2.board)])
        print("GAMEBOARD HALF B")
        print("Your board:", [f"{i+1}: {card.name} ({card.attack}/{card.defense})" for i, card in enumerate(self.player1.board)])
        print("__________________________")
        print(f"\033[1;32mHuman - Life: {self.player1.life}, Energy: {self.player1.energy}, Deck: {len(self.player1.deck)} cards\033[0m")
        print("CARDS IN HAND:")
        print(f"{'Index':<6} {'Name':<20} {'Type':<10} {'Energy Cost':<12} {'Attack/Def':<10} {'Info'}")
        for i, card in enumerate(self.player1.hand):
            print(f"{i+1:<6} {card.name:<20} {card.card_type:<10} {card.cost:<12} {f'{card.attack}/{card.defense}':<10} {card.description}")
        print("__________________________")
        print("Game Log:")
        if full_log:
            for log in self.game_log:
                print(log)
        else:
            for log in self.game_log[-10:]:
                print(log)
        print("__________________________")

    def draw_phase(self):
        self.current_player.draw_card()
        self.game_log.append(f"\033[1;33m{self.current_player.name} drew a card.\033[0m")
        self.phase = "summon1"

    def summon_phase(self, phase_name):
        while True:
            self.display_game_state()
            action = input(f"{phase_name.capitalize()} Phase - Choose action: play, pass, help: ").strip().lower()
            if action == "play":
                card_index = int(input("Choose card index to play: ")) - 1
                card = self.current_player.play_card(card_index, self.opponent)
                if not card:
                    print("Not enough energy to play this card.")
                    self.game_log.append(f"\033[1;33m{self.current_player.name} tried to play a card but didn't have enough energy.\033[0m")
                else:
                    if card.card_type == 'creature':
                        self.game_log.append(f"\033[1;32m{self.current_player.name} played {card}.\033[0m")
                    elif card.card_type == 'spell':
                        self.game_log.append(f"\033[1;32m{self.current_player.name} cast {card}.\033[0m")
                    elif card.card_type == 'equipment':
                        self.game_log.append(f"\033[1;32m{self.current_player.name} equipped {card}.\033[0m")
            elif action == "pass":
                self.game_log.append(f"\033[1;33m{self.current_player.name} passed the {phase_name} phase.\033[0m")
                break
            elif action == "help":
                print("Available actions: play, pass, help")
                input("Press Enter to continue...")
            else:
                print("Invalid action.")
                self.game_log.append(f"\033[1;33m{self.current_player.name} chose an invalid action.\033[0m")

    def attack_phase(self):
        self.display_game_state()
        action = input("Attack Phase - Choose action: attack, pass, help: ").strip().lower()
        if action == "attack":
            self.current_player.attack(self.opponent, self)
            self.game_log.append(f"\033[1;31m{self.current_player.name} attacked {self.opponent.name}.\033[0m")
        elif action == "pass":
            self.game_log.append(f"\033[1;33m{self.current_player.name} passed the attack phase.\033[0m")
        elif action == "help":
            print("Available actions: attack, pass, help")
            input("Press Enter to continue...")
        else:
            print("Invalid action.")
            self.game_log.append(f"\033[1;33m{self.current_player.name} chose an invalid action.\033[0m")

    def end_phase(self):
        if self.current_player.is_human:
            self.game_log.append(f"\033[1;33m{self.current_player.name} ended their turn.\033[0m")
        else:
            self.game_log.append(f"\033[3;33m{self.current_player.name} ended their turn.\033[0m")  # Italics for AI
        self.switch_turn()

    def ai_turn(self):
        self.current_player = self.player2
        self.opponent = self.player1
        self.draw_phase()
        self.display_game_state()
        input("Press Enter to acknowledge AI's draw phase...")  # Acknowledge AI's draw phase
        # AI Summon Phase 1
        for i, card in enumerate(self.current_player.hand):
            if card.cost <= self.current_player.energy:
                if card.card_type == 'creature':
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} played {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
                    break
                elif card.card_type == 'equipment' and self.current_player.board:
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} equipped {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
                    break
                elif card.card_type == 'spell':
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} cast {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
                    break
        # AI Attack Phase
        if self.current_player.board:
            self.current_player.attack(self.opponent, self)
            self.game_log.append(f"\033[3;31m{self.current_player.name} attacked {self.opponent.name}.\033[0m")  # Italics for AI
            self.display_game_state()
            input("Press Enter to acknowledge AI's attack...")  # Acknowledge AI's attack
        # AI Summon Phase 2
        for i, card in enumerate(self.current_player.hand):
            if card.cost <= self.current_player.energy:
                if card.card_type == 'creature':
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} played {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
                    break
                elif card.card_type == 'equipment' and self.current_player.board:
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} equipped {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
                    break
                elif card.card_type == 'spell':
                    self.current_player.play_card(i, self.opponent)
                    self.game_log.append(f"\033[3;32m{self.current_player.name} cast {card}.\033[0m")  # Italics for AI
                    self.display_game_state()
                    input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
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
                card_index = int(command.split()[1]) - 1
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