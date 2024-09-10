import os
import time
import random
from player import Player
from display import display_game_state  # Import the display_game_state function

class Game:
    def __init__(self):
        self.game_log = []  # Initialize game_log before creating players
        self.player1 = Player("Human", game_log=self.game_log)
        self.player2 = Player("AI", is_human=False, game_log=self.game_log)
        self.current_player = self.player1
        self.opponent = self.player2
        self.turn = 1
        self.phase = "upkeep"
        self.showing_game_log = False

    def play(self):
        while self.player1.life > 0 and self.player2.life > 0:
            if not self.showing_game_log:
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
        input("Press Enter to continue to AI's summon phase...")
        self.ai_summon_phase("summon1")
        input("Press Enter to continue to AI's attack phase...")
        self.ai_attack_phase()
        input("Press Enter to continue to AI's second summon phase...")
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
            action = input(f"{phase_name.capitalize()} Phase - Choose action: play, pass, help, info, spell, gamelog: ").strip().lower()
            if action == "play":
                try:
                    card_index = int(input("Choose card index to play: ")) - 1
                    played_card = self.current_player.play_card(card_index, self.opponent)
                    if played_card:
                        if played_card.card_type == 'creature':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} played {played_card.name}.\033[0m")
                        elif played_card.card_type == 'spell':
                            if played_card.name == "Gun Blast":
                                target_index = int(input("Choose target creature index: ")) - 1
                                if 0 <= target_index < len(self.opponent.board):
                                    target = self.opponent.board[target_index]
                                    self.current_player.cast_spell(played_card, self.opponent, target)
                                else:
                                    print("Invalid target index.")
                                    self.current_player.energy += played_card.cost  # Refund energy if no valid target
                            else:
                                self.current_player.cast_spell(played_card, self.opponent)
                            self.game_log.append(f"\033[1;32m{self.current_player.name} cast {played_card.name}.\033[0m")
                        elif played_card.card_type == 'equipment':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} equipped {played_card.name}.\033[0m")
                        elif played_card.card_type == 'enchantment':
                            self.game_log.append(f"\033[1;32m{self.current_player.name} cast {played_card.name}.\033[0m")
                        display_game_state(self)  # Update the display immediately
                    else:
                        print("Failed to play the card.")
                except ValueError:
                    print("Invalid input. Please enter a valid card index.")
            elif action == "pass":
                self.game_log.append(f"\033[1;33m{self.current_player.name} passed the {phase_name} phase.\033[0m")
                break
            elif action == "help":
                print("Available actions: play, pass, help, info, spell, gamelog")
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
            elif action == "spell":
                self.cast_spell_during_opponent_turn()
            elif action == "gamelog":
                self.showing_game_log = True
                self.show_game_log()
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
                if played_card.card_type == 'spell' and played_card.name == "Gun Blast":
                    if self.opponent.board:
                        target = random.choice(self.opponent.board)
                        self.current_player.cast_spell(played_card, self.opponent, target)
                else:
                    self.current_player.cast_spell(played_card, self.opponent)
                self.game_log.append(f"\033[3;32mAI played {played_card.name}.\033[0m")
                display_game_state(self)  # Update the display immediately
                self.check_for_spell_casting()  # Check for spell casting opportunity
        else:
            self.game_log.append(f"\033[3;33mAI passed the {phase_name} phase.\033[0m")

    def attack_phase(self):
        while True:
            display_game_state(self)  # Use the imported function
            action = input("Attack Phase - Choose action: attack, pass, help, spell, gamelog: ").strip().lower()
            if action == "attack":
                attackers = self.current_player.choose_attackers(self)
                if attackers:
                    attacker_descriptions = [f"{self.current_player.board.index(a) + 1}: {str(a)}" for a in attackers]
                    self.game_log.append(f"\033[1;31m{self.current_player.name} declared attackers: {', '.join(attacker_descriptions)}.\033[0m")
                    display_game_state(self)  # Use the imported function
                    self.check_for_spell_casting()  # Check for spell casting opportunity

                    if self.opponent.board:
                        blockers = self.opponent.choose_blockers(self, attackers)
                        if blockers:
                            blocker_descriptions = [f"{self.opponent.board.index(b) + 1}: {str(b)}" if b else "X" for b in blockers]
                            self.game_log.append(f"\033[1;31m{self.opponent.name} declared blockers: {', '.join(blocker_descriptions)}.\033[0m")
                            display_game_state(self)  # Use the imported function
                            self.check_for_spell_casting()  # Check for spell casting opportunity
                    else:
                        blockers = [None] * len(attackers)

                    self.current_player.attack(self.opponent, self, attackers, blockers)
                    display_game_state(self)  # Update the display immediately
                    self.check_for_spell_casting()  # Check for spell casting opportunity
                else:
                    print("No valid attackers.")
            elif action == "pass":
                self.game_log.append(f"\033[1;33m{self.current_player.name} passed the attack phase.\033[0m")
                break
            elif action == "help":
                print("Available actions: attack, pass, help, spell, gamelog")
                input("Press Enter to continue...")
            elif action == "spell":
                self.cast_spell_during_opponent_turn()
            elif action == "gamelog":
                self.showing_game_log = True
                self.show_game_log()
            else:
                print("Invalid action.")
                self.game_log.append(f"\033[1;33m{self.current_player.name} chose an invalid action.\033[0m")

    def ai_attack_phase(self):
        attackers = self.current_player.ai_choose_attackers()
        if attackers:
            self.game_log.append(f"\033[1;31mAI declared attackers: {[str(a) for a in attackers]}.\033[0m")
            display_game_state(self)  # Use the imported function
            input("Press Enter to continue to AI's attack resolution...")
            self.check_for_spell_casting()  # Check for spell casting opportunity

            if self.opponent.board:
                blockers = self.opponent.ai_choose_blockers(attackers)
                if blockers:
                    self.game_log.append(f"\033[1;31mAI declared blockers: {[str(b) for b in blockers]}.\033[0m")
                    display_game_state(self)  # Use the imported function
                    input("Press Enter to continue to AI's block resolution...")
                    self.check_for_spell_casting()  # Check for spell casting opportunity
            else:
                blockers = [None] * len(attackers)

            self.current_player.attack(self.opponent, self, attackers, blockers)
            display_game_state(self)  # Update the display immediately
            input("Press Enter to continue to AI's post-attack phase...")
            self.check_for_spell_casting()  # Check for spell casting opportunity
        else:
            self.game_log.append(f"\033[1;33mAI passed the attack phase.\033[0m")

    def check_for_spell_casting(self):
        # Placeholder for checking if a spell can be cast during the opponent's turn
        pass

    def cast_spell_during_opponent_turn(self):
        # Placeholder for casting a spell during the opponent's turn
        pass

    def show_game_log(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Full Game Log:")
        for entry in self.game_log:
            print(entry)
        input("Press Enter to return to the game...")
        self.showing_game_log = False
        display_game_state(self)  # Use the imported function

    
    
    
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
if __name__ == "__main__":
    game = Game()
    game.play()