## Sidescroller
Jeu défilement horizontal.

Un système de score affiche la distance maximale parcourue par le joueur. Le score est réinitialisé en appuyant sur **R** après un Game Over.

## Extraction des sprites

Le script `extract_frames.py` permet de découper les sprite sheets du jeu en images individuelles de 256 × 341 pixels (6 colonnes × 3 lignes).

Exemple d'utilisation :

```bash
python extract_frames.py Imagesidescroller/Chatanimation.png output/chat --prefix chat
python extract_frames.py Imagesidescroller/Chienanimation.png output/chien --prefix chien

