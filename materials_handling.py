# %%
import time
import os
import numpy as np
import ipywidgets as widgets
from IPython.display import display, HTML
import re
import json
import assets as at

rng = np.random.default_rng()
sponsors_satisfaction = 1


# %%
def count_atoms(formula):
    # Find all elements and their counts
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    atom_count = 0
    for element, count in tokens:
        atom_count += int(count) if count else 1
    return atom_count

def main_menu(user_data):
	narrative = at.load_narrative()
	while True:
		at.clear_terminal()
		print(f"Sponsors Satisfaction: {user_data.get('sponsors_satisfaction', 0)}%")
		print(f"Hydrogen Atoms: {user_data['hydrogen']} \n")
		print("Substances available:")
		for substance in user_data['materials_inventory']:
			if substance.get('Discovered', False):
				print(f"{substance['name']}: {substance['formula']} - {substance['amount']} molecules")
		print(f"\nMoney: ${user_data['cash']}")
		at.save_user_data(user_data)
		try:
			action = int(input(narrative["split_option"]))
			if action == 1:
				print("You press the option on the screen.")
				split_substance(user_data, narrative)
				break
			else:
				print(narrative["choose_valid"])
		except ValueError:
			print(narrative["enter_valid"])

def split_substance(user_data, narrative):
	splitsMade = 0
	cost = 100 * (1.15 ** splitsMade)
	possible_substances = [s for s in user_data['materials_inventory'] if s['amount'] > 0 and s.get('Discovered', False)]
	while True:
		at.clear_terminal()
		print(narrative["main_menu"])
		print(narrative["split_cost"].format(cost=cost))
		for i, substance in enumerate(possible_substances):
			print(f"{i+1}. {substance['name']}: {substance['formula']} - {substance['amount']} molecules")
		if not possible_substances:
			print(narrative["no_substances"])
			return
		at.save_user_data(user_data)
		substance_to_split = input(narrative["split_choose"].format(max=len(possible_substances)))
		try:
			substance_to_split = int(substance_to_split)
			if 1 <= substance_to_split <= len(possible_substances):
				break
			else:
				print(narrative["split_invalid"].format(max=len(possible_substances)))
		except ValueError:
			print(narrative["enter_valid"])
	chosen = possible_substances[substance_to_split - 1]
	atoms = count_atoms(chosen['formula'])
	odd = round(99 - (((99 - 7) / (1 - (1.05) ** (-25))) * (1 - (1.05) ** (-atoms))), 2)
	print(f"You chose to split {chosen['name']} ({chosen['formula']})")
	chances = chosen['amount']
	while True:
		at.save_user_data(user_data)
		at.clear_terminal()
		tries = input(narrative["split_tries"].format(odd=odd, chances=chances))
		try:
			tries = int(tries)
			if 1 <= tries <= chances:
				break
			else:
				print(narrative["split_invalid"].format(max=chances))
		except ValueError:
			print(narrative["enter_valid"])
	i = 0
	success = 0
	while i < tries:
		attempt = rng.integers(0, 101)
		if attempt > odd:
			success += 1
			print(narrative["split_success"])
			user_data['hydrogen'] += 1
			if chosen['amount'] > 0:
				chosen['amount'] -= 1
			else:
				print(narrative["split_not_enough"])
				break
		else:
			print(narrative["split_fail"])
			chosen['amount'] -= 1
		i += 1
	# Update the main inventory
	for s in user_data['materials_inventory']:
		if s['name'] == chosen['name']:
			s['amount'] = chosen['amount']
			break
	at.save_user_data(user_data)


def first_play_start():
	narrative = at.load_narrative()
	for line in narrative["intro"]:
		print(line)

	waitButton = True
	while waitButton:
		answer = input(narrative["button_prompt"])
		if answer == "n":
			print(narrative["button_resist"])
			continue
		elif answer == "y":
			waitButton = False

	print(narrative["button_press"])


if __name__ == "__main__":
    user_data = at.load_user_data()
    main_menu(user_data)



