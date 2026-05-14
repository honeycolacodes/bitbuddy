import time
import random
import json
import os

SAVE_FILE = "bitbuddy_save.json"

def load_buddy():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {
        "name": "Buddy",
        "hunger": 50,
        "happiness": 50,
        "energy": 50,
        "age": 0,
        "alive": True
    }

def save_buddy(buddy):
    with open(SAVE_FILE, "w") as f:
        json.dump(buddy, f)

def show_status(buddy):
    print("\n" + "="*30)
    print(f"  🐾 {buddy['name']} the BitBuddy")
    print("="*30)
    print(f"  Age:       {buddy['age']} days")
    print(f"  Hunger:    {'🟥' * (buddy['hunger'] // 10)}{'⬜' * (10 - buddy['hunger'] // 10)} {buddy['hunger']}/100")
    print(f"  Happiness: {'🟨' * (buddy['happiness'] // 10)}{'⬜' * (10 - buddy['happiness'] // 10)} {buddy['happiness']}/100")
    print(f"  Energy:    {'🟩' * (buddy['energy'] // 10)}{'⬜' * (10 - buddy['energy'] // 10)} {buddy['energy']}/100")
    print("="*30)

def get_mood(buddy):
    avg = (buddy['happiness'] + buddy['energy'] + (100 - buddy['hunger'])) / 3
    if avg > 70:
        return "😄 Happy and thriving!"
    elif avg > 40:
        return "😐 Doing okay..."
    else:
        return "😢 Not feeling great..."

def feed(buddy):
    if buddy['hunger'] <= 0:
        print("\n🍕 Buddy is stuffed and refuses to eat!")
        return
    buddy['hunger'] = max(0, buddy['hunger'] - 30)
    buddy['energy'] = min(100, buddy['energy'] + 10)
    print("\n🍕 Nom nom nom! Buddy loved that!")

def play(buddy):
    if buddy['energy'] < 20:
        print("\n😴 Buddy is too tired to play. Let them rest!")
        return
    buddy['happiness'] = min(100, buddy['happiness'] + 30)
    buddy['energy'] = max(0, buddy['energy'] - 20)
    buddy['hunger'] = min(100, buddy['hunger'] + 15)
    moves = ["does a backflip 🤸", "chases its tail 🌀", "zooms around the room 💨", "plays dead 💀 (just kidding!)"]
    print(f"\n🎾 Buddy {random.choice(moves)}")

def rest(buddy):
    if buddy['energy'] >= 100:
        print("\n⚡ Buddy is already full of energy!")
        return
    buddy['energy'] = min(100, buddy['energy'] + 40)
    buddy['happiness'] = max(0, buddy['happiness'] - 5)
    print("\n😴 Buddy takes a nap and snores loudly...")

def tick(buddy):
    # Time passing makes buddy hungrier, less happy, less energetic
    buddy['hunger'] = min(100, buddy['hunger'] + 10)
    buddy['happiness'] = max(0, buddy['happiness'] - 5)
    buddy['energy'] = max(0, buddy['energy'] - 5)
    buddy['age'] += 1

def check_alive(buddy):
    if buddy['hunger'] >= 100 and buddy['energy'] <= 0:
        buddy['alive'] = False
        print("\n💀 Oh no... Buddy didn't make it. You forgot about them!")
        print("Run the script again to start fresh.\n")
        os.remove(SAVE_FILE)
        return False
    return True

def rename(buddy):
    name = input("\n✏️  What do you want to name your buddy? ").strip()
    if name:
        buddy['name'] = name
        print(f"\n🎉 Say hello to {buddy['name']}!")

def main():
    buddy = load_buddy()

    if not buddy['alive']:
        print("💀 Your buddy is gone. Starting fresh...")
        buddy = load_buddy()

    print("\n🐾 Welcome to BitBuddy!")
    
    if buddy['age'] == 0:
        rename(buddy)

    while True:
        show_status(buddy)
        print(f"\n  Mood: {get_mood(buddy)}")
        print("\n  What do you want to do?")
        print("  [1] Feed Buddy")
        print("  [2] Play with Buddy")
        print("  [3] Let Buddy rest")
        print("  [4] Rename Buddy")
        print("  [5] Quit")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            feed(buddy)
        elif choice == "2":
            play(buddy)
        elif choice == "3":
            rest(buddy)
        elif choice == "4":
            rename(buddy)
        elif choice == "5":
            save_buddy(buddy)
            print(f"\n👋 Bye! {buddy['name']} will miss you!\n")
            break
        else:
            print("\n❓ Invalid choice, try again!")
            continue

        tick(buddy)
        if not check_alive(buddy):
            break

        save_buddy(buddy)
        time.sleep(0.5)

main()
