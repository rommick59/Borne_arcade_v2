#!/bin/bash
xdotool mousemove 1280 1024
cd projet/UtArcade
javac Main.java

# Lancer le jeu en arrière-plan pour pouvoir cibler sa fenêtre
java Main &
PID=$!

# Attendre la création de la fenêtre puis demander au gestionnaire de fenêtres
# de la mettre en plein écran sans changer la résolution d'affichage.
# Nécessite `xdotool` et `wmctrl` installés.
for i in $(seq 1 40); do
	sleep 0.1
	WIN=$(xdotool search --name "Mon jeu" 2>/dev/null | head -n1)
	if [ -n "$WIN" ]; then
		wmctrl -i -r "$WIN" -b add,fullscreen
		break
	fi
done

wait $PID
