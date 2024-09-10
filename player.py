import random
from card_data import create_deck, apply_card_effects, effect_handlers
from copy import deepcopy
from card import Card
from display import display_game_state
from copy import deepcopy
from functools import cmp_to_key
import colorama
colorama.init()  # Initialize colorama for Windows compatibility
from colorama import Fore, Style

class Player:
    def __init__(self, name, deck=None, is_human=True, game_log=None):
        self.name = name
        self.life = 20
        self.energy = 2
        self.energy_regen = 1  # Base energy regeneration rate
        self.deck = deck if deck is not None else create_deck("card_data.json")
        self.hand = []
        self.board = []
        self.environment = []
        self.attacked_this_turn = []
        self.is_human = is_human
        self.game_log = game_log if game_log is not None else []  # Ensure game_log is initialized
        self.damaged_opponent_this_turn = False  # Initialize the attribute
        self.equipment_cost_reduction = 0
        self.draw_initial_hand()
        self.sort_hand()  # Sort the initial hand

    def upkeep(self):
        self.untap_all()
        
        # Apply triggered effects
        for card in self.board + self.environment:
            apply_card_effects(self, card, None, phase="upkeep")
        
        old_energy = self.energy
        self.energy += self.energy_regen
        energy_gained = self.energy - old_energy
        print(f"Debug: {self.name} - Old energy: {old_energy}, Regen rate: {self.energy_regen}, New energy: {self.energy}")
        self.game_log.append(f"{self.name} untapped all cards and gained {Fore.GREEN}{energy_gained} energy{Style.RESET_ALL} (now at {self.energy}).")

    def draw_initial_hand(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            self.sort_hand()  # Sort the hand after drawing
            if self.is_human:
                self.game_log.append(f"{Fore.GREEN}{self.name} drew {card.name}.{Style.RESET_ALL}")
            return card
        return None

    def untap_all(self):
        for card in self.board:
            card.untap()

    def play_card(self, card_index, opponent):
        print(f"play_card called with card_index: {card_index}")
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            print(f"Playing card: {card.name}")
            if card.card_type == "equipment":
                card.cost = max(0, card.cost - self.equipment_cost_reduction)
            if card.cost <= self.energy:
                self.energy -= card.cost
                self.game_log.append(f"{self.name} played {card.name}.")
                if card.card_type == 'creature':
                    new_card = deepcopy(card)
                    new_card.reset_stats()
                    new_card.tap()  # Tap the creature immediately
                    self.board.append(new_card)
                    self.hand.pop(card_index)
                    return new_card
                elif card.card_type == 'spell':
                    self.hand.pop(card_index)
                    return card
                elif card.card_type == 'equipment':
                    if self.board:
                        if self.is_human:
                            return self.equip_card(card, card_index)
                        else:
                            return self.ai_equip_card(card, card_index)
                    else:
                        print("No creatures to equip the card to.")
                        self.energy += card.cost  # Refund energy if no valid target
                elif card.card_type == 'enchantment':
                    new_card = deepcopy(card)
                    self.environment.append(new_card)
                    self.hand.pop(card_index)
                    return new_card
            else:
                print("Not enough energy to play this card.")
        return None

    def cast_spell(self, card, opponent, target=None):
        print(f"cast_spell called with card: {card.name}")
        apply_card_effects(self, card, opponent)

    def attack(self, opponent, game, attackers=None, blockers=None):
        if attackers is None:
            if self.is_human:
                attackers = self.choose_attackers(game)
            else:
                attackers = self.ai_choose_attackers()

        if not attackers:
            print("No creatures to attack with.")
            return

        game.game_log.append(f"\033[1;31m{self.name} is attacking with {[str(a) for a in attackers]}.\033[0m")

        # Tap all attacking creatures and apply attack effects
        for attacker in attackers:
            attacker.tap()
            for effect in attacker.effects:
                if effect["trigger"] == "on_attack":
                    effect_type = effect["type"]
                    value = effect.get("value", 0)
                    if effect_type in effect_handlers:
                        effect_handlers[effect_type](self, opponent, value)

        if not opponent.board:
            for attacker in attackers:
                opponent.life -= attacker.attack
                self.damaged_opponent_this_turn = True  # Set the attribute to True if the opponent is damaged
                game.game_log.append(f"\033[1;31m{self.name} dealt {attacker.attack} damage to {opponent.name}.\033[0m")
                if hasattr(attacker, 'double_attack') and attacker.double_attack:
                    opponent.life -= attacker.attack
                    game.game_log.append(f"\033[1;31m{self.name} dealt an additional {attacker.attack} damage to {opponent.name} due to double attack.\033[0m")
        else:
            # Handle combat with blockers
            for attacker, blocker in zip(attackers, blockers):
                if blocker:
                    attacker.attack_creature(blocker)
                    if blocker.defense <= 0:
                        opponent.board.remove(blocker)
                    if attacker.defense <= 0:
                        self.board.remove(attacker)
                else:
                    opponent.life -= attacker.attack
                    self.damaged_opponent_this_turn = True  # Set the attribute to True if the opponent is damaged
                    game.game_log.append(f"\033[1;31m{self.name} dealt {attacker.attack} damage to {opponent.name}.\033[0m")
                    if hasattr(attacker, 'double_attack') and attacker.double_attack:
                        opponent.life -= attacker.attack
                        game.game_log.append(f"\033[1;31m{self.name} dealt an additional {attacker.attack} damage to {opponent.name} due to double attack.\033[0m")



    def choose_attackers(self, game):
        attackers = []
        while True:
            display_game_state(game)  # Use the imported function
            action = input(f"{self.name}, choose attackers (comma separated indices) or 'done' or 'all': ").strip().lower()
            if action == 'done':
                break
            elif action == 'all':
                attackers = [creature for creature in self.board if not creature.tapped and creature not in self.attacked_this_turn]
                break
            try:
                indices = list(map(lambda x: int(x) - 1, action.split(',')))
                valid_indices = [index for index in indices if 0 <= index < len(self.board) and not self.board[index].tapped and self.board[index] not in self.attacked_this_turn]
                if valid_indices:
                    attackers = [self.board[index] for index in valid_indices]
                    break
                else:
                    print("No valid attackers selected. Please choose valid indices.")
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        return attackers

    def choose_blockers(self, game, attackers):
        if not self.board:
            return [None] * len(attackers)  # No blockers if the player has no creatures

        blockers = [None] * len(attackers)
        indices = []

        while True:
            display_game_state(game)
            action = input(f"{self.name}, choose attackers to block (comma separated indices) or 'done': ").strip().lower()
            if action == 'done':
                return blockers
            try:
                indices = list(map(lambda x: int(x) - 1, action.split(',')))
                if all(0 <= index < len(attackers) for index in indices):
                    break
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        
        while True:
            display_game_state(game)
            action = input(f"{self.name}, assign blockers (comma separated indices) or 'done': ").strip().lower()
            if action == 'done':
                return blockers
            try:
                blocker_indices = list(map(lambda x: int(x) - 1, action.split(',')))
                if len(blocker_indices) == len(indices):
                    for blocker_index, attacker_index in zip(blocker_indices, indices):
                        if 0 <= blocker_index < len(self.board):
                            blockers[attacker_index] = self.board[blocker_index]
                        else:
                            print(f"Invalid blocker at index {blocker_index + 1}. Skipping.")
                    break
            except ValueError:
                print("Invalid input. Please enter comma separated indices.")
        return blockers

    def ai_choose_attackers(self):
        return [card for card in self.board if not card.tapped and card not in self.attacked_this_turn]

    def ai_choose_blockers(self, attackers):
        blockers = [None] * len(attackers)
        available_blockers = [creature for creature in self.board if not creature.tapped]
        
        for i, attacker in enumerate(attackers):
            if available_blockers and random.random() > 0.3:  # 70% chance to block if possible
                blocker = random.choice(available_blockers)
                blockers[i] = blocker
                available_blockers.remove(blocker)
        
        return blockers

    def reset_attacks(self):
        self.attacked_this_turn = []


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


    def choose_target_card(self):
        while True:
            try:
                target_index = int(input("Choose target creature index: ")) - 1
                if 0 <= target_index < len(self.board):
                    return self.board[target_index]
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")

    def end_phase(self):
        # Remove any end of turn effects here, but don't add energy
        pass

    def __str__(self):
        return f"{self.name} - Life: {self.life}, Energy: {self.energy}, Deck: {len(self.deck)} cards"

    def sort_hand(self):
        def card_sort_key(card):
            type_order = {'creature': 0, 'spell': 1, 'equipment': 2, 'enchantment': 3}
            return (type_order.get(card.card_type, 4), card.cost, card.name)
        
        self.hand.sort(key=card_sort_key)