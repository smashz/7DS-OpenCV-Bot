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
WINDOW_NAME = "7DS"

def printr(text):
    print(f"{RED}{text}{RESET}")
    
def prints(text):
    print(f"{ELSE}{text}{RESET}")

def printy(text):
    print(f"{YELLOW}{text}{RESET}")

def printg(text):
    print(f"{GREEN}{text}{RESET}")

def get_window_bbox(window_name):
    """Get the bounding box (x, y, width, height) of a window by name."""
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        printr(f"Error: Window '{window_name}' not found!")
        return None
    win = windows[0]
    return (win.left, win.top, win.right, win.bottom)  # Bounding box

def find_and_click(image_path, confidence=0.65, offset_x=0, offset_y=0):
    """Scans for an image within the specified window and clicks it if found, with optional offset."""
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
        center_x = x + w // 2 + bbox[0] + offset_x
        center_y = y + h // 2 + bbox[1] + offset_y
        pyautogui.click(center_x, center_y)
        printg(f"Clicked on {image_path} at ({center_x}, {center_y}) with offset ({offset_x}, {offset_y})")
        time.sleep(1.5)
        return True
    return False


def main():
    always_scan = {
        "images/skip.png": 0.55,
        "images/start.png": 0.65,
        "images/complete.png": 0.65,
        "images/go_now.png": 0.65,
        "images/victory.png": 0.65,
        "images/auto_set.png": 0.65,
        "images/ep_clear.png": 0.65,
        "images/enter_battle.png": 0.65,
        "images/q_reward.png": 0.65,
        "images/q_info.png": 0.75,
        "images/q_banner.png": 0.75,
        "images/q_menu_banner.png": 0.75,
        "images/q_menu_banner1.png": 0.9,
        

        
    }

    trigger_images = {
        "images/skip.png": 0.65,
        "images/auto_set.png": 0.65,
        "images/victory.png": 0.65,
        
        
        
    }

    trigger_images2 = {
        "images/ok.png": 0.55,
        "images/event.png": 0.65,
        
    }

    post_trigger_images = {
        "images/start2.png": 0.65,
        
    }

    while True:
        trigger_clicked = False

        # Scan for all always_scan images
        for image, confidence in always_scan.items():
            if find_and_click(image, confidence):
                if image in trigger_images:
                    trigger_clicked = True  
                    

        # If a trigger image was clicked, wait 1 sec, then search for trigger_images2
        if trigger_clicked:
            printg("Trigger detected! Waiting 1 second before searching for trigger_images2...")
            time.sleep(0.5)

            trigger2_clicked = False
            for image, confidence in trigger_images2.items():
                if find_and_click(image, confidence):
                    trigger2_clicked = True
                    break  # Stop searching once a trigger_images2 image is clicked

            # If an image from trigger_images2 was clicked, check for post_trigger_images
            if trigger2_clicked:
                print("Trigger_images2 clicked! Now searching for post_trigger_images...")

                found = False
                for image, confidence in post_trigger_images.items():
                    time.sleep(0.5)
                    if find_and_click(image, confidence):
                        found = True
                        break  

                if not found:
                    printy("Post trigger image not found, returning to normal scanning.")

        time.sleep(0.5)  # Small delay for smooth scanning

if __name__ == "__main__":
    prints("Starting continuous image scan within window: " + WINDOW_NAME)
    main()
