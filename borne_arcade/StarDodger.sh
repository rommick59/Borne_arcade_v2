#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/projet/StarDodger"

# Lancement du jeu
java -cp . Main
