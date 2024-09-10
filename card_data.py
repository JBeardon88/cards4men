import json
import random
from copy import deepcopy
from card import Card
from effects import draw_cards, deal_damage, gain_energy, lose_life, gain_attack, gain_defense, lose_attack, tap_creature, prevent_untap
from effects import conditional_draw_cards, conditional_gain_attack, reduce_equipment_cost, regenerate_health, grant_double_attack 
from effects import destroy_enemy_enchantment, destroy_enemy_equipment_or_enchantment, conditional_remove_summoning_sickness 
from effects import deal_damage_all_enemy_creatures, increase_energy_regen, conditional_gain_energy
from colorama import Fore, Style

def load_card_data(file_path):
    with open(file_path, 'r') as file:
        card_data = json.load(file)
    return [Card(**card) for card in card_data]

def create_deck(file_path):
    card_data = load_card_data(file_path)
    selected_cards = random.sample(card_data, 15)  # Select 15 random cards
    deck = [deepcopy(card) for card in selected_cards * 2]  # Create unique instances of each card
    random.shuffle(deck)
    return deck

# Dictionary mapping effect types to their handler functions
effect_handlers = {
    "draw_cards": draw_cards,
    "deal_damage": deal_damage,
    "gain_energy": gain_energy,
    "lose_life": lose_life,
    "gain_attack": gain_attack,
    "gain_defense": gain_defense,
    "lose_attack": lose_attack,
    "tap_creature": tap_creature,
    "prevent_untap": prevent_untap,
    # new handlers for Technobros  - Technobros   
    "conditional_draw_cards": conditional_draw_cards,
    "conditional_gain_attack": conditional_gain_attack,
    "reduce_equipment_cost": reduce_equipment_cost,
    "regenerate_health": regenerate_health,
    "grant_double_attack": grant_double_attack,
    "destroy_enemy_enchantment": destroy_enemy_enchantment,
    "destroy_enemy_equipment_or_enchantment": destroy_enemy_equipment_or_enchantment,
    "conditional_remove_summoning_sickness": conditional_remove_summoning_sickness,
    "deal_damage_all_enemy_creatures": deal_damage_all_enemy_creatures,
    "increase_energy_regen": increase_energy_regen,
    "conditional_gain_energy": conditional_gain_energy,
    # Other new handlers...
}

def apply_card_effects(player, card, opponent, phase=None):
    print(f"Applying effects for card: {card.name}")
    if card.effects:
        for effect in card.effects:
            print(f"Processing effect: {effect}")
            effect_type = effect["type"]
            value = effect.get("value", 0)
            target = effect.get("target", None)
            trigger = effect.get("trigger", None)
            condition = effect.get("condition", None)

            # Check if the effect should be triggered in the current phase
            if trigger and phase and trigger != phase:
                continue

            if effect_type in effect_handlers:
                effect_function = effect_handlers[effect_type]
                
                # Determine the correct arguments based on the effect's signature
                if "player" in effect_function.__code__.co_varnames:
                    if "opponent" in effect_function.__code__.co_varnames:
                        if "condition" in effect_function.__code__.co_varnames:
                            effect_function(player, opponent, value, condition)
                        else:
                            effect_function(player, opponent, value)
                    else:
                        effect_function(player, value)
                elif target == "creature" and player.board:
                    target_card = player.board[0]  # Simplified; you may want to select a specific card
                    effect_function(target_card, value)
                elif target == "enemy_creature" and opponent.board:
                    target_card = opponent.board[0]  # Simplified; you may want to select a specific card
                    effect_function(target_card, value)
                else:
                    effect_function(card, value)
                
                print(f"Applied {effect_type}")
            else:
                player.game_log.append(f"{Fore.RED}{player.name} cast {card.name}, but no effect was implemented for {effect_type}.{Style.RESET_ALL}")