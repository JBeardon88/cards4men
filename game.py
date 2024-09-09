import os
import time
import random
from player import Player
from display import display_game_state  # Import the display_game_state function

class Game:
    def __init__(self):
        self.player1 = Player("Human")
        self.player2 = Player("AI", is_human=False)
        self.current_player = self.player1
        self.opponent = self.player2
        self.turn = 1
        self.game_log = []
        self.phase = "upkeep"

    def play(self):
        while self.player1.life > 0 and self.player2.life > 0:
            display_game_state(self)  # Use the imported function
            print(f"Debug: Current player: {self.current_player.name}")
            print(f"Debug: Current player hand: {[card.name for card in self.current_player.hand]}")
            
            if self.current_player.is_human:
                self.human_turn()
            else:
                self.ai_turn()
            
            if self.player1.life <= 0 or self.player2.life <= 0:
                break
            
            self.switch_turn()
            time.sleep(0.5)  # Add a small delay between turns
        
        display_game_state(self)  # Use the imported function
        print("Game Over")
        if self.player1.life > 0:
            print("Human wins!")
        else:
            print("AI wins!")

    def human_turn(self):
        self.upkeep_phase()
        self.summon_phase("summon1")
        self.attack_phase()
        self.summon_phase("summon2")
        self.current_player.end_phase()  # Call the player's end_phase method

    def ai_turn(self):
        self.upkeep_phase()
        self.ai_summon_phase("summon1")
        self.ai_attack_phase()
        self.ai_summon_phase("summon2")
        self.current_player.end_phase()  # Call the player's end_phase method

    def switch_turn(self):
        self.current_player, self.opponent = self.opponent, self.current_player
        self.turn += 1
        for card in self.current_player.board:
            card.summoning_sickness = False

    def upkeep_phase(self):
        self.current_player.untap_all()
        self.current_player.energy += 1  # Gain 1 energy at the start of the turn
        self.game_log.append(f"{self.current_player.name} untapped all cards and gained 1 energy.")
        self.current_player.draw_card()
        self.game_log.append(f"{self.current_player.name} drew a card.")
        self.phase = "summon1"

    def summon_phase(self, phase_name):
        while True:
            display_game_state(self)  # Use the imported function
            action = input(f"{phase_name.capitalize()} Phase - Choose action: play, pass, help, info: ").strip().lower()
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
                        elif played_card.card_type == 'enchantment':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} cast {played_card.name}.\033[0m")
                    else:
                        print("Failed to play the card.")
                except ValueError:
                    print("Invalid input. Please enter a valid card index.")
            elif action == "pass":
                self.game_log.append(f"\033[1;33m{self.current_player.name} passed the {phase_name} phase.\033[0m")
                break
            elif action == "help":
                print("Available actions: play, pass, help, info")
                input("Press Enter to continue...")
            elif action == "info":
                try:
                    card_index = int(input("Choose card index to view info: ")) - 1
                    if 0 <= card_index < len(self.current_player.hand):
                        card = self.current_player.hand[card_index]
                        print(f"Name: {card.name}")
                        print(f"Type: {card.card_type}")
                        print(f"Energy Cost: {card.cost}")
                        print(f"Attack/Defense: {card.attack}/{card.defense}")
                        print(f"Description: {card.description}")
                        input("Press Enter to continue...")
                    else:
                        print("Invalid card index.")
                except ValueError:
                    print("Invalid input. Please enter a valid card index.")
            else:
                print("Invalid action.")
                self.game_log.append(f"\033[1;33m{self.current_player.name} chose an invalid action.\033[0m")

    def ai_summon_phase(self, phase_name):
        playable_cards = [card for card in self.current_player.hand if card.cost <= self.current_player.energy]
        if playable_cards:
            card_to_play = random.choice(playable_cards)
            card_index = self.current_player.hand.index(card_to_play)
            played_card = self.current_player.play_card(card_index, self.opponent)
            if played_card:
                self.game_log.append(f"\033[3;32mAI played {played_card.name}.\033[0m")
                display_game_state(self)  # Use the imported function
                input("Press Enter to acknowledge AI's action...")  # Acknowledge AI's action
        else:
            self.game_log.append(f"\033[3;33mAI passed the {phase_name} phase.\033[0m")

    def attack_phase(self):
        while True:
            display_game_state(self)  # Use the imported function
            action = input("Attack Phase - Choose action: attack, pass, help: ").strip().lower()
            if action == "attack":
                attackers = self.current_player.choose_attackers(self)
                if attackers:
                    attacker_descriptions = [f"{self.current_player.board.index(a) + 1}: {str(a)}" for a in attackers]
                    self.game_log.append(f"\033[1;31m{self.current_player.name} declared attackers: {', '.join(attacker_descriptions)}.\033[0m")
                    display_game_state(self)  # Use the imported function
                    input("Press Enter to acknowledge attackers...")  # Acknowledge attackers

                    if self.opponent.board:
                        blockers = self.opponent.choose_blockers(self, attackers)
                        if blockers:
                            blocker_descriptions = [f"{self.opponent.board.index(b) + 1}: {str(b)}" if b else "X" for b in blockers]
                            self.game_log.append(f"\033[1;31m{self.opponent.name} declared blockers: {', '.join(blocker_descriptions)}.\033[0m")
                            display_game_state(self)  # Use the imported function
                            input("Press Enter to acknowledge blockers...")  # Acknowledge blockers
                    else:
                        blockers = [None] * len(attackers)

                    self.current_player.attack(self.opponent, self, attackers, blockers)
                    display_game_state(self)  # Use the imported function
                    input("Press Enter to acknowledge the attack...")  # Acknowledge the attack
                else:
                    print("No valid attackers.")
            elif action == "pass":
                self.game_log.append(f"\033[1;33m{self.current_player.name} passed the attack phase.\033[0m")
                break
            elif action == "help":
                print("Available actions: attack, pass, help")
                input("Press Enter to continue...")
            else:
                print("Invalid action.")
                self.game_log.append(f"\033[1;33m{self.current_player.name} chose an invalid action.\033[0m")

    def ai_attack_phase(self):
        attackers = self.current_player.ai_choose_attackers()
        if attackers:
            attacker_descriptions = [f"{self.current_player.board.index(a) + 1}: {str(a)}" for a in attackers]
            self.game_log.append(f"\033[3;31m{self.current_player.name} declared attackers: {', '.join(attacker_descriptions)}.\033[0m")
            display_game_state(self)  # Use the imported function
            input("Press Enter to acknowledge AI's attackers...")  # Acknowledge AI's attackers

            if self.opponent.board:
                blockers = self.opponent.ai_choose_blockers(attackers) if not self.opponent.is_human else self.opponent.choose_blockers(self, attackers)
                if blockers:
                    blocker_descriptions = [f"{self.opponent.board.index(b) + 1}: {str(b)}" if b else "X" for b in blockers]
                    self.game_log.append(f"\033[3;31m{self.opponent.name} declared blockers: {', '.join(blocker_descriptions)}.\033[0m")
                    display_game_state(self)  # Use the imported function
                    input("Press Enter to acknowledge blockers...")  # Acknowledge blockers
            else:
                blockers = [None] * len(attackers)

            self.current_player.attack(self.opponent, self, attackers, blockers)
            display_game_state(self)  # Use the imported function
            input("Press Enter to acknowledge AI's attack...")  # Acknowledge AI's attack
        else:
            self.game_log.append(f"\033[3;33mAI passed the attack phase.\033[0m")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    game = Game()
    game.play()