import os
from colorama import Fore, Style

def display_game_state(game):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("====================")
    print(f"{Fore.CYAN}      TURN {game.turn}      {Style.RESET_ALL}")
    print("====================")
    print(f"{Fore.RED}AI - Life: {game.player2.life}, Energy: {game.player2.energy}, Deck: {len(game.player2.deck)} cards{Style.RESET_ALL}")
    print("__________________________")
    print("AI's Environment:")
    print("__________________________")
    display_environment(game.player2.environment)
    print("__________________________")
    print("GAMEBOARD HALF A")
    print("__________________________")
    display_board(game.player2.board)
    print("__________________________")
    print("GAMEBOARD HALF B")
    print("__________________________")
    display_board(game.player1.board)
    print("__________________________")
    print("Human's Environment:")
    print("__________________________")
    display_environment(game.player1.environment)
    print("__________________________")
    print(f"{Fore.GREEN}Human - Life: {game.player1.life}, Energy: {game.player1.energy}, Deck: {len(game.player1.deck)} cards{Style.RESET_ALL}")
    print("CARDS IN HAND:")
    display_hand(game.player1.hand)
    print("__________________________")
    print("Game Log:")
    for entry in game.game_log[-5:]:
        print(entry)
    print("__________________________")

def display_board(board):
    max_width = 20
    card_lines = []
    for idx, card in enumerate(board, 1):
        card_name = f"~~{card.name[:max_width]}~~" if card.tapped else card.name[:max_width]
        card_info = [
            f"| {idx}: {card_name}",
            f"| Type: {card.card_type[:3]}",
            f"| ATK/DEF: {card.attack}/{card.defense}",
            f"| Equ: {card.equipment.name[:max_width] if card.equipment else 'None'}"
        ]
        card_lines.append(card_info)

    # Transpose the card lines to display them side by side
    for line_idx in range(4):
        for card_info in card_lines:
            print(f"{card_info[line_idx]:<{max_width}}", end=" ")
        print()

def display_environment(environment):
    max_width = 20
    card_lines = []
    for idx, card in enumerate(environment, 1):
        card_info = [
            f"| {idx}: {card.name[:max_width]}",
            f"| Type: {card.card_type[:3]}",
            f"| ATK/DEF: {card.attack}/{card.defense}",
            f"| Equ: {card.equipment.name[:max_width] if card.equipment else 'None'}"
        ]
        card_lines.append(card_info)

    # Transpose the card lines to display them side by side
    for line_idx in range(4):
        for card_info in card_lines:
            print(f"{card_info[line_idx]:<{max_width}}", end=" ")
        print()

def display_hand(hand):
    print("Index  Name                 Type ERG ATK/DEF Info")
    for idx, card in enumerate(hand, 1):
        print(f"{idx:<6} {card.name[:20]:<20} {card.card_type[:3]:<4} {card.cost:<3} {card.attack}/{card.defense:<5} {card.description[:30]}...")

