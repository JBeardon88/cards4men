def display_game_state(self, full_log=False):
    self.clear_screen()
    print(f"\033[1;34m====================")
    print(f"      TURN {self.turn}      ")
    print(f"====================\033[0m")
    print(f"\033[1;31mAI - Life: {self.player2.life}, Energy: {self.player2.energy}, Deck: {len(self.player2.deck)} cards\033[0m")
    print("__________________________")
    print("GAMEBOARD HALF A")
    print(f"AI's Environment: {', '.join(str(card) for card in self.player2.environment)}")
    print("Opponent's board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player2.board)])
    print("GAMEBOARD HALF B")
    print("Your board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player1.board)])
    print(f"Human's Environment: {', '.join(str(card) for card in self.player1.environment)}")
    print("__________________________")
    print(f"\033[1;32mHuman - Life: {self.player1.life}, Energy: {self.player1.energy}, Deck: {len(self.player1.deck)} cards\033[0m")
    print("CARDS IN HAND:")
    print(f"{'Index':<6} {'Name':<20} {'Type':<4} {'ERG':<3} {'ATK/DEF':<7} {'Info':<50}")
    for i, card in enumerate(self.player1.hand):
        card_type = card.card_type[:3].upper()  # Truncate card type
        attack_defense = f"{card.attack}/{card.defense}"
        if card.card_type == 'equipment':
            attack_bonus = getattr(card, 'attack_bonus', 0)
            defense_bonus = getattr(card, 'defense_bonus', 0)
            attack_defense = f"{attack_bonus}/{defense_bonus}"
        info = card.description if len(card.description) <= 50 else card.description[:47] + "..."
        print(f"{i+1:<6} {card.name:<20} {card_type:<4} {card.cost:<3} {attack_defense:<7} {info:<50}")
    print("__________________________")
    print("\033[1;36mGame Log:\033[0m")
    if full_log:
        for log in self.game_log:
            print(log)
    else:
        for log in self.game_log[-10:]:
            print(log)
    print("__________________________")

