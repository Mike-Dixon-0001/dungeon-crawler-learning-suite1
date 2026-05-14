# ============================================================================
# FILE:    readme.md
# PROJECT: Dungeon Crawler Learning Suite I (ver. 1.0)
# AUTHOR:  Michael Dixon (c). 2013 - 2026
# LICENSE: CC BY 4.0 (Attribution Required)
# GITHUB: https://github.com/Mike-Dixon-0001/dungeon-crawler-learning-suite1
# ============================================================================
#                          |
#                     OXXX[|]///////////////>
#                          |
# ============================================================================
# DOCUMENTATION: Authorship, AI Disclosure, and Project Roadmap
# ============================================================================

# Authorship & AI Disclosure

This project represents a 13-year journey from a 2013 C++ prototype (`npcmon`) 
to a modern 2026 Python OOP Learning Suite.

 **The Development Process:**

- **Human Origins:** The core combat spirit and character roles originated in the 
  author's 2013 C++ battle engine (`npcmon`). In 2026, the author 
  architected and created the "8-key" save system and modern OOP structures 
  specifically for this Python suite.
  
- **AI-Assisted Modernization:** After mastering Python OOP basics, the author 
  used AI as a "digital assistant" to help refactor legacy 2013 logic into the 
  2026 framework.
  
- **Human Refinement:** The author personally directed the AI to refine the 
  "8-key" logic, debug combat interactions, and polish documentation. 
  Every element has been manually reviewed, tested, and fine-tuned by the 
  author to ensure a "human-centric" standard.

 *Copyright (c) 2013-2026 Michael Dixon. All rights reserved.*

DUNGEON CRAWLER (GAME ENGINE) - LEARNING EDITION

WELCOME TO THE DUNGEON!

(Your journey begins here.)

This project is a complete learning suite for Python OOP 
and game architecture. It evolved from a 2013 C++ npc_monster 
battle engine project which was hardcoded using structs. 

When I started this learning journey using Python with OOP design, my 
Dungeon Crawler evolved into a modern version that I am happy to share 
as a learning suite.

The goal in this learning suite is to help others follow the same learning 
journey from basic variables to a full game engine.

====================================================================================
THE LEARNING PATH (Recommended Order)
====================================================================================

STEP 1:  BUILDING THE FOUNDATION (Lessons 0-2)

 * lesson0.py - Variables and basic game logic (combat log)

 * lesson1.py - Intro to Classes (the "lightbulb" moment)

 * lesson2.py - Inheritance with the Entity base class


STEP 2: THE SANDBOX

 * mini_engine.py - Practice sandbox for combat loops and 8-key saving


STEP 3: MODDING & EXPANSION

 * dev_guide.py - How to add new hero roles, abilities, and persistent data


STEP 4: ENGINEERING DEEP-DIVE

 * engine_guide.py - A masterclass in software architecture. It explains 
   the "Brain vs. Workhorse" split, portability for future projects, 
   how to maintain the link between the engine and the game, and the 
   "Humanized" naming standard for display vs. data storage.

====================================================================================
HOW TO USE THIS SUITE
====================================================================================

Note: This project was built using Python 3.13.3 with the Thonny editor. To ensure 
all OOP features and save logic work as intended, using a version of Python 3.11 or 
higher is recommended.

1. Start with lesson0.py and follow the files in order.

2. Read each lesson then run the file directly to see the output:
   such as python lesson0.py
   
3. When ready, run the full game:
   python game.py and load Bob: The Elf or create a new character!
   
 * PRO TIP: To test the "Data Rule" for file safety, try loading the 
   pre-made characters. The engine is smart enough to handle capitalization 
   and underscores for you! 
     
    - Type: 'bob' or 'Bob' to load the Level 38 Elf.
    - Type: 'sir test' or 'Sir Test' to load the Level 4 Fighter. 
     
 (The engine automatically finds 'sir_test.txt' even if you use spaces!)

====================================================================================
SYSTEM-SPECIFIC LAUNCH RITUALS (FOR THE BEST EXPERIENCE)
====================================================================================

Since this engine uses ANSI escape codes to hide the cursor and wipe the terminal 
for total immersion, running it inside a "code editor shell" (like the bottom 
box in Thonny or IDLE) will clutter the screen with messy symbols. 

Those editors are for writing code, but a real OS terminal is where the 
"Game Heartbeat" actually lives. For a clean interface, follow these steps:

====================================================================================
WINDOWS 11 (PC / Desktop)
====================================================================================
STEP 1: LAUNCH THE ENGINE
- FROM THONNY: Press CTRL + T to launch the game in the System Terminal (cmd.exe).

- FROM COMMAND PROMPT: 
  1. Open 'cmd' from the Windows Start menu.
  2. Type: cd c:\dungeon_crawler_suite1 (or your specific path).
  3. Type: python game.py

STEP 2: TERMINAL RITUALS (Works for both methods)
- Press ALT + ENTER to go Full Screen.

- Use CTRL + (+/-) to zoom the text to your viewing preference.

====================================================================================
RASPBERRY PI 5 OS / LINUX (ARM / Desktop)
====================================================================================
STEP 1: LAUNCH THE ENGINE
- FROM THONNY: Press CTRL + ALT + T to open the Terminal. 
  (Note: You must then manually 'cd' to your folder and type: python3 game.py)

- FROM TERMINAL / TTY3:
  1. Open LXTerminal or press CTRL + ALT + F3 for a full-screen "Pure CLI" mode.
  2. Type: cd /home/pi/dungeon_crawler_suite1 (or your specific path).
  3. Type: python game.py or python3 game.py (Both are verified to work).

STEP 2: TERMINAL RITUALS
- ZOOM: Use CTRL + SHIFT + (+/-) to adjust text size in the desktop terminal.

- FULL SCREEN (TTY3) TEXT SETUP: To fix small text, follow these steps:
  1. Run: sudo dpkg-reconfigure console-setup
  2. Select: UTF-8 -> Guess optimal character set.
  3. Select Font: Terminus (Recommended for high-res readability).
  4. Select Size: 16x32 (Provides large, clear text on modern screens).

- EXIT TTY3: To return to your Desktop GUI, press CTRL + ALT + F7 (Note: This 
  may vary on some systems).

- CLEAR SCREEN: Type clear at any time to wipe the terminal history.

*Note: This engine was tested successfully on Raspberry Pi 5 running Python 3.11.2.*

====================================================================================
ANDROID (Pydroid 3 / Mobile)
====================================================================================
1. Open game.py and tap the PLAY button.
2. Adjust text size manually: TAP THE THREE VERTICAL DOTS > PREFERENCES > FONT SIZE.

====================================================================================
PROJECT FILES
====================================================================================

- engine.py - The "Brain": Core classes and "Strategic Guardrail" name validation.

- game.py - Main game loop, combat, events, and saving

- lesson0.py - Basic variables and logic

- lesson1.py - First Hero class + 8-key dictionary saving

- lesson2.py - Inheritance with Entity and Shared Logic

- mini_engine.py - Practice sandbox for testing mechanics

- dev_guide.py - Extension examples (Knight, Thief, and Rooms)

- engine_guide.py - Technical deep dive into @properties, core 
  architecture, and the "Brain vs. Workhorse" design.
  
- archive.zip - The Legacy 2013 C++ Prototype (npcmon) for historical reference.

====================================================================================
HISTORY
====================================================================================

- 2013: Original C++ prototype (npcmon)

- 2026: Rewritten in Python with modern OOP principles and bug-safe math

 "Evolving the 2013 (npcmon) prototype into this comprehensive learning suite has 
 been quite a journey. It serves as proof that returning to old projects can spark 
 fresh ideas, all while embracing the spirit of learning Python and the power 
 of classes."

 NOTE: This Dungeon Crawler Learning Suite I is the first entry of a 
 planned trilogy:
 
 * SUITE I: The Logic Foundation (OOP Basics, Combat Loops, & Save Systems)
 
 * SUITE II: The Visual Frontier (Advanced Console Mechanics & World Navigation)
 
 * SUITE III: The Graphical Evolution (Asset Integration & Modern Rendering)
  
====================================================================================
Now go, slay some monsters with some coding fun!
====================================================================================
