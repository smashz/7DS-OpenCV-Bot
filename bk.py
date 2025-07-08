import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
from PIL import ImageGrab

# Console colors for logging
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ELSE = "\033[95m"
RESET = "\033[0m"

# Window name to search
WINDOW_NAME = "memu"

def printr(text):
    print(f"{RED}{text}{RESET}")
    
def prints(text):
    print(f"{ELSE}{text}{RESET}")

def printy(text):
    print(f"{YELLOW}{text}{RESET}")

def printg(text):
    print(f"{GREEN}{text}{RESET}")

def get_window_bbox(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        printr(f"Error: Window '{window_name}' not found!")
        return None
    win = windows[0]
    return (win.left, win.top, win.right, win.bottom)

def find_and_click(image_path, confidence=0.65):
    bbox = get_window_bbox(WINDOW_NAME)
    if not bbox:
        printr("Window not found! Retrying in 2 seconds...")
        time.sleep(2)
        return False

    screen = ImageGrab.grab(bbox)
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        printr(f"Error: Could not load {image_path}")
        return False

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        x, y = max_loc
        w, h = template.shape[::-1]
        center_x, center_y = x + w // 2 + bbox[0], y + h // 2 + bbox[1]
        pyautogui.click(center_x, center_y)
        printg(f"Clicked on {image_path} at ({center_x}, {center_y})")
        time.sleep(1.5)
        return True
    return False

def find_most_frequent_and_click(image_paths_conf, bbox):
    screen = ImageGrab.grab(bbox)
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    match_counts = {}
    match_positions = {}

    for image_path, confidence in image_paths_conf.items():
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            printr(f"Error: Could not load {image_path}")
            continue

        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= confidence)

        points = list(zip(*loc[::-1]))  # (x, y)
        match_counts[image_path] = len(points)
        match_positions[image_path] = points

    if not match_counts:
        return False

    most_common = max(match_counts, key=match_counts.get)
    count = match_counts[most_common]

    if count == 0:
        return False

    first_match = match_positions[most_common][0]
    template = cv2.imread(most_common, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    center_x = first_match[0] + w // 2 + bbox[0]
    center_y = first_match[1] + h // 2 + bbox[1]

    pyautogui.click(center_x, center_y)
    printg(f"Clicked on most common: {most_common} with {count} matches at ({center_x}, {center_y})")
    time.sleep(1.5)
    return True

def main():
    always_scan = {
        "images/skip.png": 0.65,   
        "images/skip2.png": 0.65,
        "images/start.png": 0.65,
        "images/start2.png": 0.65,
        "images/complete.png": 0.65,
        "images/go_now.png": 0.65,
        "images/victory.png": 0.65,
        "images/auto_set.png": 0.65,
        "images/ep_clear.png": 0.65,
        "images/enter_battle.png": 0.65,
        "images/b_banner.png": 0.65,
        "images/level_1.png": 0.75,
        "images/auto_clear.png": 0.95,
        "images/ok.png": 0.65,
        "images/potion.png": 0.85,
        "images/ai.png": 0.85,
        "images/invite_ai.png": 0.85,
        "images/preparation.png": 0.65,
        "images/auto_off.png": 0.9,
        "images/hell.png": 0.8,
        "images/use_potion.png": 0.65,
        "images/boss_start.png": 0.65,
    }

    trigger_images = {
        "images/nest_save_team.png": 0.65,
        "images/victory.png": 0.65,
        "images/ok.png": 0.8,
        "images/lv1_b1.png": 0.8,
        "images/lv1_b2.png": 0.8,
        "images/lv1_b3.png": 0.8,
        "images/lv2_b1.png": 0.85,
        "images/lv2_b2.png": 0.85,
    }

    trigger_images2 = {
        "images/ok.png": 0.8,
        
        "images/lv1_b1.png": 0.8,
        "images/lv1_b2.png": 0.8,
        "images/lv1_b3.png": 0.8,
        "images/lv2_b1.png": 0.85,
        "images/lv2_b2.png": 0.85,
    }

    post_trigger_images = {
        "images/use.png": 0.55,
    }

    lv1_b_images = {
        "images/lv1_b1.png": 0.8,
        "images/lv1_b2.png": 0.8,
        "images/lv1_b3.png": 0.8,
    }

    while True:
        # Step 1: Try to click any always_scan image
        for image, confidence in always_scan.items():
            if find_and_click(image, confidence):
                printg(f"Clicked always_scan image: {image}")
                time.sleep(0.5)

                # Step 2: If clicked, search for a trigger image
                for trig_img, trig_conf in trigger_images.items():
                    if find_and_click(trig_img, trig_conf):
                        printg(f"Clicked trigger image: {trig_img}")
                        time.sleep(0.5)

                        # Step 3: Search for trigger_images2
                        for trig2_img, trig2_conf in trigger_images2.items():
                            if find_and_click(trig2_img, trig2_conf):
                                printg(f"Clicked trigger_images2 image: {trig2_img}")
                                time.sleep(0.5)

                                # Step 4: Search for post_trigger_images
                                for post_img, post_conf in post_trigger_images.items():
                                    if find_and_click(post_img, post_conf):
                                        printg(f"Clicked post_trigger_image: {post_img}")
                                        break  # optional: stop after first found

                                # Step 5: Analyze lv1_b images and click most frequent
                                bbox = get_window_bbox(WINDOW_NAME)
                                if bbox:
                                    if find_most_frequent_and_click(lv1_b_images, bbox):
                                        printg("Clicked most frequent lv1_b image.")
                                break  # stop after full chain

                        break  # stop trigger chain after success
                break  # stop always_scan loop once one image is clicked

        time.sleep(0.5)


if __name__ == "__main__":
    prints("Starting continuous image scan within window: " + WINDOW_NAME)
    main()
