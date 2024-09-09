import random
from card_data import create_deck
from copy import deepcopy
from card import Card

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
            card = self.deck.pop(0)
            self.hand.append(card)
            return card
        return None

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