import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import screen_brightness_control as sbc
import webbrowser

def control_cursor(hand_landmarks):
    # Récupérer les coordonnées x et y du centre de la main
    wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
    x, y = wrist.x, wrist.y
    seuil = 0.05
    # Convertir les coordonnées de la main en coordonnées de l'écran
    screen_width, screen_height = pyautogui.size()
    x, y = int((1 - x) * screen_width), int(y * screen_height)  # Notez l'inversion de l'axe des x ici
    # Déplacer le curseur de la souris
    pyautogui.moveTo(x, y)
    # # Récupérer les coordonnées des extrémités du pouce et de l'index
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    # Calculer la distance entre le pouce et l'index
    distance_thumb_index = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    # Si la distance est inférieure à un certain seuil, considérez que la main est fermée et cliquez à la position actuelle du curseur
    if distance_thumb_index < seuil:
        pyautogui.click(x, y)

def control_brightness(hand_landmarks):
    # Récupérer les points de repère des bouts des doigts
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
    # Vérifier si le bout de l'index est au-dessus de tous les autres bouts des doigts
    if index_finger_tip.y < thumb_tip.y and index_finger_tip.y < middle_finger_tip.y and index_finger_tip.y < ring_finger_tip.y and index_finger_tip.y < pinky_tip.y:
        # Augmenter la luminosité de l'écran
        current_brightness = sbc.get_brightness()
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]
        sbc.set_brightness(min(100, current_brightness + 10))
    # Vérifier si le bout de l'index est en dessous de tous les autres bouts des doigts
    elif index_finger_tip.y > thumb_tip.y and index_finger_tip.y > middle_finger_tip.y and index_finger_tip.y > ring_finger_tip.y and index_finger_tip.y > pinky_tip.y:
        # Diminuer la luminosité de l'écran
        current_brightness = sbc.get_brightness()
        if isinstance(current_brightness, list):
            current_brightness = current_brightness[0]
        sbc.set_brightness(max(0, current_brightness - 10))

def control_volume(hand_landmarks):
    # Récupérer les points de repère du pouce et de l'index
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    # Calculer la distance euclidienne entre le pouce et l'index
    distance = np.sqrt((thumb_tip.x - index_finger_tip.x)**2 + (thumb_tip.y - index_finger_tip.y)**2 + (thumb_tip.z - index_finger_tip.z)**2)
    # Récupérer le niveau de volume actuel
    current_volume_level = volume_control.GetMasterVolumeLevel()
    # Récupérer les limites de volume
    min_volume_level, max_volume_level, _ = volume_control.GetVolumeRange()
    # Définir un seuil pour la distance entre le pouce et l'index
    threshold_distance = 0.05  # Vous pouvez ajuster cette valeur en fonction de vos besoins
    if distance < threshold_distance:  # Si la distance est inférieure au seuil (pouce et index proches)
        new_volume_level = current_volume_level - 1.0
        if new_volume_level >= min_volume_level:
            volume_control.SetMasterVolumeLevel(new_volume_level, None)
    else:  # Si la distance est supérieure au seuil (pouce et index éloignés)
        new_volume_level = current_volume_level + 1.0
        if new_volume_level <= max_volume_level:
            volume_control.SetMasterVolumeLevel(new_volume_level, None)

def control_browser(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]  
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

    distance_index_pinky = np.sqrt((index_finger_tip.x - pinky_tip.x)**2 + (index_finger_tip.y - pinky_tip.y)**2 + (index_finger_tip.z - pinky_tip.z)**2)
    distance_middle_ring = np.sqrt((middle_finger_tip.x - ring_finger_tip.x)**2 + (middle_finger_tip.y - ring_finger_tip.y)**2 + (middle_finger_tip.z - ring_finger_tip.z)**2)
    distance_thumb_middle = np.sqrt((thumb_tip.x - middle_finger_tip.x)**2 + (thumb_tip.y - middle_finger_tip.y)**2 + (thumb_tip.z - middle_finger_tip.z)**2)

    threshold_distance_close = 0.03  # Augmenter la valeur pour rendre le signe plus facile à faire
    threshold_distance_far = 0.05  # Augmenter la valeur pour rendre le signe plus facile à faire

    if distance_index_pinky > threshold_distance_far and distance_middle_ring < threshold_distance_close and distance_thumb_middle < threshold_distance_close:
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')



def detect_hand_landmarks(img, hands):
    output_img = img.copy()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(image=output_img,
                                                      landmark_list=hand_landmarks,
                                                      connections=mp.solutions.hands.HAND_CONNECTIONS,
                                                      landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(255, 255, 255), thickness=3, circle_radius=3),
                                                      connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(0, 255, 0), thickness=3, circle_radius=3))
            control_volume(hand_landmarks)
            control_cursor(hand_landmarks)
            control_brightness(hand_landmarks)
            control_browser(hand_landmarks)
    return output_img


# Initialisation de MediaPipe Hands
landmarker = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# Initialisation de la capture vidéo
camera_video = cv2.VideoCapture(0)
camera_video.set(3, 1280)
camera_video.set(4, 720)
# Initialisation de la bibliothèque pycaw pour le contrôle du volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))
volume_level = volume_control.GetMasterVolumeLevel()

# Boucle principale
while camera_video.isOpened():
    read, frame = camera_video.read()
    if not read:
        continue
    frame = detect_hand_landmarks(frame, landmarker)
    cv2.imshow('Hand Detection & Volume Control', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# Libérer la capture vidéo et fermer toutes les fenêtres
camera_video.release()
cv2.destroyAllWindows()
