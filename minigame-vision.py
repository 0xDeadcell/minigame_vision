import pyautogui as pyag
import os
import cv2
import time
from random import choice

cwd = os.path.dirname(os.path.abspath(__file__)) + "\\"
# images = "screen-captures"
static_images = "static-captures"
os.chdir(cwd)
last_minigame_choice = []


def startup():
    try:
        os.mkdir(static_images)
        # os.mkdir(images)

    except FileExistsError:
        print(f"[!]Path already exists => {cwd}{static_images}\n")

    # print(f"[+] Attempting to clean up last sessions screen-captures in: {images}")

    # for old_images in os.listdir(images):
    #     # We will remove old screen captures if they start with "dynamic-capture"
    #     if old_images.startswith("dynamic-capture"):
    #         os.remove(old_images)

    print("Please navigate to `https://animesoul.com/mini-games`, the script is starting in...")
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1\n')
    time.sleep(1)


def begin_game():
    enter_game = "enter-minigame.PNG"
    try:
        # We try locating all minigames on the screen, but only select the last one found
        # It returns a generator object, so we turn it into a list
        region = list(pyag.locateAllOnScreen(f"{cwd}{static_images}\\{enter_game}", grayscale=False, confidence=0.8))
        x, y = pyag.center(choice(region))

        # Check to see if the random choice we made was already done last round, if so go to the last choice in the list
        if f"{x},{y}" in last_minigame_choice:
            # We JUST clicked on this minigame, let's do another one.
            x, y = pyag.center(region[-1])
        
        if x and y:
            pyag.moveTo(x, y, duration=0.2, tween=pyag.easeOutElastic)
            pyag.click(x, y)
            print("[+] Clicked on enter-minigame button!")
            last_minigame_choice.append(f"{x},{y}")
            click_card() # After we have confirmed that we clicked on the enter-minigame button, we will continue to the next step

    except Exception as e:
        print(e)
        print(f"\n[!] Could not locate a game to play! [{enter_game}]")


def click_card():
    pick_card = "hidden-card.PNG"
    pyag.scroll(-250)
    
    time.sleep(0.5)

    # We try finding a card to choose 3 times then try to go back, or break and go back if found
    for _ in range(3):
        try:
            card_region = list(pyag.locateAllOnScreen(f"{cwd}{static_images}\\{pick_card}", grayscale=False, confidence=0.9))
            x, y = pyag.center(choice(card_region))
            if x and y:
                pyag.moveTo(x, y, duration=0.15, tween=pyag.easeOutElastic)
                pyag.click(x, y)
                print("[+] Tried picking a card!")
            break

        except Exception:
            print(f"[!] Could not pick a card! [{pick_card}]")


startup()
while True:
    pyag.press("f5")
    time.sleep(0.8)
    begin_game()
    time.sleep(0.5)
    pyag.press("browserback")
    print("[+] Went back to play another minigame!")
    
    if len(last_minigame_choice) > 3:
        last_minigame_choice.pop(0)
        # Remove the oldest result so we can keep playing