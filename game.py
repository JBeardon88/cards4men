import os
from player import Player

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
        print("Opponent's board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player2.board)])
        print("GAMEBOARD HALF B")
        print("Your board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player1.board)])
        print("__________________________")
        print(f"\033[1;32mHuman - Life: {self.player1.life}, Energy: {self.player1.energy}, Deck: {len(self.player1.deck)} cards\033[0m")
        print("CARDS IN HAND:")
        print(f"{'Index':<6} {'Name':<20} {'Type':<10} {'Energy Cost':<12} {'Attack/Def':<10} {'Info':<30}")
        for i, card in enumerate(self.player1.hand):
            info = card.description if len(card.description) <= 30 else card.description[:27] + "..."
            print(f"{i+1:<6} {card.name:<20} {card.card_type:<10} {card.cost:<12} {f'{card.attack}/{card.defense}':<10} {info:<30}")
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
                try:
                    card_index = int(input("Choose card index to play: ")) - 1
                    played_card = self.current_player.play_card(card_index, self.opponent)
                    if played_card:
                        if played_card.card_type == 'creature':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} played {played_card.name}.\033[0m")
                        elif played_card.card_type == 'spell':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} cast {played_card.name}.\033[0m")
                        elif played_card.card_type == 'equipment':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} equipped {played_card.name}.\033[0m")
                    else:
                        print("Failed to play the card.")
                except ValueError:
                    print("Invalid input. Please enter a valid card index.")
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
            self.display_game_state()
            print(f"Debug: Current player hand: {[card.name for card in self.current_player.hand]}")
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

if __name__ == "__main__":
    game = Game()
    game.play()
        