# Sidescroller
Jeu sidescroller

Un système de score affiche la distance maximale parcourue par le joueur. Le
score est réinitialisé en appuyant sur **R** après un Game Over.

## Sol gris

Le sol continu visible en bas de l'écran est dessiné avec la couleur
`GROUND_COLOR` définie dans `sidescroller_chat.py`.  Il est possible de :

* modifier cette couleur en changeant la valeur de `GROUND_COLOR` ;
* ne pas afficher le sol en passant `show_ground=False` lors de la création du
  `Level` (voir la fonction `reset_game`) ;
* appliquer une texture en fournissant une surface via le paramètre
  `ground_texture`.
