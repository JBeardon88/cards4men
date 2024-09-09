class Card:
    def __init__(self, name, attack, defense, cost, description, card_type):
        self.name = name
        self.base_attack = attack
        self.base_defense = defense
        self.attack = attack
        self.defense = defense
        self.cost = cost
        self.description = description
        self.card_type = card_type  # Make sure this is set correctly
        self.tapped = False
        self.summoning_sickness = True


    def reset_stats(self):
        self.attack = self.base_attack
        self.defense = self.base_defense

    def __str__(self):
        return f"{self.name} (ATK: {self.attack}, DEF: {self.defense}, E:{self.cost}) - {self.description}"

    def get_stats_display(self):
        return f"{self.name} ({self.attack}/{self.defense})"