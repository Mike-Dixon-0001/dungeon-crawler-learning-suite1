'''
# =====================================================================
# FILE:    mini_engine.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# =====================================================================
# MINI_ENGINE.PY - THE PRACTICE SANDBOX
# =====================================================================
# Goal: Combine Inheritance and Dictionary-based saving into a 
#       working "Proof of Concept" battle loop.
#
# This is where mechanics are tested before moving them into the 
# main engine.py and game.py files.
#
# DATA ARCHITECTURE NOTE:
# Remember, we use super().__init__(name.lower(), health, gold) to
# force Hero names to lowercase for the save data. We then use .title()
# to capitalize the output for the user interface. 
#
# This ensures that file names (e.g., sir_arthur.txt) and internal 
# data stay consistent and safe for cross-platform file systems.
# =====================================================================
'''

import random
import time

# --- THE BLUEPRINTS ---

class Entity:
    def __init__(self, name, health, gold=0):
        self.name = name
        self._health = health
        self._max_health = health
        self.gold = gold

    def is_alive(self):
        return self._health > 0

    def take_damage(self, amount):
        if amount < 0:
            amount = 0
        self._health -= amount
        if self._health < 0:
            self._health = 0
        # Entity is silent to match the real engine.py

class Hero(Entity):
    def __init__(self, name, health, gold, role, level=1, xp=0, potions=1, max_health=None):
        
        # Force name to lowercase AND replace spaces with underscores.
        # This matches the get_safe_filename logic in game.py.
        safe_name = name.lower().replace(" ", "_")
        super().__init__(safe_name, health, gold)
        
        if max_health:
            self._max_health = max_health
            
        self.role = role
        self.level = level
        self.xp = xp
        self.potions = potions

    def attack(self, target):
        dmg = random.randint(10, 20) + (self.level * 2)
        
        # UI RULE: Replace underscores back with spaces and use .title() for display
        display_name = self.name.replace("_", " ").title()
        print(f"\n{display_name} swings their sword at the {target.name}!")
        target.take_damage(dmg)
        return dmg

    def get_save_data(self):
        return {
            "name": self.name, 
            "health": self._health,
            "max_health": self._max_health,
            "gold": self.gold,
            "role": self.role,
            "level": self.level,
            "xp": self.xp,
            "potions": self.potions
        }

class Monster(Entity):
    def __init__(self, name, health, gold, strength):
        super().__init__(name, health, gold)
        self.strength = strength

    def attack(self, target):
        # Add randomness to balance the battle loop
        dmg = random.randint(self.strength - 2, self.strength + 2)
        print(f"\nThe {self.name} lunges forward!")
        target.take_damage(dmg)
        return dmg

# ============================================================
# RUNNABLE SANDBOX LOOP
# ============================================================

if __name__ == "__main__":
    import os  # Added for screen clearing logic
    
    while True:
        # UI LOGIC: Wipes the terminal for a clean test run
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("   === MINI-ENGINE SANDBOX START ===\n")

        # TEST SETUP: Resetting objects inside the loop ensures every 
        # run starts with full health.
        player = Hero("Sir Arthur", 110, 100, "Paladin", level=1)
        slime = Monster("Mega Slime", 110, 15, 18)

        # UI RULE: Use .replace('_', ' ').title() for display
        display_name = player.name.replace("_", " ").title()
        print(f"Battle starts: {display_name} the {player.role} vs {slime.name}")
        print(f"Player HP: {player._health} | Monster HP: {slime._health}")
        print("-" * 40)
        
        # UI Logic for pausing before the battle starts
        print("\n" + "-"*30)
        input("Press Enter to begin the battle loop...")
        print("-"*30 + "\n")
        
        turn = 0
        while player.is_alive() and slime.is_alive():
            turn += 1
            print(f"\n--- ROUND {turn} ---")
            
            # Player Turn
            p_dmg = player.attack(slime)
            print(f"Result: {slime.name} takes {p_dmg} damage! (HP: {slime._health})")
            
            time.sleep(1)

            # Monster Turn (only if alive)
            if slime.is_alive():
                m_dmg = slime.attack(player)
                print(f"Result: {display_name} takes {m_dmg} damage! (HP: {player._health})")
                
                time.sleep(1)

        # --- FINAL OUTCOME ---
        print("\n" + "-"*40)
        print("=== BATTLE COMPLETE ===")
        if player.is_alive():
            print(f"VICTORY! {display_name} defeated the {slime.name}!")
        else:
            print(f"DEFEAT... {display_name} has been slain.")
        print("="*40)

        # Verify Save Data (Matches get_save_data dictionary logic)
        print("\nChecking dictionary output for save file (Note the lowercase name):")
        save_preview = player.get_save_data()
        for key, value in save_preview.items():
            print(f"  {key}: {value}")

        # --- STRICT INPUT VALIDATION: NO ENTER KEY RESTART ---
        # Prevents accidental restarts when enter is hit before making a choice.
        user_choice = ""
        while user_choice not in ['y', 'n']:
            user_choice = input("\nRun testing again? (y/n): ").strip().lower()
        
        if user_choice == 'n':
            print("\nTesting Mini Engine closed. Check out dev_guide.py next.\n \nGoodbye!")
            break