'''
# ====================================================================
# FILE:    engine.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# CORE RULESET: Health, Leveling, and Monster Abilities
# ====================================================================
# This is the core ruleset for the game. 
# It handles health, leveling, and monster abilities.
# ====================================================================
'''
import random
from abc import ABC, abstractmethod

# --- GAME CONSTANTS ---
STARTING_HP = 60
STARTING_GOLD = 50
POTION_HEAL = 40
POTION_COST = 10
XP_PER_KILL = 30
LEVEL_UP_HP_BONUS = 10
EXPLOSION_DAMAGE = 5 

# --- ABILITY SYSTEM ---
class Ability(ABC):
    @abstractmethod
    def modify_health(self, health): pass
    @abstractmethod
    def modify_damage(self, damage): pass
    @abstractmethod
    def get_name(self): pass
    def on_death(self, player): pass
    def on_attack(self, monster, target, damage_dealt): return False

class NoAbility(Ability):
    def modify_health(self, health): return health
    def modify_damage(self, damage): return damage
    def get_name(self): return "Standard"

class BruteAbility(Ability):
    def modify_health(self, health): return health * 2
    def modify_damage(self, damage): return damage - 2
    def get_name(self): return "Brute"

class FragileAbility(Ability):
    def modify_health(self, health): return health // 2
    def modify_damage(self, damage): return damage * 2
    def get_name(self): return "Fragile"

class ExplosiveAbility(Ability):
    def modify_health(self, health): return health
    def modify_damage(self, damage): return damage
    def get_name(self): return "Explosive"
    def on_death(self, player):
        print(f"\n!!! BOOM !!! The monster exploded for {EXPLOSION_DAMAGE} damage!")
        player.take_damage(EXPLOSION_DAMAGE)

class VampireAbility(Ability):
    def modify_health(self, health): return health
    def modify_damage(self, damage): return damage
    def get_name(self): return "Life Drain"
    def on_attack(self, monster, target, damage_dealt):
        if monster.health < (monster.max_health * 0.5):
            if random.random() < 0.5:
                heal_up = int(damage_dealt * 0.5)
                monster.heal(heal_up)
                return True
        return False

# --- ENTITIES ---
class Entity(ABC):
    def __init__(self, name, health, gold):
        self.name = name
        self._health = health
        self._max_health = health
        self.gold = gold

    @property
    def health(self): return self._health
    @property
    def max_health(self): return self._max_health
    @max_health.setter
    def max_health(self, value): self._max_health = value

    def is_alive(self): return self._health > 0
    def take_damage(self, amount):
        self._health = max(0, self._health - max(0, amount))
    def heal(self, amount):
        self._health = min(self._max_health, self._health + amount)

    @abstractmethod
    def attack(self, target): pass

class Hero(Entity):
    def __init__(self, name, health, gold, role, level=1, xp=0, potions=1, max_health=STARTING_HP):
        # Force lowercase and underscores for safe save files.This acts as a Strategic Guardrail
        # fail-safe; even though game.py uses name.lower().replace(" ", "_"), the 'Brain' will
        # automatically correct it here before the character is created.
        safe_name = name.lower().replace(" ", "_")
        super().__init__(safe_name, health, gold)
        self.role = role
        self.level = level
        self.xp = xp
        self.potions = potions
        self._max_health = max_health
     
    def get_save_data(self):
        return {
            "name": self.name, "health": self.health, "max_health": self.max_health,
            "gold": self.gold, "role": self.role, "level": self.level,
            "xp": self.xp, "potions": self.potions
        }
     
    def attack(self, target):
        final_dmg = random.randint(5, 15) + (self.level * 2)
        target.take_damage(final_dmg)
        return final_dmg

    def gain_xp(self, amount):
        self.xp += amount
        print(f"Gained {amount} XP!")
        if self.xp >= (self.level * 50): self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.max_health += LEVEL_UP_HP_BONUS
        self._health = self.max_health
        print(f"\n*** LEVEL UP! You are now level {self.level}! ***")

    def use_potion(self):
        if self.potions <= 0:
            return "no_potions"

        if self._health >= self._max_health:
            return "full_health"
        
        self.heal(POTION_HEAL)
        self.potions -= 1
        return "success"

class Monster(Entity):
    def __init__(self, name, health, gold, damage, ability=None):
        self.ability = ability if ability else NoAbility()
        super().__init__(name, self.ability.modify_health(health), gold)
        self.mod_d = self.ability.modify_damage(damage)

    def attack(self, target):
        target.take_damage(self.mod_d)
        triggered = self.ability.on_attack(self, target, self.mod_d)
        return self.mod_d, triggered