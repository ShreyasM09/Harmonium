import cv2
import numpy as np
import pygame
import keyboard

# initialize sound
pygame.mixer.init()

sounds = {
    "a": pygame.mixer.Sound("sounds/C.wav"),
    "s": pygame.mixer.Sound("sounds/D.wav"),
    "d": pygame.mixer.Sound("sounds/E.wav"),
    "f": pygame.mixer.Sound("sounds/F.wav"),
    "g": pygame.mixer.Sound("sounds/G.wav"),
    "h": pygame.mixer.Sound("sounds/A.wav"),
    "j": pygame.mixer.Sound("sounds/B.wav")
}

# open webcam
cap = cv2.VideoCapture(0)

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

volume = 0

print("Move lid/hand near webcam to pump bellows")

while True:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(prev_gray, gray)
    airflow = np.sum(diff)

    # normalize airflow to volume
    volume = min(airflow / 5000000, 1)

    for key in sounds:
        if keyboard.is_pressed(key):
            sounds[key].set_volume(volume)
            sounds[key].play()

    prev_gray = gray

    cv2.imshow("Bellows Motion", diff)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()