"""
Program Name: You_Wake_Up_Jonas_Penner_Mayoh
Author: Jonas Penner Mayoh
Course: CS 30
Date: June 17, 2026

Description:
    "You Wake Up" is a text-based choose-your-own-adventure game.
    The player wakes up and must make a series of decisions about
    how their morning unfolds. Whether to call in sick or get
    breakfast, how to get ready for work, and how to handle their
    boss. Every choice branches the story in a new direction,
    eventually leading to one of eleven possible endings: some
    good, some bad, and quite a few fatal. The main menu loops
    continuously so the player can keep replaying the story and
    try to discover every ending.
"""

import textwrap


# ---------------------------------------------------------------
# STORY DATA
#
# The entire story is stored as one nested dictionary. Each key
# is a unique node id, and each value is a dictionary describing
# that moment in the story. A node will contain ONE of the
# following shapes:
#   1. An ending node:   {"text": ..., "ending": True,
#                          "ending_type": ...}
#   2. A linear node:    {"text": ..., "next": <node id>}
#   3. A decision node:  {"text": ..., "prompt": ...,
#                          "choices": {<answer>: <node id>, ...}}
# ---------------------------------------------------------------
STORY = {

    # Opening
    "start": {
        "text": (
            "You wake up. It's a brand new day, and already you "
            "have a decision to make."
        ),
        "prompt": (
            "Do you call in sick to skip work, or are you hungry "
            "and want to get breakfast first? (sick/breakfast)"
        ),
        "choices": {
            "sick": "call_in_sick",
            "breakfast": "get_breakfast",
        },
    },

    # Branch A: Call in sick
    "call_in_sick": {
        "text": (
            "You call in sick to skip work. Almost immediately, "
            "your phone rings. Your boss starts yelling at you "
            "for not showing up. He's such a jerk that you don't "
            "even want to work there anymore."
        ),
        "prompt": (
            "Do you call him right back to quit, head to his "
            "office to quit in person, or just treat yourself to "
            "brunch since you're not going in anyway? "
            "(call/office/brunch)"
        ),
        "choices": {
            "call": "quit_call_boss",
            "office": "quit_go_office",
            "brunch": "go_brunch",
        },
    },
    "quit_call_boss": {
        "text": (
            "He picks up the phone and starts to yell at you for "
            "not showing up for work. Before he can get another "
            "word in, you tell him you're quitting and hang up "
            "the phone. It's finally over."
        ),
        "ending": True,
        "ending_type": "good",
    },
    "quit_go_office": {
        "text": (
            "You walk into his office and he immediately yells "
            "at you for being late. You tell him you're quitting "
            "right then and there. He tells you to get out of "
            "his office and says you weren't a good employee "
            "anyway. You leave filled with joy, slamming the "
            "door behind you as one final goodbye. It's finally "
            "over."
        ),
        "ending": True,
        "ending_type": "good",
    },

    # Branch A1: Brunch instead of work
    "go_brunch": {
        "text": (
            "Since you're already not going to work, you decide "
            "you might as well treat yourself to a nice brunch."
        ),
        "prompt": "Do you go to Smitty's or Cafe Francais? "
                  "(smittys/francais)",
        "choices": {
            "smittys": "brunch_smittys",
            "francais": "brunch_francais",
        },
    },
    "brunch_smittys": {
        "text": "You sit down at Smitty's and open up the menu.",
        "prompt": (
            "Do you order Sausage and Eggs, or a Chicken and "
            "Waffles? (sausage/waffles)"
        ),
        "choices": {
            "sausage": "order_sausage_eggs",
            "waffles": "order_chicken_waffles",
        },
    },
    "brunch_francais": {
        "text": (
            "You sit down at Cafe Francais and open up the menu."
        ),
        "prompt": (
            "Do you order Sausage and Eggs, or a Chicken and "
            "Waffles? (sausage/waffles)"
        ),
        "choices": {
            "sausage": "order_sausage_eggs",
            "waffles": "order_chicken_waffles",
        },
    },
    "order_sausage_eggs": {
        "text": (
            "You order the Sausage and Eggs. The meal is great, "
            "so you head home afterward to rest. Before long, "
            "you start to feel sick. A trip to the doctor reveals "
            "you've contracted a mutant tapeworm."
        ),
        "next": "bedridden",
    },
    "order_chicken_waffles": {
        "text": (
            "You order the Chicken and Waffles. The meal is "
            "great, so you head home afterward to rest. Before "
            "long, you start to feel sick. A trip to the doctor "
            "reveals you've contracted salmonella."
        ),
        "next": "bedridden",
    },
    "bedridden": {
        "text": (
            "Whatever it is you've caught, it's bad. You're now "
            "bedridden, and your sickness only gets worse by the "
            "hour."
        ),
        "next": "food_poisoning_death",
    },
    "food_poisoning_death": {
        "text": (
            "Despite everyone's best efforts, you die due to "
            "complications in the healing process. Turns out "
            "calling in sick was far more dangerous than just "
            "going to work ever could have been."
        ),
        "ending": True,
        "ending_type": "death",
    },

    # Branch B: Get breakfast and go to work
    "get_breakfast": {
        "text": (
            "You're hungry, so before anything else, you decide "
            "to make yourself some breakfast."
        ),
        "prompt": (
            "Do you make scrambled eggs and bacon, or just grab "
            "a bowl of yogurt? (eggs/yogurt)"
        ),
        "choices": {
            "eggs": "breakfast_eggs_bacon",
            "yogurt": "breakfast_yogurt",
        },
    },
    "breakfast_eggs_bacon": {
        "text": (
            "You decide to make scrambled eggs and bacon. It "
            "takes you a full 30 minutes to slowly cook your way "
            "through breakfast."
        ),
        "next": "get_ready",
    },
    "breakfast_yogurt": {
        "text": (
            "You decide a bowl of yogurt is quick and easy. With "
            "time to spare, you flip on the TV, and somehow end "
            "up watching it for the next 30 minutes anyway."
        ),
        "next": "get_ready",
    },
    "get_ready": {
        "text": (
            "You glance at the clock. You have to be at work in "
            "30 minutes. It's only a short walk away, but you "
            "still haven't showered."
        ),
        "prompt": (
            "Do you shower and risk being late, skip the shower "
            "so you're on time, or take a relaxing bath and "
            "accept you might not show up at all? "
            "(shower/noshower/bath)"
        ),
        "choices": {
            "shower": "shower_late",
            "noshower": "skip_shower",
            "bath": "take_bath",
        },
    },

    # Branch B1: Shower and be late
    "shower_late": {
        "text": (
            "You shower anyway, even though you know it'll make "
            "you late. You throw on your suit and start the walk "
            "to work."
        ),
        "prompt": (
            "Your day is already off to a rough start, but it "
            "doesn't have to stay that way. Do you push forward "
            "and try to turn things around, or just brace "
            "yourself for the worst since your boss is probably "
            "already furious? (push/brace)"
        ),
        "choices": {
            "push": "rough_start",
            "brace": "three_strikes",
        },
    },
    "three_strikes": {
        "text": (
            "Sure enough, you arrive late again. This is "
            "officially the third time this week, and this time "
            "your boss doesn't even bother yelling. The look on "
            "his face says everything you need to know about how "
            "this is going to go."
        ),
        "ending": True,
        "ending_type": "bad",
    },
    "rough_start": {
        "text": (
            "Your day is already off to a rough start, but you "
            "decide it doesn't have to stay that way."
        ),
        "prompt": (
            "Do you put your head down and work hard until "
            "lunch, or invite your boss out to lunch to apologize "
            "for being late? (work/apologize)"
        ),
        "choices": {
            "work": "work_hard_lunch",
            "apologize": "lunch_apology",
        },
    },
    "work_hard_lunch": {
        "text": (
            "You work hard right up until lunch to set an "
            "example of your effort. As it turns out, lunch with "
            "your boss goes well, though he now expects a lot "
            "more from you. If you perform well over the next "
            "quarter, you could be looking at a pay raise."
        ),
        "next": "work_harder_months",
    },
    "lunch_apology": {
        "text": (
            "You talk to your boss and invite him out to lunch "
            "as an apology for your recent mistakes. "
            "Unfortunately, your boss gets mad, and the lunch "
            "turns into a huge fight right there in the "
            "restaurant. You get fired on the spot."
        ),
        "next": "fired_path",
    },
    "work_harder_months": {
        "text": (
            "The rest of the day, you work harder than you ever "
            "have before. Over the next few months, you keep "
            "showing up on time and stay more active in the "
            "workplace than ever. Eventually, your boss calls you "
            "into his office for a talk."
        ),
        "next": "pay_raise_ending",
    },
    "pay_raise_ending": {
        "text": (
            "He tells you that you've helped bring a 30 percent "
            "increase to the company's profits over the last few "
            "months. The company is so grateful that they offer "
            "you a raise on the spot, your salary has now "
            "increased by 20 percent. Calling in sick almost cost "
            "you everything, but in the end, persistence paid "
            "off."
        ),
        "ending": True,
        "ending_type": "good",
    },
    "fired_path": {
        "text": (
            "With nothing left to do, you go home for the rest "
            "of the day to rest. There's nothing else you can do "
            "now."
        ),
        "next": "eviction_ending",
    },
    "eviction_ending": {
        "text": (
            "Months later, you still can't find a job, although "
            "you aren't exactly working hard to find one either. "
            "Without any income, you can't afford rent, and you "
            "end up getting evicted. Maybe that apology lunch "
            "wasn't your best idea."
        ),
        "ending": True,
        "ending_type": "bad",
    },

    # Branch B2: Skip the shower
    "skip_shower": {
        "text": (
            "You decide to skip the shower entirely so you can "
            "make it to work on time. You throw on your suit and "
            "head out the door."
        ),
        "next": "crosswalk_incident",
    },
    "crosswalk_incident": {
        "text": (
            "While you're waiting at a crosswalk, a car blasts "
            "past you, right through a puddle. You're completely "
            "soaked from head to toe."
        ),
        "next": "soaked_at_work",
    },
    "soaked_at_work": {
        "text": (
            "When you finally arrive at work, your boss lectures "
            "you about your incompetence, since you've wrecked "
            "your suit and you smell like puddle water. Showering "
            "might have actually been the smarter choice after "
            "all."
        ),
        "ending": True,
        "ending_type": "bad",
    },

    # Branch B3: Take a bath instead
    "take_bath": {
        "text": (
            "You're tired, so you decide to take a bath instead, "
            "accepting that you might be late for work if you "
            "even show up at all."
        ),
        "prompt": (
            "Do you take a plain bath with no bubbles, or treat "
            "yourself to a full bubble bath? (nobubbles/bubbles)"
        ),
        "choices": {
            "nobubbles": "bath_no_bubbles",
            "bubbles": "bubble_bath",
        },
    },

    # Sub-branch: plain bath
    "bath_no_bubbles": {
        "text": (
            "You settle into a relaxing bath, but something "
            "about it feels like it's missing something."
        ),
        "prompt": (
            "Do you toss in a bath bomb to make the experience "
            "better, or start watching a show on your iPad "
            "instead? (bomb/ipad)"
        ),
        "choices": {
            "bomb": "bath_bomb_1",
            "ipad": "ipad_bath",
        },
    },
    "bath_bomb_1": {
        "text": (
            "You toss in a bath bomb to make the experience "
            "better. When you finally get out of the bath, "
            "you notice you're red all over, turns out you had "
            "an allergic reaction to the bath bomb."
        ),
        "prompt": (
            "Do you start scratching at the itch, or grab some "
            "lotion to try to cool your skin down? (scratch/"
            "lotion)"
        ),
        "choices": {
            "scratch": "scratch_path",
            "lotion": "lotion_path",
        },
    },
    "scratch_path": {
        "text": (
            "You give in and scratch at the itch, but it only "
            "seems to make things worse."
        ),
        "next": "throat_closes",
    },
    "lotion_path": {
        "text": (
            "You grab some lotion to cool your skin, but it "
            "doesn't seem to help much at all."
        ),
        "next": "throat_closes",
    },
    "throat_closes": {
        "text": (
            "Whatever is happening to your body is getting worse "
            "fast, your throat starts to close up."
        ),
        "next": "allergy_death",
    },
    "allergy_death": {
        "text": (
            "Nobody is around to help in time, and you die before "
            "anyone can save you. Bath bombs, it turns out, are "
            "not quite as relaxing as advertised."
        ),
        "ending": True,
        "ending_type": "death",
    },
    "ipad_bath": {
        "text": (
            "You prop up your iPad and start watching a show to "
            "make the bath feel a little better."
        ),
        "prompt": (
            "Do you wash your body without a scrubber, or reach "
            "over to grab a scrubber to wash your body? "
            "(noscrub/scrub)"
        ),
        "choices": {
            "noscrub": "no_scrubber_path",
            "scrub": "scrubber_path",
        },
    },
    "no_scrubber_path": {
        "text": (
            "Without a scrubber, you reach for some soap instead. "
            "Almost immediately, you start scratching all over, "
            "and the lotion you grab afterward does nothing to "
            "help."
        ),
        "next": "throat_closes",
    },
    "scrubber_path": {
        "text": (
            "You reach over for the scrubber, but in doing so "
            "you accidentally knock your iPad's charging cord "
            "into the bathwater. It electrocutes you instantly, "
            "knocking you unconscious, and you slowly sink into "
            "the water."
        ),
        "next": "drowning_death",
    },
    "drowning_death": {
        "text": (
            "You die before anyone can save you. Lesson learned: "
            "maybe leave the electronics out of the bathroom next "
            "time."
        ),
        "ending": True,
        "ending_type": "death",
    },

    # Sub-branch: bubble bath
    "bubble_bath": {
        "text": (
            "You decide to treat yourself to a full bubble bath. "
            "Honestly, your bath is perfect, nothing could "
            "possibly ruin it."
        ),
        "prompt": (
            "Do you add a bath bomb anyway, or just leave the "
            "bath alone? (bomb/nobomb)"
        ),
        "choices": {
            "bomb": "bath_bomb_2",
            "nobomb": "no_bath_bomb",
        },
    },
    "bath_bomb_2": {
        "text": (
            "You add a bath bomb anyway, just to push your luck. "
            "Sure enough, you get out of the bath red all over, "
            "yet another allergic reaction to the bath bomb. Your "
            "throat starts to close up almost immediately."
        ),
        "next": "allergy_death",
    },
    "no_bath_bomb": {
        "text": (
            "You decide to leave the bath alone. It really was "
            "perfect, after all, and now it's time to get out."
        ),
        "prompt": (
            "Do you grab a towel and dry off right away, or take "
            "a moment to flex in the mirror first? (towel/flex)"
        ),
        "choices": {
            "towel": "towel_dry",
            "flex": "flex_mirror",
        },
    },
    "towel_dry": {
        "text": (
            "You grab a towel and dry yourself off, but you slip "
            "on the wet floor and hit your head hard on the sink."
        ),
        "next": "blunt_trauma_death",
    },
    "blunt_trauma_death": {
        "text": (
            "You die due to blunt force trauma. Bathroom floors, "
            "it turns out, are no joke."
        ),
        "ending": True,
        "ending_type": "death",
    },
    "flex_mirror": {
        "text": (
            "You take a moment to flex in the mirror, admiring a "
            "bath well spent. Without warning, you get a severe "
            "charley horse and find that you can't move at all."
        ),
        "next": "starve_to_death",
    },
    "starve_to_death": {
        "text": (
            "Over the next few days, you're stuck right where you "
            "are. Your boss calls to fire you, but you can't even "
            "answer the phone, and nobody ever checks up on you. "
            "Slowly, and all because of one bath, you starve to "
            "death."
        ),
        "ending": True,
        "ending_type": "death",
    },
}


# ---------------------------------------------------------------
# Display names for every ending, used by the endings tracker.
# Keeping this separate from STORY keeps the menu display logic
# simple while STORY stays focused purely on the narrative.
# ---------------------------------------------------------------
ENDING_NAMES = {
    "quit_call_boss": "Quit By Phone",
    "quit_go_office": "Quit In Person",
    "pay_raise_ending": "Employee Of The Month",
    "three_strikes": "Three Strikes",
    "eviction_ending": "Evicted",
    "soaked_at_work": "Soaked And Scolded",
    "food_poisoning_death": "Food Poisoning",
    "allergy_death": "Bath Bomb Allergy",
    "drowning_death": "iPad Electrocution",
    "blunt_trauma_death": "Slippery Sink",
    "starve_to_death": "Charley Horse Catastrophe",
}


def display_text(text):
    """Print a piece of narration or a prompt, nicely wrapped.

    Args:
        text: The string to print, wrapped to a fixed width so
            long sentences stay readable in the console.

    Returns:
        None
    """
    print(textwrap.fill(text, width=70))


def print_divider():
    """Print a horizontal divider line for visual separation.

    Returns:
        None
    """
    print("-" * 60)


def press_enter_to_continue():
    """Pause the story and wait for the user to press Enter.

    Returns:
        None
    """
    input("\n(Press Enter to continue...)\n")


def get_choice(prompt, valid_keys):
    """Ask the user a question and loop until they answer validly.

    This is the single input-validation routine used by both the
    main menu and every decision point in the story, so invalid
    input is always handled the same way.

    Args:
        prompt: The question text to display, which should
            already include the available options for the user.
        valid_keys: Any container (dict or set) whose keys/items
            are the accepted lowercase answers for this question.

    Returns:
        The validated, lowercase answer the user typed.
    """
    while True:
        print()
        display_text(prompt)
        answer = input("> ").strip().lower()
        if answer in valid_keys:
            return answer
        print(
            "Sorry, I didn't understand that. Please type one "
            "of the options shown above."
        )


def play_game(achieved_endings):
    """Run one full playthrough of the You Wake Up story.

    Starting at the "start" node, this walks the STORY graph one
    node at a time: printing narration, collecting a validated
    choice at every decision point, and automatically advancing
    through linear story beats. When an ending node is reached,
    its id is recorded in achieved_endings before returning to
    the main menu.

    Args:
        achieved_endings: A set of ending ids already unlocked
            across the play session. Updated in place so the
            endings tracker persists between playthroughs.

    Returns:
        None
    """
    current_id = "start"
    print()
    print_divider()

    # Walk the story graph node by node until an ending is hit.
    while True:
        node = STORY[current_id]
        display_text(node["text"])

        if node.get("ending"):
            achieved_endings.add(current_id)
            print()
            print_divider()
            print("THE END")
            print_divider()
            break

        if "choices" in node:
            answer = get_choice(node["prompt"], node["choices"])
            current_id = node["choices"][answer]
        else:
            press_enter_to_continue()
            current_id = node["next"]


def show_endings(achieved_endings):
    """Print every ending the player has unlocked so far.

    Loops over the master list of endings and reveals the name
    of each one the player has already reached, while keeping
    undiscovered endings hidden as a replay incentive.

    Args:
        achieved_endings: A set of ending ids the player has
            reached during this session.

    Returns:
        None
    """
    print()
    print_divider()
    print(
        f"ENDINGS DISCOVERED: {len(achieved_endings)} / "
        f"{len(ENDING_NAMES)}"
    )
    print_divider()
    for ending_id, name in ENDING_NAMES.items():
        if ending_id in achieved_endings:
            kind = STORY[ending_id]["ending_type"]
            print(f"[X] {name} ({kind})")
        else:
            print("[ ] ???")
    print_divider()


def show_instructions():
    """Print a short explanation of how to play the game.

    Returns:
        None
    """
    print()
    print_divider()
    display_text(
        "You will wake up and make a series of decisions that "
        "shape your day. At each decision point, type one of "
        "the options shown to choose what happens next. There "
        "is no single correct path. Some choices lead to "
        "success, some lead to disaster, and a surprising "
        "number of them lead to an untimely death. Play "
        "multiple times to discover every ending."
    )
    print_divider()


def show_title():
    """Print the game's title banner.

    Returns:
        None
    """
    print_divider()
    print("YOU WAKE UP")
    print("A Text-Based Adventure by Jonas Penner Mayoh")
    print_divider()


def main_menu():
    """Run the persistent main menu loop for the program.

    Continuously displays the menu until the user chooses to
    quit, dispatching to gameplay, the endings tracker, or the
    instructions screen based on validated input. This loop is
    what keeps the program running across multiple playthroughs.

    Returns:
        None
    """
    achieved_endings = set()
    menu_options = {"1", "2", "3", "4"}

    show_title()

    # The menu keeps looping until the user explicitly quits.
    while True:
        print()
        print("MAIN MENU")
        print("1. Play You Wake Up")
        print("2. View endings discovered")
        print("3. How to play")
        print("4. Quit")

        choice = get_choice(
            "What would you like to do? (1/2/3/4)", menu_options
        )

        if choice == "1":
            play_game(achieved_endings)
        elif choice == "2":
            show_endings(achieved_endings)
        elif choice == "3":
            show_instructions()
        else:
            print()
            print("Thanks for playing You Wake Up. Goodbye!")
            break


if __name__ == "__main__":
    main_menu()

