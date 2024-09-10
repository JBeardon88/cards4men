from colorama import Fore, Style

def draw_cards(player, num_cards):
    for _ in range(num_cards):
        player.draw_card()
    player.game_log.append(f"{player.name} drew {num_cards} card(s).")

def deal_damage(player, opponent, damage):
    opponent.life -= damage
    player.game_log.append(f"{player.name} dealt {damage} damage to {opponent.name}. Remaining life: {opponent.life}")

def gain_energy(player, energy):
    player.energy += energy
    player.game_log.append(f"{player.name} gained {energy} energy.")

def lose_life(player, life):
    player.life -= life
    player.game_log.append(f"{player.name} lost {life} life.")

def gain_attack(card, value):
    card.attack += value

def gain_defense(card, value):
    card.defense += value

def lose_attack(card, value):
    card.attack -= value

def tap_creature(card):
    card.tap()

def prevent_untap(card):
    card.prevent_untap = True

def conditional_gain_energy(player, opponent, value, condition):
    if condition == "damaged_opponent":
        if player.damaged_opponent_this_turn:
            player.energy += value
            player.game_log.append(f"{player.name} gained {value} energy from Energy Bloom.")

# Add these new functions - Technobros  

def conditional_draw_cards(player, opponent, num_cards, condition):
    if condition == "control_more_than_3_creatures" and len(player.board) > 3:
        draw_cards(player, num_cards)

def conditional_gain_attack(card, value, condition):
    if condition == "equipped" and card.equipment:
        gain_attack(card, value)

def reduce_equipment_cost(player, value):
    player.equipment_cost_reduction = value
    print(f"{player.name}'s equipment costs are reduced by {value} while Tactical Drone is on the field.")

def regenerate_health(card, value):
    card.defense = min(card.defense + value, card.max_defense)

def grant_double_attack(target_card):
    target_card.double_attack = True
    print(f"{target_card.name} can now attack twice this turn.")

def destroy_enemy_enchantment(player, opponent):
    if opponent.environment:
        print("Opponent's environment cards:")
        for idx, card in enumerate(opponent.environment, 1):
            print(f"{idx}: {card.name} (ATK: {card.attack}, DEF: {card.defense}, Cost: {card.cost}) - {card.description}")
        
        while True:
            try:
                target_index = int(input("Choose an enemy enchantment to destroy (index): ")) - 1
                if 0 <= target_index < len(opponent.environment):
                    destroyed_card = opponent.environment.pop(target_index)
                    print(f"Destroyed {destroyed_card.name}")
                    player.game_log.append(f"{player.name} destroyed {opponent.name}'s {destroyed_card.name}.")
                    break
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
    else:
        print("No enemy enchantments to destroy.")
        player.game_log.append(f"{player.name} tried to destroy an enemy enchantment, but there were none.")

def destroy_enemy_equipment_or_enchantment(player, opponent):
    if opponent.equipment:
        destroyed_item = opponent.equipment.pop()
        player.game_log.append(f"{player.name} destroyed {opponent.name}'s equipment: {destroyed_item.name}")
    elif opponent.enchantments:
        destroyed_item = opponent.enchantments.pop()
        player.game_log.append(f"{player.name} destroyed {opponent.name}'s enchantment: {destroyed_item.name}")

def conditional_remove_summoning_sickness(card, condition):
    if condition == "equipped" and card.equipment:
        card.summoning_sickness = False

def deal_damage_all_enemy_creatures(player, opponent, damage):
    for creature in opponent.board:
        creature.defense -= damage
    opponent.remove_destroyed_creatures()
    player.game_log.append(f"{player.name} dealt {damage} damage to all of {opponent.name}'s creatures.")

def increase_energy_regen(player, value):
    if not hasattr(player, 'energy_regen_increased'):
        player.energy_regen += value
        player.energy_regen_increased = True
        print(f"Debug: Increased {player.name}'s energy regen by {value}. New regen rate: {player.energy_regen}")
        player.game_log.append(f"{player.name}'s energy regeneration {Fore.GREEN}increased by {value}{Style.RESET_ALL}.")
    else:
        print(f"Debug: {player.name}'s energy regen already increased. Current rate: {player.energy_regen}")


def destroy_enemy_equipment_or_enchantment(player, opponent):
    if opponent.environment:
        target_index = int(input("Choose an enemy enchantment to destroy (index): ")) - 1
        if 0 <= target_index < len(opponent.environment):
            destroyed_card = opponent.environment.pop(target_index)
            print(f"Destroyed {destroyed_card.name}")
            player.game_log.append(f"{player.name} destroyed {opponent.name}'s {destroyed_card.name}.")
    else:
        print("No enemy enchantments to destroy.")
        player.game_log.append(f"{player.name} tried to destroy an enemy enchantment, but there were none.")

# Add more generic effects as needed