import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import screen_brightness_control as sbc
import webbrowser

def control_curseur(landmarks_main):
    # Récupérer les coordonnées x et y du centre de la main
    poignet = landmarks_main.landmark[mp.solutions.hands.HandLandmark.WRIST]
    x, y = poignet.x, poignet.y
    seuil = 0.05
    # Convertir les coordonnées de la main en coordonnées de l'écran
    largeur_ecran, hauteur_ecran = pyautogui.size()
    x, y = int((1 - x) * largeur_ecran), int(y * hauteur_ecran)  # Notez l'inversion de l'axe des x ici
    # Déplacer le curseur de la souris
    pyautogui.moveTo(x, y)
    # Récupérer les coordonnées des extrémités du pouce et de l'index
    bout_pouce = landmarks_main.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    bout_index = landmarks_main.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    # Calculer la distance entre le pouce et l'index
    distance_pouce_index = ((bout_pouce.x - bout_index.x) ** 2 + (bout_pouce.y - bout_index.y) ** 2) ** 0.5
    # Si la distance est inférieure à un certain seuil, considérez que la main est fermée et cliquez à la position actuelle du curseur
    if distance_pouce_index < seuil:
        pyautogui.click(x, y)

def control_luminosite(landmarks_main):
    # Récupérer les points de repère des bouts des doigts
    bout_pouce = landmarks_main.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    bout_index = landmarks_main.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    bout_majeur = landmarks_main.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    bout_annulaire = landmarks_main.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    bout_auriculaire = landmarks_main.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
    # Vérifier si le bout de l'index est au-dessus de tous les autres bouts des doigts
    if bout_index.y < bout_pouce.y and bout_index.y < bout_majeur.y and bout_index.y < bout_annulaire.y and bout_index.y < bout_auriculaire.y:
        # Augmenter la luminosité de l'écran
        luminosite_actuelle = sbc.get_brightness()
        if isinstance(luminosite_actuelle, list):
            luminosite_actuelle = luminosite_actuelle[0]
        sbc.set_brightness(min(100, luminosite_actuelle + 10))
    # Vérifier si le bout de l'index est en dessous de tous les autres bouts des doigts
    elif bout_index.y > bout_pouce.y and bout_index.y > bout_majeur.y and bout_index.y > bout_annulaire.y and bout_index.y > bout_auriculaire.y:
        # Diminuer la luminosité de l'écran
        luminosite_actuelle = sbc.get_brightness()
        if isinstance(luminosite_actuelle, list):
            luminosite_actuelle = luminosite_actuelle[0]
        sbc.set_brightness(max(0, luminosite_actuelle - 10))

def control_volume(landmarks_main):
    # Récupérer les points de repère du pouce et de l'index
    bout_pouce = landmarks_main.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    bout_index = landmarks_main.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    # Calculer la distance euclidienne entre le pouce et l'index
    distance = np.sqrt((bout_pouce.x - bout_index.x)**2 + (bout_pouce.y - bout_index.y)**2 + (bout_pouce.z - bout_index.z)**2)
    # Récupérer le niveau de volume actuel
    niveau_volume_actuel = volume_control.GetMasterVolumeLevel()
    # Récupérer les limites de volume
    niveau_volume_min, niveau_volume_max, _ = volume_control.GetVolumeRange()
    # Définir un seuil pour la distance entre le pouce et l'index
    seuil_distance = 0.05
    if distance < seuil_distance:  # Si la distance est inférieure au seuil (pouce et index proches)
        nouveau_niveau_volume = niveau_volume_actuel - 1.0
        if nouveau_niveau_volume >= niveau_volume_min:
            volume_control.SetMasterVolumeLevel(nouveau_niveau_volume, None)
    else:  # Si la distance est supérieure au seuil (pouce et index éloignés)
        nouveau_niveau_volume = niveau_volume_actuel + 1.0
        if nouveau_niveau_volume <= niveau_volume_max:
            volume_control.SetMasterVolumeLevel(nouveau_niveau_volume, None)

def control_navigateur(landmarks_main):
    bout_index = landmarks_main.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    bout_majeur = landmarks_main.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    bout_annulaire = landmarks_main.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    bout_auriculaire = landmarks_main.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]  
    bout_pouce = landmarks_main.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

    distance_index_auriculaire = np.sqrt((bout_index.x - bout_auriculaire.x)**2 + (bout_index.y - bout_auriculaire.y)**2 + (bout_index.z - bout_auriculaire.z)**2)
    distance_majeur_annulaire = np.sqrt((bout_majeur.x - bout_annulaire.x)**2 + (bout_majeur.y - bout_annulaire.y)**2 + (bout_majeur.z - bout_annulaire.z)**2)
    distance_pouce_majeur = np.sqrt((bout_pouce.x - bout_majeur.x)**2 + (bout_pouce.y - bout_majeur.y)**2 + (bout_pouce.z - bout_majeur.z)**2)

    seuil_distance_proche = 0.03
    seuil_distance_loin = 0.05

    if distance_index_auriculaire > seuil_distance_loin and distance_majeur_annulaire < seuil_distance_proche and distance_pouce_majeur < seuil_distance_proche:
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

def detecter_landmarks_main(image, detecteur_mains):
    image_resultat = image.copy()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resultat = detecteur_mains.process(image_rgb)
    if resultat.multi_hand_landmarks:
        for landmarks_main in resultat.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(image=image_resultat,
                                                      landmark_list=landmarks_main,
                                                      connections=mp.solutions.hands.HAND_CONNECTIONS,
                                                      landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(255, 255, 255), thickness=3, circle_radius=3),
                                                      connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                          color=(0, 255, 0), thickness=3, circle_radius=3))
            control_volume(landmarks_main)
            control_curseur(landmarks_main)
            control_luminosite(landmarks_main)
            control_navigateur(landmarks_main)
    return image_resultat

# Initialisation de MediaPipe Hands
detecteur_mains = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# Initialisation de la capture vidéo
camera_video = cv2.VideoCapture(0)
camera_video.set(3, 1280)
camera_video.set(4, 720)
# Initialisation de la bibliothèque pycaw pour le contrôle du volume
appareils = AudioUtilities.GetSpeakers()
interface = appareils.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))
niveau_volume = volume_control.GetMasterVolumeLevel()

# Boucle principale
while camera_video.isOpened():
    read, frame = camera_video.read()
    if not read:
        continue
    frame = detecter_landmarks_main(frame, detecteur_mains)
    cv2.imshow('Détection de la main et contrôle du volume', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# Libérer la capture vidéo et fermer toutes les fenêtres
camera_video.release()
cv2.destroyAllWindows()
