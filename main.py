# %%
import materials_handling as mats
import assets as at
import time

user_data = at.load_user_data()

if user_data["total_play_time"] == 0:
    print("You're fibnally here. Let's get started, shall we?")
    print("Loading reality...\n \n")
    time.sleep(2)
    mats.first_play_start()
    mats.main_menu(user_data)
else:
    print("You have played for", user_data["total_play_time"], "hours.")
    print("Your current level is", user_data["level"])
    print("Your current score is", user_data["score"])
    print("Your current inventory is", user_data["inventory"])





