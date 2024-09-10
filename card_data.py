import json
import random
from card import Card

def load_card_data(file_path):
    with open(file_path, 'r') as file:
        card_data = json.load(file)
    return [Card(**card) for card in card_data]

def create_deck(file_path):
    deck = load_card_data(file_path) * 3
    random.shuffle(deck)
    return deck