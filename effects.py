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
        # You'll need to implement a way to track if the opponent was damaged this turn
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

def regenerate_health(card, value):
    card.defense = min(card.defense + value, card.max_defense)

def grant_double_attack(card):
    card.double_attack = True

def destroy_enemy_enchantment(player, opponent):
    if opponent.enchantments:
        destroyed_enchantment = opponent.enchantments.pop()
        player.game_log.append(f"{player.name} destroyed {opponent.name}'s enchantment: {destroyed_enchantment.name}")

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

# Add more generic effects as needed