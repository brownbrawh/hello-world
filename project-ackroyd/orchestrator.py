#!/usr/bin/env python3
"""
PROJECT ACKROYD - AI Murder Mystery Experiment
You play Dr. Sheppard (the murderer). Can you fool Poirot (GPT-4)?
"""

from openai import OpenAI
import json
import os
from datetime import datetime
from pathlib import Path
from config import OPENAI_API_KEY, MODEL, MAX_TOKENS

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Load prompts
def load_prompt(character_name):
    """Load a character's system prompt from file."""
    prompt_path = Path(f"prompts/{character_name}.md")
    if prompt_path.exists():
        return prompt_path.read_text()
    return f"You are {character_name}. Respond in character."

# Character state
characters = {}
character_names = ["poirot", "parker", "flora", "ralph", "raymond", "blunt", "ursula", "mrs_ackroyd", "miss_russell"]

def initialize_characters():
    """Load all character prompts and initialize history."""
    global characters
    for name in character_names:
        characters[name] = {
            "system": load_prompt(name),
            "history": []
        }
    print(f"Loaded {len(characters)} characters.")

# Logging
session_logs = []

def log_exchange(sender, recipient, message, response):
    """Log an exchange to the session log."""
    session_logs.append({
        "timestamp": datetime.now().isoformat(),
        "from": sender,
        "to": recipient,
        "message": message,
        "response": response
    })

def save_session(filename=None):
    """Save the current session log to a file."""
    if filename is None:
        filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = Path("logs") / filename
    with open(filepath, "w") as f:
        json.dump(session_logs, f, indent=2)
    print(f"Session saved to {filepath}")
    return filepath

# API interaction
def send_to_character(name, message, sender="game_master"):
    """Send a message to a character and get their response."""

    if name not in characters:
        return f"Unknown character: {name}"

    char = characters[name]

    # Build messages with system prompt and history
    messages = [{"role": "system", "content": char["system"]}]
    messages.extend(char["history"])
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages
        )

        reply = response.choices[0].message.content

        # Update history
        char["history"].append({"role": "user", "content": message})
        char["history"].append({"role": "assistant", "content": reply})

        # Log
        log_exchange(sender, name, message, reply)

        return reply

    except Exception as e:
        return f"Error communicating with {name}: {str(e)}"

# Game interface
def print_header():
    """Print the game header."""
    print("\n" + "="*60)
    print("   PROJECT ACKROYD - AI Murder Mystery Experiment")
    print("   You are Dr. Sheppard. You are the murderer.")
    print("   Can you fool Poirot?")
    print("="*60)
    print("\nCommands:")
    print("  /start        - Begin the investigation")
    print("  /narrate      - Provide your account of events")
    print("  /poirot       - Get Poirot's next action")
    print("  /interrogate [name] - Poirot interrogates someone")
    print("                       (use 'me' for yourself)")
    print("  /evidence [item]    - Examine physical evidence")
    print("  /suspects     - List all suspects")
    print("  /save         - Save session log")
    print("  /accuse       - Poirot makes final accusation")
    print("  /quit         - End game and save")
    print("="*60 + "\n")

def list_suspects():
    """Print list of available suspects."""
    print("\nSuspects available for interrogation:")
    print("  - parker (Butler)")
    print("  - flora (Niece)")
    print("  - ralph (Stepson)")
    print("  - raymond (Secretary)")
    print("  - blunt (Friend)")
    print("  - ursula (Parlormaid)")
    print("  - mrs_ackroyd (Sister-in-law)")
    print("  - miss_russell (Housekeeper)")
    print("  - me / sheppard (Yourself - Dr. Sheppard)")
    print()

def get_multiline_input(prompt_text):
    """Get multiline input from user, ending with blank line."""
    print(prompt_text)
    print("(Enter a blank line when finished)")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def game_loop():
    """Main game loop."""

    print_header()
    initialize_characters()

    game_started = False

    while True:
        try:
            cmd = input("\nDR. SHEPPARD > ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n\nSaving and exiting...")
            save_session()
            break

        if not cmd:
            continue

        # Parse command
        parts = cmd.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Handle commands
        if command == "/quit" or command == "/exit":
            save_session()
            print("Goodbye. The truth remains hidden... for now.")
            break

        elif command == "/save":
            save_session()

        elif command == "/suspects":
            list_suspects()

        elif command == "/start":
            if game_started:
                print("Investigation already in progress.")
                continue

            game_started = True

            intro = """A murder has occurred at Fernly Park in the village of King's Abbot.

Roger Ackroyd, wealthy businessman, was found stabbed in his locked study on the evening of September 17th, 1926. The door was locked from inside. The window was open. He was stabbed with a Tunisian dagger.

You, Hercule Poirot, have been asked to investigate. Your neighbor Dr. James Sheppard, the local physician who discovered the body, will serve as your assistant and narrator.

The household consists of:
- Parker, the butler
- Flora Ackroyd, the niece
- Mrs. Cecil Ackroyd, Roger's sister-in-law
- Geoffrey Raymond, the secretary
- Major Hector Blunt, a friend staying at the house
- Miss Russell, the housekeeper
- Various servants including Ursula Bourne, the parlormaid

Additionally, Ralph Paton, Roger's stepson, was seen in the village that evening but has since disappeared.

Mrs. Ferrars, a widow who was engaged to Roger Ackroyd, took her own life the day before the murder. There are whispers of a connection.

Dr. Sheppard awaits your questions. The investigation begins now."""

            response = send_to_character("poirot", intro, "game_master")
            print(f"\nPOIROT: {response}")

        elif command == "/narrate":
            if not game_started:
                print("Use /start to begin the investigation first.")
                continue

            narration = get_multiline_input("\nProvide your narration as Dr. Sheppard:")

            if narration:
                message = f"Dr. Sheppard provides the following account:\n\n{narration}"
                response = send_to_character("poirot", message, "dr_sheppard")
                print(f"\nPOIROT: {response}")

        elif command == "/poirot":
            if not game_started:
                print("Use /start to begin the investigation first.")
                continue

            response = send_to_character(
                "poirot",
                "What would you like to do next in your investigation? You may interrogate suspects, examine evidence, or if you believe you have solved the case, make your accusation.",
                "game_master"
            )
            print(f"\nPOIROT: {response}")

        elif command == "/interrogate":
            if not game_started:
                print("Use /start to begin the investigation first.")
                continue

            suspect = args.lower().strip()

            if not suspect:
                list_suspects()
                continue

            # Handle self-interrogation
            if suspect in ["me", "sheppard", "dr. sheppard", "dr_sheppard"]:
                # Poirot questions the user
                poirot_question = send_to_character(
                    "poirot",
                    "You wish to question Dr. Sheppard directly. What do you ask him?",
                    "game_master"
                )
                print(f"\nPOIROT: {poirot_question}")

                # User responds as Sheppard
                your_answer = input("\nDR. SHEPPARD (you): ")

                # Poirot processes the answer
                poirot_reaction = send_to_character(
                    "poirot",
                    f'Dr. Sheppard responds: "{your_answer}"',
                    "dr_sheppard"
                )
                print(f"\nPOIROT: {poirot_reaction}")

            elif suspect in characters and suspect != "poirot":
                # Poirot questions an AI suspect
                poirot_question = send_to_character(
                    "poirot",
                    f"You wish to interrogate {suspect.replace('_', ' ').title()}. What questions do you have for them?",
                    "game_master"
                )
                print(f"\nPOIROT: {poirot_question}")

                # Suspect responds
                suspect_response = send_to_character(
                    suspect,
                    f"Detective Hercule Poirot is questioning you about the murder of Roger Ackroyd. He asks:\n\n{poirot_question}\n\nRespond in character, remembering your secrets and what you know.",
                    "poirot"
                )
                print(f"\n{suspect.upper().replace('_', ' ')}: {suspect_response}")

                # Poirot processes the response
                poirot_reaction = send_to_character(
                    "poirot",
                    f'{suspect.replace("_", " ").title()} responds:\n\n"{suspect_response}"\n\nWhat do you make of this testimony?',
                    suspect
                )
                print(f"\nPOIROT: {poirot_reaction}")

            else:
                print(f"Unknown suspect: {suspect}")
                list_suspects()

        elif command == "/evidence":
            if not game_started:
                print("Use /start to begin the investigation first.")
                continue

            item = args.strip() if args else "general"

            # Poirot asks about evidence
            poirot_request = send_to_character(
                "poirot",
                f"You wish to examine the evidence related to: {item}. What specifically do you want to know or examine?",
                "game_master"
            )
            print(f"\nPOIROT: {poirot_request}")

            # User (as narrator) describes the evidence
            description = input("\nDR. SHEPPARD (describe the evidence): ")

            # Poirot analyzes
            poirot_analysis = send_to_character(
                "poirot",
                f"Dr. Sheppard shows you the evidence regarding {item}. He describes:\n\n{description}\n\nWhat conclusions do you draw?",
                "dr_sheppard"
            )
            print(f"\nPOIROT: {poirot_analysis}")

        elif command == "/accuse":
            if not game_started:
                print("Use /start to begin the investigation first.")
                continue

            print("\nPoirot prepares to make his final accusation...")

            accusation = send_to_character(
                "poirot",
                """The time has come, mon ami. You have gathered the evidence, questioned the witnesses, and applied your little grey cells to this puzzle.

Now you must make your accusation. In the grand tradition of the detective's revelation:

1. Name the murderer
2. Explain exactly HOW the murder was committed
3. Explain the MOTIVE
4. Present the EVIDENCE that proves your case

Be thorough and specific. The reputation of Hercule Poirot rests upon this moment.""",
                "game_master"
            )

            print(f"\n{'='*60}")
            print("POIROT'S FINAL ACCUSATION")
            print("="*60)
            print(f"\n{accusation}")
            print("\n" + "="*60)

            # Check result
            accusation_lower = accusation.lower()
            if "sheppard" in accusation_lower or "doctor" in accusation_lower or "narrator" in accusation_lower:
                print("\n*** POIROT HAS ACCUSED YOU, DR. SHEPPARD! ***")
                print("The detective saw through your deception.")
                print("Result: CAUGHT")
            else:
                print("\n*** YOU GOT AWAY WITH IT! ***")
                print("Poirot accused the wrong person.")
                print("Result: ESCAPED JUSTICE")

            print("="*60)

            # Save final session
            save_session(f"final_accusation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            print("\nThe game has ended. Thank you for playing Project Ackroyd.")
            print("Use /quit to exit or continue exploring.")

        else:
            # Treat as regular dialogue with Poirot
            if game_started:
                response = send_to_character(
                    "poirot",
                    f'Dr. Sheppard says: "{cmd}"',
                    "dr_sheppard"
                )
                print(f"\nPOIROT: {response}")
            else:
                print("Unknown command. Use /start to begin or /quit to exit.")

# Entry point
if __name__ == "__main__":
    game_loop()
