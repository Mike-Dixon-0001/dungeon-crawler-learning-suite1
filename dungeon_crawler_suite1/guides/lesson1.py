'''
# ====================================================================
# FILE:    lesson1.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# LESSON 1: INTRO TO CLASSES - The Hero Blueprint
# ====================================================================
# Goal: Move from loose variables to a proper Hero class.
#
# This is the "lightbulb" moment — realizing a Class is a blueprint 
# for characters.
#
# We also introduce simple dictionary-based saving.
# ====================================================================
'''

class Hero:
    # We use 8 arguments which match the 8-variable engine structure
    def __init__(self, name, health, gold, role, level=1, xp=0, potions=1, max_health=None):
        
        # Force lowercase and underscores for saving file name 
        # Just like player_name.replace('_', ' ').title() in lesson0.py
        # We do the opposite for saving player name to file
        self.name = name.lower().strip().replace(" ", "_") 
        self._health = health          
        
        # Logic: If loading, use saved max. If new, use current health.
        if max_health is None:
            self._max_health = health
        else:
            self._max_health = max_health
            
        self.role = role
        self.gold = gold
        self.level = level
        self.xp = xp
        self.potions = potions

    # =================================================================
    # A Class lets us "bundle" data (attributes) and actions (methods). 
    # Instead of having 8 loose variables for every character, we just
    # say 'Hero()'. This makes the code reusable and organized.
    # =================================================================

    def show_stats(self):
        # UI RULE: Restore spaces and capitalize for the player
        display_name = self.name.replace("_", " ").title()
        print(f"--- {display_name} the {self.role} ---")
        print(f"Health: {self._health}/{self._max_health}")
        print(f"Gold: {self.gold} | Potions: {self.potions}")
        print("--------------------------")

    def take_damage(self, amount):
        if amount < 0:
            amount = 0
            
        self._health -= amount
        if self._health < 0:
            self._health = 0
            
        # UI RULE: Hero output
        display_name = self.name.replace("_", " ").title()
        print(f"{display_name} took {amount} damage! Health: {self._health}/{self._max_health}")

    def get_save_data(self):
        # This dictionary is how we talk to the save files.
        # It follows our strict 8-variable order.
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


if __name__ == "__main__":
    print("=== LESSON 1: The Hero Class ===\n")
    
    # ====================================================================
    # TEST CASE: STRATEGIC GUARDRAILS (The Name Cleanup)
    # ====================================================================
    # We test with " Sir Arthur" (leading space) to prove the class in 
    # this lesson emulates what works in engine.py by automatically 
    # stripping the spaces and adding underscores for file safety.
    
    player = Hero(" Sir Arthur", 100, 50, "Paladin")
    player.show_stats()

    print("\n* A goblin attacks! *")
    player.take_damage(22)

    print("\n=== SAVING GAME STATE ===")
    # DATA RULE: The name is now stored as 'sir_arthur' for the save file.
    save_data = player.get_save_data()
    for k, v in save_data.items():
        print(f"{k}: {v}")

    print("\n" + "-"*60)
    print("NEXT LESSON: lesson2.py — Using Inheritance to clean up code!")
    print("-"*60)