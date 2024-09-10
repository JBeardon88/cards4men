import json
import random
import os
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
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, 'card_sets', file_path)
    
    with open(full_path, 'r') as file:
        card_data = json.load(file)
    
    deck = [Card(**random.choice(card_data)) for _ in range(30)]
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
    "destroy_enemy_equipment_or_enchantment": destroy_enemy_equipment_or_enchantment,
    "reduce_equipment_cost": reduce_equipment_cost,
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
                if effect_type == "conditional_gain_energy":
                    effect_function(player, opponent, value, condition)
                elif effect_type == "destroy_enemy_enchantment":
                    effect_function(player, opponent)
                elif effect_type == "deal_damage":
                    effect_function(player, opponent, value)
                elif target == "self":
                    effect_function(card, value)
                elif target == "creature" and player.board:
                    target_card = player.choose_target_card()
                    if effect_type == "grant_double_attack":
                        effect_function(target_card)
                    else:
                        effect_function(target_card, value)
                elif target == "enemy_creature" and opponent.board:
                    target_card = opponent.choose_target_card()
                    effect_function(target_card, value)
                else:
                    effect_function(player, value)
                
                print(f"Applied {effect_type}")
            else:
                player.game_log.append(f"{Fore.RED}{player.name} cast {card.name}, but no effect was implemented for {effect_type}.{Style.RESET_ALL}")