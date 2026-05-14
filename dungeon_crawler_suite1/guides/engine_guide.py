'''
# ====================================================================
# FILE:    engine_guide.py
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# ====================================================================
# ENGINE_GUIDE.PY - TECHNICAL DEEP DIVE
# ====================================================================
# Goal: Explain the "Why" behind the design decisions in engine.py.
# 
# Focus: Encapsulation, Ability System, and the "Brain vs. Workhorse" 
#         Architectural Split.
# ====================================================================


# ============================================================================
# 1. ARCHITECTURE: THE BRAIN VS. THE WORKHORSE
# ============================================================================

 The most important design choice is the split between engine.py and game.py.

 - THE BRAIN (engine.py): This is the "Core" of the game. It contains the 
  logic for health, combat, and the Data Blueprint. It defines how a 
  Player is structured (the 8-variable dictionary) so that every save 
  is consistent. While it currently handles some basic feedback (like 
  potion messages), it is designed to be mostly independent.
  
 - THE WORKHORSE (game.py): This is the "Driver." It pulls the logic 
  from the brain and gives it a voice through outputting the character
  stats, battle loops, merchant, and rooms (which, rooms could have 
  something in it like a chest if we wanted to add that). It also 
  handles the File I/O in game.py as it is the workhorse that actually 
  saves the data to the disk and loads it back.

 WHY DO THIS? 
 The Brain provides the Template; the Workhorse provides the Action.
 By keeping logic separate, you can move your core rules to new projects. 

 To make the Brain 100% portable, we could use Pygame (a game library) to make
 a graphical game and eventually move those text messages like "Used a potion!"
 to game.py and have a graphical action take place (such as...health bar goes up)
 when the potion is used.

 We could also keep the potion output message and display it in a box at the
 bottom part of a graphical battle loop along with the visual action....
 
 Well, that could be a lesson for another day. - <(^_^)> -


 # ============================================================================
 # 2. THE DEVELOPER'S LINK: ENGINE + GAME
 # ============================================================================

 When expanding this engine, remember the "Link":
  1. Define it in the Engine: Add the variable or method to the Class.
  2. Invoke it in the Game: Create a menu option or display line in game.py.

 Note on Data Flow: When you see active_player.to_dict(), the Brain is 
 handing a perfectly organized package of data to the Workhorse. The 
 Workhorse then takes that package and writes it to the player's file.

 # =================================================================
 # 3. ENCAPSULATION - The Security Guard System
 # =================================================================

 In engine.py we don't let other code directly touch health.

 Instead of:
     player._health = -500     # Dangerous!

 We use:
     player.health             # Safe read via property

 This protects the internal state and lets us add logic checks 
 so the player never ends up with -9999 Health.

 We use a three-part "Security System" to achieve this:

 1. @property (The Gatekeeper): 
    Turns a function into a "read-only" variable so you can check 
    the current HP without being able to change it by mistake.

 2. @health.setter (The Security Guard): 
    The logic that runs when you try to change health. It contains 
    the "Max/Min" math that prevents HP from going above Max HP 
    or below 0. 

 3. @abstractmethod (The Blueprint Rule): 
    Acts as a "Rule" that forces every Hero and Monster to have 
    an attack() function, or the game won't run.

 # ========================================================================
 # 4. UI VS DATA - The "Bulletproof" Name Standard
 # ========================================================================

 We separate how the computer SEES a name from how the player SEES it.

 DATA RULE: Names are forced to .lower() and spaces are replaced with 
            underscores (_) within the Hero class or safe filename logic. 
            This ensures save files are consistent and cross-platform.
            
 UI RULE:   Always use .replace("_", " ").title() for Hero output. 
            This ensures "sir_arthur" displays as "Sir Arthur".
'''

# ============================================================
# BUG STRESS TEST: Property Protection
# ============================================================

class HealthDemo:
    def __init__(self, start_health=100, max_health=100):
        self._health = start_health
        self._max_health = max_health

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value > self._max_health:
            self._health = self._max_health
        elif value < 0:
            self._health = 0
        else:
            self._health = value

    # POTION STRESS TEST LOGIC
    def use_potion(self):
        if self._health >= self._max_health:
            return "full_health"
        
        self.health += 40
        return "success"


if __name__ == "__main__":
    print("=================================================================")
    print("=== ENGINE GUIDE - Technical Deep Dive ==========================")
    print("=================================================================\n")

    # Testing the security guard logic
    demo = HealthDemo(start_health=60, max_health=100)
    print(f"Starting health: {demo.health}")

    print("Trying to set health to 999...")
    demo.health = 999
    print(f"After attempt: {demo.health} (capped at max 100)")

    # Testing the Potion Guardrail
    print("\nStarting Potion Stress Test (Current HP: 100)...")
    result = demo.use_potion()
    print(f"Potion Result: {result} (The Brain blocked the use of potion!)")
    
    print("\n" + "-"*53)
    input("Press Enter to continue...")
    
    # Testing the Potion Success Trigger
    print("\nLowering health to 60 for Success Test...")
    demo.health = 60
    result = demo.use_potion()
    print(f"Current HP: {demo.health}")
    print(f"Potion Result: {result} (The Brain confirmed the potion was drank!)")

    print("\n" + "="*65 + "\n")
    # Reflecting the separation-to-link architecture design.
    print(" CORE ARCHITECTURE: The Separation-to-Link Design\n")
    
    print("• THE BRAIN: engine.py defines the data blueprint")
    print("• THE WORKHORSE: game.py handles File I/O and user display")
    print("• THE LINK: Changes in the Class must be called in the Game")
    print("• Use _health internally (protected)")
    print("• UI: Use .replace('_', ' ').title() for Hero names")
    print("• DATA: Store names as .lower() with underscores for save safety\n")
    print("="*65)

    print("\nThis concludes your learning journey for now, Hero.\n")
    print("Your building journey has just begun!")
    print("\n- Happy Coding -")