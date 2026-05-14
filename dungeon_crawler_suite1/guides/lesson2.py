'''
# ====================================================================
# FILE:    lesson2.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# LESSON 2: INHERITANCE - The Entity Blueprint
# ====================================================================
#
# Goal: Show that Heroes and Monsters share common traits 
#       (name, health, is_alive, take_damage).
#
# We create a parent class called Entity to avoid repeating code.
# This makes the engine cleaner and more professional.
#
# NOTE: In the final engine.py, you will see @property, @setter, 
# and @abstractmethod. These protect data and set rules:
#
# 1. @property: Turns a function into a "read-only" variable to 
#    protect stats like Health from accidental changes.
#
# 2. @max_health.setter: A controlled way to update a variable. 
#    It allows the engine to change Max Health (like when leveling 
#    up) while keeping the guardrails in place.
#
# 3. @abstractmethod: Acts as a "Rule" that forces every Hero and 
#    Monster to have an attack() function, or the game won't run.
# ====================================================================
'''

# ====================================================================
# THE BASICS: 4 RULES OF A CLASS
# ====================================================================
# To understand Inheritance, you must first understand how a "Class"
# works. Think of it like a Tabletop RPG character sheet:
#
# RULE 1: THE BLUEPRINT (The Class)
# A Class is the blank character sheet. It defines what EVERY 
# character has (Health, Name, Gold) before a specific person 
# is ever created.
#
# RULE 2: THE BIRTH (The __init__ Method)
# The __init__ function is the "Creation Screen." It takes raw 
# data (like "Sir Arthur") and stamps it onto the blueprint to 
# create a specific Object you can play with.
#
# RULE 3: ENCAPSULATION (The Protective Shell)
# Think of Encapsulation like a "Control Panel." We use an underscore 
# (self._health) to hide the raw wires inside the machine. 
#
# THE WHY: If you let any part of the game change health directly, 
# someone might accidentally set it to -500 or something silly like
# "Pizza."
#
# THE HOW: By forcing everyone to use a function like take_damage(), 
# the Entity can "check" the math first (e.g., ensuring health 
# never drops below 0). It keeps the internal data safe and 
# predictable.
#
# THE PYTHON "CATCH": In Python, the underscore is a suggestion. 
# A programmer CAN still force a change to self._health, but they 
# shouldn't. In the final engine.py, we use @property to turn 
# this suggestion into a strict "Read-Only" rule.
#
# RULE 4: POLYMORPHISM (The Blueprint Rule)
# Polymorphism means "Many Forms." In our game, it allows us to give 
# the same command—like attack()—to any character, and they will 
# perform it in their own unique way. 
#
# THE WHY: In the final engine.py, we use @abstractmethod to FORCE 
# every Hero and Monster to have an attack() function. This 
# ensures that no matter who is fighting, the engine knows 
# exactly how to call the "Attack" command without the game crashing.
#
# WHY USE ENTITY? (The Efficiency Rule)
# Without the Entity blueprint, you would have to write the same 
# logic for Health, Gold, and Damage twice—once for the Hero and 
# once for the Monster. By putting it in Entity, you write it 
# ONCE, and everyone else inherits it. This means fewer bugs and 
# a much smaller, cleaner engine.
# ====================================================================
class Entity:
    def __init__(self, name, health, gold=0):
        # We leave the parent name as-is so monsters can stay capitalized
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
        # Silent Math: Update _health with safety checks,
        # but leave the messaging to the game loop.

    def get_health(self):
        return self._health


class Hero(Entity):
    def __init__(self, name, health, gold, role, level=1, xp=0, potions=1, max_health=None):        
        # Here we use .lower().replace(" ", "_") to force hero name to lowercase 
        # and underscores for saving file name.
        super().__init__(name.lower().replace(" ", "_"), health, gold) 
        
        # Logic to handle starting HP vs saved HP
        self._max_health = max_health if max_health else health
            
        self.role = role
        self.level = level
        self.xp = xp
        self.potions = potions
    
    # Note: We now use .replace('_', ' ').title() to output the hero name. 
    def show_stats(self):
        display_name = self.name.replace("_", " ").title()
        print(f"--- {display_name} the {self.role} ---")
        print(f"Health: {self._health}/{self._max_health}")
        print(f"Gold: {self.gold} | Potions: {self.potions}")
        print("------------------------------")


class Monster(Entity):
    def __init__(self, name, health, gold, strength):
        super().__init__(name, health, gold)
        self.strength = strength

    def attack(self, target):
        print(f"\n{self.name} attacks!")
        target.take_damage(self.strength)


if __name__ == "__main__":
    print("=== LESSON 2: Inheritance with Entity ===\n")
    
    # 8-variable compliant initialization
    player = Hero("Sir Arthur", 100, 50, "Paladin")
    slime = Monster("Cave Slime", 45, 10, 12)

    player.show_stats()
    print(f"A {slime.name} appears!\n")
    
    #Wait for the user to hit enter.
    input("Press Enter to start")
    
    while player.is_alive() and slime.is_alive():
        # Monster attacks the player
        slime.attack(player)
        
        # UI RULE: Use Hero name for the battle log
        display_name = player.name.replace("_", " ").title()
        print(f"{display_name} took {slime.strength} damage!")

    if player.is_alive():
        display_name = player.name.replace("_", " ").title()
        print(f"\nVictory! {display_name} survived.")
    else:
        display_name = player.name.replace("_", " ").title()
        print(f"\n{display_name} has fallen.")

    print("\n" + "-"*60)
    print("NEXT STEP: mini_engine.py — Test it all in the sandbox!")
    print("-"*60)