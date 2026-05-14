# ====================================================================
# FILE: dev_guide.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR: Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# THE INTEGRATION ROADMAP
# GOAL: Show how to safely extend the Dungeon Crawler engine.
# ====================================================================

import random 
import os  # Required for the screen clearing logic

try:
    from engine import Hero, Monster, Ability
    ENGINE_LOADED = True
except ImportError:
    ENGINE_LOADED = False
    print("WARNING: 'engine.py' not found in this folder.")
    print("The guide will continue using 'mock' logic for display.\n")

# ==================================== # 
# EXAMPLE 1: ADDING A NEW HERO ROLE    #
# ==================================== #
class Knight(Hero if ENGINE_LOADED else object):
    def __init__(self, name, health, gold):
        # DATA RULE: Force lowercase and underscores for engine compatibility
        self.name = name.lower().replace(" ", "_")
        
        # Initialize engine attributes
        if ENGINE_LOADED:
            super().__init__(self.name, health, gold, role="Knight")
            self.gold += 20
        else:
            self.role = "Knight"
            self.health = health
            self.gold = gold + 20
            
        # TRACKING RULE: Track progress like the game engine
        self.rooms_cleared = 0

    def attack(self, target):
        # UI RULE: Use .replace('_', ' ').title() for display
        display_name = self.name.replace("_", " ").title()
        print(f"\n{display_name} strikes with Magic Sword!")
        if ENGINE_LOADED:
            return super().attack(target)

# ================================= #
# EXAMPLE 2.1: ADDING A NEW ABILITY   #
# ================================= #
class ThiefAbility(Ability if ENGINE_LOADED else object):
    def modify_health(self, health): return health
    def modify_damage(self, damage): return damage - 2
    def get_name(self): return "Thief"

    def on_attack(self, monster, target, damage_dealt):
        if hasattr(target, 'gold') and target.gold >= 5:
            target.gold -= 5
            
            # UI RULE: Display the theft clearly to the player
            target_display = target.name.replace("_", " ").title()
            print(f"!!! {monster.name} stole 5 gold from {target_display}! !!!")
            return True
        return False

# ============================================================================
# MOCK-READY MONSTER CLASS (For Integration Testing)
# ============================================================================
class MockMonster(Monster if ENGINE_LOADED else object):
    def __init__(self, name, health, gold, strength, ability=None):
        if ENGINE_LOADED:
            super().__init__(name, health, gold, strength, ability)
        else:
            self.name = name
            self.health = health
            self.gold = gold
            self.strength = strength
            self.ability = ability

# =======================================================================
# EXAMPLE 2.2: THE SPAWN WEIGHT SYSTEM (Dictionary)
# =======================================================================
# ENGINE LOGIC: The game.py uses a Dictionary for the weights. Why we
# use Dictonary instead of a list?
# -----------------------------------------------------------------------
# 1. SCALABILITY: Adding a "Treasure Room" only requires one line.
#
# 2. READABILITY: No matching separate lists by index as it would
# become a nightmare to maintain if we used list and it grew larger.
#
# 3. SAFETY: .keys() and .values() keep names and weights paired.
# =======================================================================
def get_random_event(weight_dict):
    selection = random.choices(
        population=list(weight_dict.keys()), 
        weights=list(weight_dict.values()),
        k=1
    )
    return selection[0]

def simulate_game_rooms(player, iterations=10):
    # Matches the balance dictionary in game.py
    room_chances = {
        "monster": 57, 
        "merchant": 18, 
        "empty": 25
    }
    
    print(f"\n--- Simulating {iterations} Rooms (Dictionary Weights) ---")
    results = {"monster": 0, "merchant": 0, "empty": 0}
    
    for i in range(1, iterations + 1):
        picked = get_random_event(room_chances)
        results[picked] += 1
        
        # TRACKING RULE: Update hero progress per room
        player.rooms_cleared += 1
        print(f" Room {player.rooms_cleared}: {picked.title()}")
        
    print(f"\nFinal Distribution: {results}")

# ============================================================================
# EXAMPLE 2.3: IDENTITY VS. RANDOMNESS (The "Special Case" Rule)
# ============================================================================
# THE RULE: Some monsters have 'Fixed Identities.' While a 'Wolf' might 
# randomly be 'Brute' or 'Explosive,' a 'Vampire' should always have 
# Life Drain to match its signature character.
#
# WHY DO THIS? 
# It avoids a "Logic Mismatch." If a player fights a Vampire and it 
# just explodes like a bomb instead of biting them, it breaks the "flavor" 
# of the world. Locking an Ability to a Name ensures the game logic 
# matches the player's expectations.
#
# HOW TO ADD A NEW "GIMMICK":
# 1. Define the Ability in engine.py (The Brain):
#    class StoneSkinAbility(Ability):
#        def modify_health(self, health): return health + 50
#        def modify_damage(self, damage): return damage
#        def get_name(self): return "Stone Skin"
#
# 2. Import the new Ability at the top of game.py:
#    from engine import (Hero, Monster, VampireAbility, StoneSkinAbility, ...)
#
# 3. Add the Monster to the monster_vault dictionary in game.py:
#    monster_vault = {
#        "Vampire":     {"hp": 40, "gold": 50, "dmg": 10},
#        "Stone Golem": {"hp": 60, "gold": 40, "dmg": 8}
#    }
#
# 4. In game.py (The Workhorse) within get_random_monster, use 'elif':
#
#    if name == "Vampire":
#        ability = VampireAbility()
#
#    # Like the Vampire, we pass the specific ability into the Monster
#    elif name == "Stone Golem":
#        ability = StoneSkinAbility() 
#    else:
#        ability = random.choice([NoAbility(), BruteAbility()...])
#
#    # The engine then creates the monster with that specific identity:
#    # return Monster(name, hp, gold, dmg, ability)
# ============================================================================

# ============================================================================
# EXAMPLE 2.4: ADDING A NEW ROOM TYPE (The Integration Roadmap)
# ============================================================================
# THE RULE: To add a new room event, you must update the balance settings 
# and the main game loop. This follows the "Barnaby" Merchant pattern.
#
# WHY DO THIS? 
# 1. CONSISTENCY: By following the Merchant pattern in game.py, you keep 
#    the interaction logic (inputs/prints) in the main loop while keeping 
#    the engine.py focused on core entity math.
#
# 2. SCALABILITY: Using a dictionary for probabilities allows you to 
#    easily add a "Treasure Room" or "Trap Room" without breaking the math.
#
# HOW TO ADD A NEW ROOM:
# 1. Update ROOM_CHANCES in game.py (The Probability):
#    # Adjust weights to stay at 100 total - using Vertical Alignment
#    ROOM_CHANCES = {
#        "monster": 55,
#        "merchant": 15,
#        "empty": 20,
#        "treasure": 10  # <--- Step 1: Add the probability
#    }
#
# 2. Update the Exploration Loop in game.py (The Event):
#    # Add a new 'elif' block to handle the interaction logic:
#    elif event == "treasure":
#        # Like the Merchant, we handle the UI and gold directly here:
#        loot = random.randint(10, 30)
#        player.gold += loot
#        print(f"\n --- TREASURE ---")
#        print(f"You found a dusty chest containing {loot} gold!")
#
# 3. Use the simulation below to verify the 'Game Feel' before going live.
# ============================================================================
def simulate_treasure_room(player):
    # This simulation mimics the logic you would paste into game.py
    display_name = player.name.replace("_", " ").title()
    loot = random.randint(10, 30)
    
    player.gold += loot
    player.rooms_cleared += 1
    
    print(f"\n--- TREASURE ROOM SIMULATION ---")
    print(f"Lucky find! {display_name} found a dusty chest.")
    print(f"Obtained {loot} gold! Total Gold: {player.gold}")
    print(f"Progress Update: {player.rooms_cleared} rooms cleared.")

# =================================== #
# EXAMPLE 3: ADDING PERSISTENT DATA   #
# =================================== #
class HeroWithProgress(Hero if ENGINE_LOADED else object):
    def __init__(self, name, health, gold, role, level=1, xp=0, potions=1, max_health=None, rooms_cleared=0):
        self.name = name.lower().replace(" ", "_")
        if max_health is None: max_health = health
        
        if ENGINE_LOADED:
            super().__init__(self.name, health, gold, role, level, xp, potions, max_health)
            self.rooms_cleared = rooms_cleared
        else:
            self.role, self.health, self.max_health, self.gold, self.rooms_cleared = \
                       role, health, max_health, gold, rooms_cleared

    def get_save_data(self):
        if ENGINE_LOADED:
            data = super().get_save_data()
            data["rooms_cleared"] = self.rooms_cleared
            return data
        else:
            return {
                "name": self.name, "health": self.health, "max_health": self.max_health,
                "role": self.role, "gold": self.gold, "rooms_cleared": self.rooms_cleared
            }

# =========================================================================
# MAIN EXECUTION LOOP - LIKE GAME.PY
# =========================================================================
if __name__ == "__main__":
    while True:
        # UI LOGIC: CLEAR SCREEN (Matches game.py logic)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Mockup Warning when running without engine.py
        if not ENGINE_LOADED:
            print("!"*53)
            print("WARNING: 'engine.py' not found. Using Mock Logic.")
            print("!"*53 + "\n")

        print("="*53)
        print("=== DEV GUIDE: INTEGRATION TEST ===")
        print("="*53 + "\n")

        # Test 1: Sir Arthur
        sir_arthur = Knight("Sir Arthur", 120, 60)
        sir_arthur_display = sir_arthur.name.replace("_", " ").title()
        print(f"New Hero Role: {sir_arthur_display} | Role: {sir_arthur.role} | Gold: {sir_arthur.gold}")

        # Test 2: Randomized Monster Combat Simulation
        # We use MockMonster so it shows up even if ENGINE_LOADED is False
        thief = ThiefAbility()
        goblin = MockMonster("Sneaky Goblin", 30, 25, 10, ability=thief)
        
        ability_name = goblin.ability.get_name() if goblin.ability else "None"
        print(f"New Monster: {goblin.name} ({ability_name})")
        
        def monster_turn(m, h):
            action_roll = random.random()
            h_display = h.name.replace("_", " ").title()
            
            if action_roll < 0.5:
                print(f"\n--- {m.name} chooses: ATTACK ---")
                if hasattr(h, 'take_damage'):
                    h.take_damage(10)
                else:
                    h.health -= 10
                print(f"{m.name} hits {h_display} for 10 HP!")
                print(f"[{h_display} Status | HP: {h.health} | Gold: {h.gold}]")
            else:
                print(f"\n--- {m.name} chooses: STEAL ---")
                # Trigger ability logic (on_attack is mock-friendly)
                m.ability.on_attack(m, h, 0)
                print(f"[{h_display} Status | HP: {h.health} | Gold: {h.gold}]")

        print("\n--- Testing Randomized Initiative ---")
        if random.random() < 0.5:
            print(f"!!! AMBUSH! {goblin.name} acts first! !!!")
            monster_turn(goblin, sir_arthur)
        else:
            print(f"{sir_arthur_display} acts first!")
            sir_arthur.attack(goblin)

        print("\n" + "-"*53)
        input("Press Enter to continue to Room logic...")
        simulate_game_rooms(sir_arthur, 5)

        print("\n" + "-"*53)
        input("Press Enter to continue to Treasure logic...")
        simulate_treasure_room(sir_arthur)

        # Test 3: Data Rule Demonstration
        hero_with_progress = HeroWithProgress(
            sir_arthur.name,
            sir_arthur.health,
            sir_arthur.gold, 
            sir_arthur.role,
            rooms_cleared = sir_arthur.rooms_cleared
        )

        print(f"\nChecking save file (DATA RULE/VERTICAL PREVIEW):")
        save_data = hero_with_progress.get_save_data()
        for key, value in save_data.items():
            print(f"  {key.upper()}: {value}")

        print("\n" + "="*65)
        print("UI RULE: Use .replace('_', ' ').title() for Hero display.")
        print("DATA RULE: Hero names use lowercase and underscores.")
        print("ENGINE LOGIC: Use Dictionaries for scalable weights/probabilities.")
        print("="*65)

        user_choice = ""
        while user_choice not in ['y', 'n']:
            user_choice = input("\nRun testing again? (y/n): ").strip().lower()
        
        if user_choice == 'n':
            print("\nTesting Dev Guide closed. Check out engine_guide.py next.\n \nGoodbye!")
            break