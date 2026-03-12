#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
source ./scripts/env.sh

# Evite d'executer un .class obsolet apres un git pull.
javac -cp ".:${MG2D_HOME}" projet/DungeonBlitz/*.java

java -cp "projet/DungeonBlitz:.:${MG2D_HOME}" DungeonBlitz
