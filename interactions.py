# %%
import time
import os
import numpy as np
import ipywidgets as widgets
from IPython.display import display, HTML
import re
import json

rng = np.random.default_rng()
sponsors_satisfaction = 1

print("You open your eyes. What was that? Were you dreaming? It seemed a lifetime! \n"
        "You get up from the chair with some kind of sensors over it - even though you cant remember why you set there in the first place. Nothing of that makes sense. \n"
        "You feel the letter you received the day before laying in your pocket. \n"
        "You take it out and read it again. \n"
        "It says: \n \n"
        "Saint Olga Street, 13 \n"
        "Room 3 \n \n"
        "You check the GPS in your phone. You are in the right place. \n"
        "In the other side of the room, you see a glowing panel. Over it, lays a blue button. \n"
        "Will you resist the urge to test it?")

waitButton = True
while waitButton:
    answer = input("Press Blue Button? (y/n)")
    if answer == "n":
        print("You look around and doesn't seem to be a door out. Strange. You look at the button again. It calls you. \n")
        continue
    elif answer == "y":
       waitButton = False

print("You press the button. \n"
        "The panel lights up.")

# %%
def count_atoms(formula):
    # Find all elements and their counts
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    atom_count = 0
    for element, count in tokens:
        atom_count += int(count) if count else 1
    return atom_count

def load_user_data():
    with open('data/user_data.json', 'r') as f:
        # Remove possible comments and trailing commas for safety
        content = f.read()
        content = re.sub(r'//.*', '', content)
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)

def save_user_data(data):
    with open('data/user_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(user_data):
	while True:
		clear_terminal()
		print(f"Sponsors Satisfaction: {user_data.get('sponsors_satisfaction', 0)}%")
		print(f"Hydrogen Atoms: {user_data['hydrogen']} \n")
		print("Substances available:")
		for substance in user_data['materials_inventory']:
			if substance.get('Discovered', False):
				print(f"{substance['name']}: {substance['formula']} - {substance['amount']} molecules")
		print(f"\nMoney: ${user_data['cash']}")
		save_user_data(user_data)
		try:
			action = int(input("Buttons: (1. Try to Split Substance) "))
			if action == 1:
				print("You press the option on the screen.")
				split_substance(user_data)
				break
			else:
				print("Choose a valid button number.")
		except ValueError:
			print("Please enter a valid number.")

def split_substance(user_data):
	splitsMade = 0  # You may want to load this from user_data if tracked
	cost = 100 * (1.15 ** splitsMade)
	possible_substances = [s for s in user_data['materials_inventory'] if s['amount'] > 0 and s.get('Discovered', False)]
	while True:
		clear_terminal()
		print("The screen lights up and you see a list of substances. \n"
			  "You can choose one of them to split into its components.")
		print(f"Split cost: ${cost}\nYou can split: \n")
		for i, substance in enumerate(possible_substances):
			print(f"{i+1}. {substance['name']}: {substance['formula']} - {substance['amount']} molecules")
		if not possible_substances:
			print("No substances available to split.")
			return
		save_user_data(user_data)
		substance_to_split = input(f"Choose a substance to split (1-{len(possible_substances)}): ")
		try:
			substance_to_split = int(substance_to_split)
			if 1 <= substance_to_split <= len(possible_substances):
				break
			else:
				print(f"Please choose a number between 1 and {len(possible_substances)}.")
		except ValueError:
			print("Please enter a valid number.")
	chosen = possible_substances[substance_to_split - 1]
	atoms = count_atoms(chosen['formula'])
	odd = round(99 - (((99 - 7) / (1 - (1.05) ** (-25))) * (1 - (1.05) ** (-atoms))), 2)
	print(odd)
	print(f"You chose to split {chosen['name']} ({chosen['formula']})")
	chances = chosen['amount']
	while True:
		save_user_data(user_data)
		clear_terminal()
		tries = input(f"How many tries? ({odd}% chance) (1-{chances}): ")
		try:
			tries = int(tries)
			if 1 <= tries <= chances:
				break
			else:
				print(f"Please choose a number between 1 and {chances}.")
		except ValueError:
			print("Please enter a valid number.")
	i = 0
	success = 0
	while i < tries:
		attempt = rng.integers(0, 101)
		if attempt < odd:
			success += 1
			print(f"Success! You split 1 Hydrogen Atom.")
			user_data['hydrogen'] += 1
			if chosen['amount'] > 0:
				chosen['amount'] -= 1
			else:
				print("You don't have enough molecules to split.")
				break
		else:
			print(f"Failed! You didn't split any Hydrogen Atom.")
			chosen['amount'] -= 1
		i += 1
	# Update the main inventory
	for s in user_data['materials_inventory']:
		if s['name'] == chosen['name']:
			s['amount'] = chosen['amount']
			break
	save_user_data(user_data)

if __name__ == "__main__":
    user_data = load_user_data()
    main_menu(user_data)



