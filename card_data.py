from card import Card
import random

def create_deck():
    deck = [
        Card("Cyber Myconid", 2, 2, 1, "A cyber-enhanced mushroom warrior.", "creature"),
        Card("Spore Hacker", 3, 1, 2, "A hacker that uses spores to disrupt technology.", "creature"),
        Card("Fungal Drone", 1, 3, 1, "A drone controlled by fungal networks.", "creature"),
        Card("Mushroom Shaman", 2, 2, 2, "A shaman that channels the power of mushrooms.", "creature"),
        Card("Techno Shroom", 4, 4, 3, "A powerful mushroom infused with technology.", "creature"),
        Card("Energy Boost", 0, 0, 1, "Gain 2 energy.", "spell"),
        Card("Spore Burst", 0, 0, 2, "Deal 3 damage to the opponent.", "spell"),
        Card("Fungal Shield", 0, 0, 1, "Equip to a creature to give it +1 DEF.", "equipment"),
        Card("Cyber Blade", 0, 0, 2, "Equip to a creature to give it +2 ATK.", "equipment"),
        Card("Land Enchantment", 0, 0, 1, "Gives +0.5 energy per turn.", "enchantment"),
    ] * 3
    random.shuffle(deck)
    return deck