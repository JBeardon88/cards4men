def display_game_state(self, full_log=False):
    self.clear_screen()
    print(f"\033[1;34m====================")
    print(f"      TURN {self.turn}      ")
    print(f"====================\033[0m")
    print(f"\033[1;31mAI - Life: {self.player2.life}, Energy: {self.player2.energy}, Deck: {len(self.player2.deck)} cards\033[0m")
    print("__________________________")
    print("GAMEBOARD HALF A")
    print(f"Environment: {[str(card) for card in self.opponent.environment]}")
    print("Opponent's board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player2.board)])
    print("GAMEBOARD HALF B")
    print("Your board:", [f"{i+1}: {card.get_stats_display()}" for i, card in enumerate(self.player1.board)])
    print(f"Environment: {[str(card) for card in self.current_player.environment]}")
    print("__________________________")
    print(f"\033[1;32mHuman - Life: {self.player1.life}, Energy: {self.player1.energy}, Deck: {len(self.player1.deck)} cards\033[0m")
    print("CARDS IN HAND:")
    print(f"{'Index':<6} {'Name':<20} {'Type':<10} {'Energy Cost':<12} {'Attack/Def':<15} {'Info':<50}")
    for i, card in enumerate(self.player1.hand):
        attack_defense = f"{card.attack}/{card.defense}"
        if card.card_type == 'equipment':
            attack_bonus = getattr(card, 'attack_bonus', 0)
            defense_bonus = getattr(card, 'defense_bonus', 0)
            attack_defense = f"{attack_bonus}/{defense_bonus}"
        info = card.description if len(card.description) <= 50 else card.description[:47] + "..."
        print(f"{i+1:<6} {card.name:<20} {card.card_type:<10} {card.cost:<12} {attack_defense:<15} {info:<50}")
    print("__________________________")
    print("Game Log:")
    if full_log:
        for log in self.game_log:
            print(log)
    else:
        for log in self.game_log[-10:]:
            print(log)
    print("__________________________")