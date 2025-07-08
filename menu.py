import subprocess
import keyboard
import time
import os

# Script list
scripts = {
    "1": "main_story_ch_7_up.py",
    "2": "creature_nest.py",
    "3": "boss_battle.py",
    "4": "test.py",
    
}

# Console colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ELSE = "\033[95m"
RESET = "\033[0m"

def printr(text):
    print(f"{RED}{text}{RESET}")

def prints(text):
    print(f"{ELSE}{text}{RESET}")

def printy(text):
    print(f"{YELLOW}{text}{RESET}")

def printg(text):
    print(f"{GREEN}{text}{RESET}")

def print_menu():
    printy("\nSelect a script to run:")
    for key, name in scripts.items():
        print(f"{key}. {name}")
    printr("Press X anytime to stop the script and return to menu.\n")

def run_script(script_path):
    printg(f"\nLaunching: {script_path}")
    process = subprocess.Popen(["python", script_path])

    try:
        while True:
            if keyboard.is_pressed('x'):
                printr("\n[X] pressed. Terminating script...")
                process.terminate()
                process.wait()
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        printy("\nInterrupted by user.")
        process.terminate()
        process.wait()

def main():
    while True:
        print_menu()
        choice = input("Enter script number (or q to quit): ").strip()
        
        if choice.lower() == "q":
            
            break
        elif choice not in scripts:
            printr("Invalid choice. Try again.")
        else:
            run_script(scripts[choice])

if __name__ == "__main__":
    main()
