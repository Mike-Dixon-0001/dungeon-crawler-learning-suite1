'''
# ====================================================================
# FILE:    lesson0.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# LESSON 0: THE FOUNDATION - Variables & Combat Log
# ====================================================================
# Goal: Translate "Game Rules" into simple Python code using 
#       variables and prints.
#
# This is the very beginning — no classes yet. Just variables and logic.
# ====================================================================
'''

# Game Rules as Variables (Matches the 8-Variable Engine Structure)

# We use 'save/load' file name in lowercase with underscore.
player_name = "Sir Arthur".lower().replace(" ", "_") 
player_health = 100        
player_max_health = 100    
player_gold = 50
player_role = "Warrior"
player_level = 1
player_xp = 0   # Current progress (Starts at 0). Note: You need 50 XP to reach Level 2!
player_potions = 1          

monster_name = "Cave Slime"
monster_health = 35
monster_max_health = 35

# =================================================================
# We start with simple variables so you can see how data is stored.
# In a real game, you have dozens of these. If we don't group them
# together eventually, the code becomes a "spaghetti" mess of loose
# names and numbers.
# =================================================================

# Note: we use player_name.replace('_', ' ').title()
# instead of .capitalize() to display names.  If you name your character
# "Sir Arthur", .capitalize() would only fix the first letter - Sir arthur -
# .title() ensures every word is capitalized, and .replace('_', ' ')
# converts the "data version" - sir_arthur - for save file naming back into
# our "Output" version of Sir Arthur.

print("=== DUNGEON CRAWLER - LESSON 0 ===")
print(f"A wild {monster_name} appears!")
print(f"{player_name.replace('_', ' ').title()} HP: {player_health}/{player_max_health}")
print(f"{monster_name} HP: {monster_health}/{monster_max_health}\n")

# Simulate taking damage
damage = 18
player_health -= damage

# Logic check: Don't let HP go negative
if player_health < 0:
    player_health = 0

print(f"The {monster_name} hits {player_name.replace('_', ' ').title()} for {damage} damage!")
print(f"{player_name.replace('_', ' ').title()}'s HP is now: {player_health}/{player_max_health}\n")

# Healing with a potion
heal_amount = 25
player_health += heal_amount

# Logic check: Don't let HP go over maximum
if player_health > player_max_health:
    player_health = player_max_health

print(f"{player_name.replace('_', ' ').title()} drinks a potion for {heal_amount} HP!")
print(f"{player_name.replace('_', ' ').title()}'s HP is now: {player_health}/{player_max_health}")

print("\n" + "-"*60)
print("NEXT LESSON: lesson1.py — Moving from variables to Classes!")
print("-"*60)