import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab

# SETTINGS
IMAGE_PATH = "images/q_icon_circle.png"  # Change to your image
WINDOW_NAME = "7DS"                      # Change to your game/window name
CONFIDENCE_THRESHOLD = 0.29            # Minimum confidence to display match

def get_window_bbox(window_name):
    """Get the bounding box of the window to capture."""
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        print(f"Window '{window_name}' not found.")
        return None
    win = windows[0]
    return (win.left, win.top, win.right, win.bottom)

def main():
    template = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Could not load image {IMAGE_PATH}")
        return
    w, h = template.shape[::-1]

    bbox = get_window_bbox(WINDOW_NAME)
    if not bbox:
        return

    while True:
        # Capture screen in that window
        screen = ImageGrab.grab(bbox=bbox)
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

        # Template matching
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Draw result if match is good enough
        display_frame = screen_np.copy()
        if max_val >= CONFIDENCE_THRESHOLD:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(display_frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Confidence: {max_val:.2f}", (top_left[0], top_left[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(display_frame, f"Confidence: {max_val:.2f} (No match)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Image Tracker", cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR))

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
