import random
from card_data import create_deck
from copy import deepcopy
from card import Card
from display import display_game_state

class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.life = 20
        self.energy = 2
        self.deck = create_deck()
        self.hand = []
        self.board = []
        self.environment = []
        self.draw_initial_hand()
        self.attacked_this_turn = []
        self.is_human = is_human

    def draw_initial_hand(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            return card
        return None
    
    def untap_all(self):
        for card in self.board:
            card.untap()

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.cost <= self.energy:
                self.energy -= card.cost
                if card.card_type == 'creature':
                    new_card = deepcopy(card)
                    new_card.reset_stats()
                    self.board.append(new_card)
                    self.hand.pop(card_index)
                    return new_card
                elif card.card_type == 'spell':
                    self.cast_spell(card, opponent)
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
                    self.environment.append(card)
                    self.hand.pop(card_index)
                    return card
            else:
                print("Not enough energy to play this card.")
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

        # Tap all attacking creatures
        for attacker in attackers:
            attacker.tap()

        if not opponent.board:
            for attacker in attackers:
                opponent.life -= attacker.attack
                self.attacked_this_turn.append(attacker)
            game.game_log.append(f"\033[1;31m{self.name} attacked {opponent.name} directly with {len(attackers)} creatures.\033[0m")
        else:
            if blockers is None:
                if opponent.is_human:
                    blockers = opponent.choose_blockers(game, attackers)
                else:
                    blockers = opponent.ai_choose_blockers(attackers)

            for attacker, blocker in zip(attackers, blockers):
                if blocker and not blocker.tapped:  # Check if blocker is still untapped
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
                    if blocker:
                        game.game_log.append(f"\033[1;31m{blocker.name} was unable to block {attacker.name}.\033[0m")

            game.game_log.append(f"\033[1;31m{self.name} attacked {opponent.name} with {len(attackers)} creatures, {len([b for b in blockers if b and not b.tapped])} were blocked.\033[0m")




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
            game.display_game_state()
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
            game.display_game_state()
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
        if not self.board:
            return [None] * len(attackers)  # No blockers if the AI has no creatures

        blockers = [None] * len(attackers)
        available_blockers = [card for card in self.board if not card.tapped]
        
        for i, attacker in enumerate(attackers):
            if available_blockers and random.random() > 0.3:  # 70% chance to block if possible
                blocker = random.choice(available_blockers)
                blockers[i] = blocker
                available_blockers.remove(blocker)
        
        return blockers

    def reset_attacks(self):
        self.attacked_this_turn = []



    def end_phase(self):
        # Perform any end-of-turn actions here
        self.attacked_this_turn = []  # Reset the list of creatures that attacked this turn
        # Apply environment effects
        for card in self.environment:
            if card.name == "Land Enchantment":
                self.energy += 0.5

    def __str__(self):
        return f"{self.name} - Life: {self.life}, Energy: {self.energy}, Deck: {len(self.deck)} cards"