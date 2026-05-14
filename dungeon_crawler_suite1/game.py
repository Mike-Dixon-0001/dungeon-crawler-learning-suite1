# ====================================================================
# FILE:    game.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
#                          |
#                     OXXX[|]///////////////>
#                          |
# ====================================================================
# GAME ENTRY POINT: Main Loop & Event Handling
# ====================================================================
import os, random, sys
from engine import (Hero, 
                    Monster,
                    VampireAbility,
                    BruteAbility,
                    FragileAbility, 
                    ExplosiveAbility,
                    NoAbility,
                    STARTING_HP,
                    STARTING_GOLD, 
                    XP_PER_KILL,
                    POTION_COST)

# --- GAME BALANCE SETTINGS ---
# Using dictionary to make it easier to add a new item/monster to a room later
ROOM_CHANCES = {
    "monster": 57,
    "merchant": 18,
    "empty": 25
}
SAVE_FOLDER = "players"
MAX_LEVEL = 99  # Adjust this to change the Hero's journey length

# --------------------------------------------------------------------
# SYSTEM UTILITIES
# --------------------------------------------------------------------

def clear_screen():
    """Wipes the terminal and scrollback buffer for immersion."""
    # HIDE CURSOR [ANSI: ?25l]
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system(r'clear && printf "\e[3J"')

def show_cursor():
    """Restores cursor visibility for player input [ANSI: ?25h]."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def get_safe_filename(name):
    """Translates 'Sir Arthur' to 'sir_arthur.txt' for file safety."""
    return name.lower().replace(" ", "_") + ".txt"

# --------------------------------------------------------------------
# DATA PERSISTENCE (SAVE/LOAD)
# --------------------------------------------------------------------

def save_player(player, path):
    """Serializes the Hero object into a key:value text file."""
    try:
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        
        save_dict = player.get_save_data()
        save_dict["name"] = save_dict["name"].lower() 
        
        lines = [f"{k}:{v}" for k, v in save_dict.items()]
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        print(f"Error saving to {path}: {e}")

def load_player():
    """Retrieves player data and enforces Cemetery and Legend rules."""
    show_cursor()
    raw_name = input("Enter character name to load: ").strip()
    safe_name = get_safe_filename(raw_name)
    
    folder_path = os.path.join(SAVE_FOLDER, safe_name)
    root_path = safe_name
    
    if os.path.exists(folder_path): 
        path_to_load = folder_path
    elif os.path.exists(root_path): 
        path_to_load = root_path
    else:
        print(f"Save file not found for {raw_name.title()}.")
        input("\n[Enter] to return to menu...")
        return None, None
        
    try:
        save_data = {}
        with open(path_to_load, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    save_data[key] = value
        
        # CEMETERY CHECK: Prevent loading dead heroes from previous sessions
        if int(save_data.get("health", 0)) <= 0:
            display_name = raw_name.replace("_", " ").title()
            print(f"\n[!] {display_name} HAS FALLEN and cannot be loaded.")
            print("Their name is written in the cemetery records.")
            input("\n[Enter] to return to menu...")
            return None, None

        # LEGEND CHECK: Prevent loading heroes who have already won
        if int(save_data.get("level", 1)) >= MAX_LEVEL:
            display_name = raw_name.replace("_", " ").title()
            print(f"\n[!] {display_name} is a HERO OF LEGEND and has retired.")
            print("Their story is complete. Choose a new hero to follow.")
            input("\n[Enter] to return to menu...")
            return None, None

        h = Hero(
            save_data.get("name", "Unknown"),
            int(save_data.get("health", STARTING_HP)),
            int(save_data.get("gold", STARTING_GOLD)),
            save_data.get("role", "Adventurer"),
            int(save_data.get("level", 1)),
            int(save_data.get("xp", 0)),
            int(save_data.get("potions", 1))
        )
        h.max_health = int(save_data.get("max_health", STARTING_HP))
        return h, path_to_load
        
    except Exception as e:
        print(f"Error reading the save file: {e}")
        input("\n[Enter] to return to menu...")
        return None, None

def get_random_monster(level):
    """Spawns a monster scaled to player level with random abilities."""
    # DATA RULE: Using a Dictionary for clear labeling and scalability
    monster_vault = {
        "Goblin":   {"hp": 20, "gold": 20, "dmg": 5},
        "Skeleton": {"hp": 15, "gold": 10, "dmg": 4},
        "Wolf":     {"hp": 25, "gold": 30, "dmg": 7},
        "Vampire":  {"hp": 40, "gold": 50, "dmg": 10}
    }
    
    # Pick a random name from the keys
    name = random.choice(list(monster_vault.keys()))
    stats = monster_vault[name]
    
    # Apply leveling math to the dictionary values
    hp = stats["hp"] + (level * 5)
    gold = stats["gold"]
    dmg = stats["dmg"]
    
    ability = (
        VampireAbility() 
        if name == "Vampire"        
        else random.choice([
            NoAbility(), 
            BruteAbility(), 
            FragileAbility(), 
            ExplosiveAbility()
        ])
    )
    
    return Monster(name, hp, gold, dmg, ability)

# --------------------------------------------------------------------
# MAIN GAME LOOP
# --------------------------------------------------------------------

def main():
    while True: # Outer Menu Loop
        clear_screen()
        print("==============================\n  WELCOME TO THE DUNGEON  \n==============================\n")
        player = None
        current_save_path = None
        
        # --- INITIAL MENU ---
        while True:
            show_cursor()
            choice = input("Load game (l), New game (n), or Quit (q)? ").lower()
            
            if choice == 'q':
                print("\nGoodbye Hero... until next time.")
                sys.exit()
                
            if choice == 'l':
                player, current_save_path = load_player()
                
                if player: 
                    break
                
                else:
                    clear_screen()
                    print("==============================\n  WELCOME TO THE DUNGEON  \n==============================\n")
                    continue
                    
            if choice == 'n':
                break 
            
        if player is None: 
            show_cursor()
            # UI RULE: Character's name can't be higher than 13 even with spaces
            name = input("Enter your hero's name (Max 13): ").strip()
            
            if len(name) > 13:
                name = name[:13]
                print(f"Name too long! Shortened to: {name}")

            role = input("Enter your character type: ").strip()
            player = Hero(name, STARTING_HP, STARTING_GOLD, role)
            
            safe_filename = get_safe_filename(name)
            
            # --- AUTO-SAVE LOGIC ---
            # Attempt to save to the players folder first for clean organization.
            # save_player() will automatically create the folder if it's missing.
            current_save_path = os.path.join(SAVE_FOLDER, safe_filename)
            
            save_player(player, current_save_path)
            
            print(f"\nRecord saved.")
            input("\n[Enter] to begin your journey...")
            
        # --- EXPLORATION LOOP ---
        room_count = 1
        while player.is_alive():
            clear_screen()
            display_name = player.name.replace("_", " ").title()
            
            line = "-" * 48
            print(f"\n{line}\n          ROOM {room_count}\n{line}")
            print(f"[ {display_name} the {player.role} | Level: {player.level} | Gold: {player.gold} ]")
            
            event = random.choices(
                population=list(ROOM_CHANCES.keys()), 
                weights=list(ROOM_CHANCES.values()))[0]
            
            if event == "monster":
                monster = get_random_monster(player.level)
                stolen_potion = False 
                combat_msg = f"A {monster.name} ({monster.ability.get_name()}) appears!"
                
                # --- COMBAT SUB-LOOP ---
                while monster.is_alive() and player.is_alive():
                    clear_screen()
                    print(f"\n{line}\n          ROOM {room_count}\n{line}")
                    print(f"[ {display_name} the {player.role} | Level: {player.level} | Gold: {player.gold} ]")
                    print(f"\n>> {combat_msg}\n")
                    print(f"HP: {player.health}/{player.max_health} | Potions: {player.potions} | Gold: {player.gold}\n")
                    
                    if stolen_potion: print(f"!!! The {monster.name} is holding your stolen Potion !!!")
                    
                    show_cursor()
                    action = input("Attack (a), Run (r), Potion (p), Steal Back (s): ").lower()
                    
                    if action == 'a':
                        dmg = player.attack(monster)
                        combat_msg = f"{display_name} hits the {monster.name} for {dmg} damage.\n"
                        
                        if monster.is_alive():
                            
                            # MONSTER LOGIC: Prioritize stealing, then drinking, then attacking
                            if player.potions > 0 and random.random() < 0.2 and not stolen_potion:
                                player.potions -= 1; stolen_potion = True
                                combat_msg += f"\nThe {monster.name} snatched a Potion!"
                                
                            elif stolen_potion and monster.health < 28 and random.random() < 0.6:
                                monster.heal(20); stolen_potion = False
                                combat_msg += "\n!!! The monster drank your Potion and healed! !!!"
                                
                            else: 
                                m_dmg, triggered = monster.attack(player)
                                combat_msg += f"\nThe {monster.name} hits you for {m_dmg} damage."
                                if triggered: combat_msg += f"\n!!! The {monster.name} drained life and healed! !!!"
                    
                    elif action == 's':
                        if stolen_potion:
                            if random.random() < 0.5:
                                player.potions += 1; stolen_potion = False
                                combat_msg = "Success! You grabbed your Potion back!"
                            else: 
                                m_dmg, triggered = monster.attack(player)
                                combat_msg = f"Failed! The {monster.name} hits you for {m_dmg} damage."
                        else: combat_msg = "Nothing to steal back."
                    
                    elif action == 'r':
                        if random.random() < 0.5: print("\nYou escaped!"); break
                        else: 
                            m_dmg, triggered = monster.attack(player)
                            combat_msg = f"Failed! The {monster.name} hits you for {m_dmg} damage."
                    
                    elif action == 'p': 
                        status = player.use_potion()
                        if status == "success":
                            combat_msg = f">>> {display_name} drank a potion. <<<"
                        elif status == "full_health":
                            combat_msg = f">>> HP is already full! Potion saved. <<<"
                        else:
                            combat_msg = "No potions left!"

                if not player.is_alive():
                    show_cursor()
                    print(f"\n[!] The {monster.name} has defeated you...\n")
                    input("Press [Enter] to see your fate...")
                
                elif not monster.is_alive():
                    print(f"\nYou defeated the {monster.name}!")
                    if stolen_potion:
                        player.potions += 1
                        print('\n>>> You search the monster and RECOVER your stolen potion!\n')
                    monster.ability.on_death(player) 
                    player.gold += monster.gold; player.gain_xp(XP_PER_KILL)
                    
                    # --- VICTORY CHECK ---
                    if player.level >= MAX_LEVEL:
                        clear_screen()
                        print("\n==========================================")
                        print(f"      CONGRATULATIONS, {display_name.upper()}!")
                        print("==========================================\n")
                        print(f"{display_name} has fought valiantly and reached Level {MAX_LEVEL}!")
                        print("Your journey and battles will be told for generations to come.")
                        save_player(player, current_save_path)
                        input("\n[Enter] to return to menu...")
                        break 
                    
            elif event == "merchant":
                show_cursor()
                print(f"\nMerchant Barnaby: I have potions for {POTION_COST} gold.")
                while True:
                    m_choice = input("Buy a potion? (y/n): ").lower()
                    if m_choice in ['y', 'n']: break
                if m_choice == 'y':
                    if player.gold >= POTION_COST:
                        player.gold -= POTION_COST; player.potions += 1
                        print("Bought a potion.")
                    else: print("Not enough gold.")
                else: print("Barnaby waves goodbye.")
            
            else:
                print(f"\n --- EMPTY ---\n")
                print("The corridor is quiet. Nothing but dust and shadows here.")
            
            save_player(player, current_save_path)
            if player.is_alive():
                room_count += 1
                show_cursor()
                choice = input("\n[Enter] to continue, 'q' to quit: ").lower()
                if choice == 'q':
                    break
        
        # --- DEATH SEQUENCE ---
        if player is not None and not player.is_alive():
            save_player(player, current_save_path) 
            clear_screen()
            display_name = player.name.replace("_", " ").upper()
            sentence_name = player.name.replace("_", " ").title()

            print("\n==============================")
            print(f"      {display_name} HAS FALLEN")
            print("==============================\n")
            
            if room_count < 4:
                print(f"{sentence_name}'s journey ended pitifully in Room {room_count}.")
                print("Their name is shamefully written in the cemetery records.")
                
            else:
                print(f"{sentence_name}'s journey ended courageously fighting to the death in Room {room_count}.")
                print("Their name is written in the cemetery records.")
            
            print("\n" + "=" * 30 + "\n")
            
            show_cursor()
            while True:
                death_choice = input("Return to Main Menu? (y/n): ").lower().strip()
                if death_choice == 'y':
                    break
                if death_choice == 'n':
                    print("\nGoodbye Hero... until next time.")
                    sys.exit()

if __name__ == "__main__":
    main()
