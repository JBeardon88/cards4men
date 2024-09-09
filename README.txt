# Cards4Men

Welcome to **Cards4Men**, a fun and strategic card game where you battle with cyber-enhanced mushroom warriors, hackers, and shamans! Equip your creatures, cast powerful spells, and outsmart your opponent to win the game.

## Installation

Follow these steps to install and run the game:

1. **Clone the Repository**:
    
    git clone https://github.com/yourusername/cards4men.git
    cd cards4men
    

2. **Install Dependencies**: use terminal / command prompt / powershell to run stuff
    
    pip install -r requirements.txt
    

3. **Run the Game**:
    
    python game.py
    

## How to Play

It's a rip off of Magic: The Gathering, so same shit way less features and no artists.

### Objective

Reduce your opponent's life to 0 by attacking with your creatures and casting powerful spells.

### Game Phases

1. **Draw Phase**: Draw a card from your deck.
2. **Summon Phase 1**: Play creatures, spells, or equipment from your hand.
3. **Attack Phase**: Choose your attackers and attack your opponent.
4. **Summon Phase 2**: Play additional creatures, spells, or equipment.
5. **End Phase**: End your turn and pass to your opponent.

### Commands

- **Play**: Play a card. During the summon phases, you can play a card by entering its index number.
- **Attack**: Attack with your creatures. During the attack phase, choose your attackers by entering their index numbers (comma-separated).
- **Block**: Block with your creatures. If your opponent attacks, choose your blockers by entering their index numbers (comma-separated).
- **Pass**: Skip the current phase by typing `pass`.
- **Help**: Get a list of available commands by typing `help`.

### Card Types

- **Creatures**: These cards can attack and block. They have attack (ATK) and defense (DEF) values.
- **Spells**: These cards have immediate effects, such as dealing damage or gaining energy.
- **Equipment**: These cards enhance your creatures. You must choose a creature to equip them to.

### Example Turn

1. **Summon Phase 1**:
    ```
    Choose action: play, pass, help: play
    Enter card index to play: 1
    ```

2. **Attack Phase**:
    ```
    Choose attackers (comma separated indices) or 'done': 1,2
    ```

3. **Summon Phase 2**:
    ```
    Choose action: play, pass, help: pass
    ```

4. **End Phase**:
    ```
    Your turn ends. Opponent's turn begins.
    ```
