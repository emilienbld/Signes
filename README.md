# Contrôle de l'Ordinateur par Gestes

Ce projet utilise la caméra de l'ordinateur pour détecter des gestes de la main et exécuter différentes actions sur le PC. Grâce à la bibliothèque **MediaPipe**, les gestes sont interprétés et permettent de contrôler des fonctionnalités telles que la luminosité, le volume et la navigation sur le web.

## Explication des Signes

- 🤘🏻 **Lancer YouTube avec une vidéo** : Ouvre une vidéo prédéfinie sur YouTube.
- ☝🏻 **Monter la luminosité** : Augmente la luminosité de l'écran.
- 👇🏻 **Baisser la luminosité** : Diminue la luminosité de l'écran.
- 👌🏻 **Baisser le son** : Réduit le volume. Écarter les doigts augmente le son.
- 👋🏻 **Déplacer la souris** : Déplace le curseur de la souris en fonction de la position de la main.
- ✊🏻 **Clic droit** : Simule un clic droit lorsque la main est fermée.

## Prérequis

Assurez-vous d'avoir installé les bibliothèques suivantes :

```bash
pip install opencv-python mediapipe numpy pyautogui screen-brightness-control pycaw
```

## Fonctionnement

1. **Détection de la Main** : Le programme utilise MediaPipe pour détecter la position des mains.
2. **Contrôle de l'Ordinateur** :
   - Les gestes détectés sont interprétés pour exécuter des actions sur l'ordinateur (volume, luminosité, navigation).
   - Le curseur de la souris peut être déplacé avec la position de la main.

## Lancer le Programme

Pour démarrer le programme, exécutez le fichier Python :

```bash
python nom_du_fichier.py
```

Assurez-vous que votre caméra est activée et que vous avez les permissions nécessaires.

## Avertissement

Ce projet est principalement expérimental et éducatif. Les performances peuvent varier en fonction des conditions d'éclairage et de la configuration de la caméra.
