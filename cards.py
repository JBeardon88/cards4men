import random
import uuid

class Card:
    def __init__(self, name, attack=0, defense=0, cost=0, card_type='creature', description=''):
        self.id = uuid.uuid4()  # Unique identifier for each card instance
        self.name = name
        self.attack = attack
        self.defense = defense
        self.cost = cost
        self.card_type = card_type
        self.description = description

    def __str__(self):
        return f"{self.name} (ATK: {self.attack}, DEF: {self.defense}, E:{self.cost}) - {self.description}"

def create_deck():
    deck = [
        Card("Cyber Myconid", 2, 2, 1, 'creature', "A cyber-enhanced mushroom warrior."),
        Card("Spore Hacker", 3, 1, 2, 'creature', "A hacker that uses spores to disrupt technology."),
        Card("Fungal Drone", 1, 3, 1, 'creature', "A drone controlled by fungal networks."),
        Card("Mushroom Shaman", 2, 2, 2, 'creature', "A shaman that channels the power of mushrooms."),
        Card("Techno Shroom", 4, 4, 3, 'creature', "A powerful mushroom infused with technology."),
        Card("Energy Boost", 0, 0, 1, 'spell', "Gain 2 energy."),
        Card("Spore Burst", 0, 0, 2, 'spell', "Deal 3 damage to the opponent."),
        Card("Fungal Shield", 0, 0, 1, 'equipment', "Equip to a creature to give it +1 DEF."),
        Card("Cyber Blade", 0, 0, 2, 'equipment', "Equip to a creature to give it +2 ATK.")
    ] * 3
    random.shuffle(deck)
    return deck