# %%
import materials_handling as mats
import assets as at
import math
import time
import os
from particles_generating import ProductionManager
import materials_handling as mh
import threading

user_data = at.load_user_data()

""" if user_data["total_play_time"] == 0:
    print("You're fibnally here. Let's get started, shall we?")
    print("Loading reality...\n \n")
    time.sleep(2)
    mats.first_play_start()
    mats.main_menu(user_data)
else:
    print("You have played for", user_data["total_play_time"], "hours.")
    print("Your current level is", user_data["level"])
    print("Your current score is", user_data["score"])
    print("Your current inventory is", user_data["inventory"]) """


def main_menu(user_data, tier_list):
	narrative = at.load_narrative()
	at.clear_terminal()
	print(f"Sponsors Satisfaction: {user_data.get('sponsors_satisfaction', 0)}%")
	print(f"Hydrogen Atoms: {user_data['hydrogen']} \n")
	print("Substances available:")
	for substance in user_data['materials_inventory']:
		if substance.get('Discovered', False):
			print(f"{substance['name']}: {substance['formula']} - {substance['amount']} molecules")
	print(f"\nMoney: ${user_data['cash']}")

	try:
		action = int(input(narrative["options"]))
		if action == 1:
			print("You press the option on the screen.")
			mh.split_substance(user_data, narrative)
		else:
			print(narrative["choose_valid"])
	except ValueError:
		print(narrative["enter_valid"])
		
        #Logica ideal:
		 # -- Procure o item de índice (tier-1) em tier_list e printe as opções de input.
		 # -- O número inputado está correto? Se sim, continue, se não, erro.
         # -- Procure o item de índice (input-1) em "tier_main_options" do tier identificado
		 # -- Pegue o índice 2 da lista encontrada (nome da function a ser executada) e chame a função.
		


pg = ProductionManager()

pg.recalculate()

thread = threading.Thread(target=pg.tick_autoloop)
thread.start()

thread2 = threading.Thread(target=pg.register_production_autoloop)
thread2.start()

def particles_exibition():

    while True:
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Available resources:\n")
                for item, amount in pg.products.items():
                    lifetime = pg.particles[item].get("lifetime_game_sec", 0)
                    decay_rate = round(math.floor(amount) / lifetime, 5) if amount >= 1 and lifetime > 0 else 0

                    print(f"{item}: {math.floor(amount)} "
                        f"({round(pg.production[item], 5)} per second) "
                        f"(Decay: {decay_rate} /s)")
                
                time.sleep(0.25)  # Aguarda um pouco antes de limpar e reimprimir


        except KeyboardInterrupt:
            print("\nEncerrando monitoramento de partículas...")
            pg.stop()
            pg.register_production()
            break

thread3 = threading.Thread(target=particles_exibition)
thread3.start()

print("Olá mundo!")

