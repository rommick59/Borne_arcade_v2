#!/bin/bash
set -euo pipefail

# Resolve script directory and enter the game folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"/projet/DungeonBlitz || { echo "projet/DungeonBlitz not found"; exit 1; }

touch highscore

# move mouse if available
if command -v xdotool >/dev/null 2>&1; then
	xdotool mousemove 1280 1024 || true
else
	echo "xdotool not found — continuing without moving the mouse"
fi

# Compile Java sources in this folder if the class file is missing or out of date
if ls *.java >/dev/null 2>&1; then
	# compile if no class or any java is newer than class
	if [ ! -f DungeonBlitz.class ] || [ "$(find . -maxdepth 1 -name '*.java' -newer DungeonBlitz.class | wc -l)" -gt 0 ]; then
		echo "Compiling DungeonBlitz sources..."
		javac -cp .:../..:$HOME *.java || { echo "Java compilation failed"; exit 1; }
	fi
else
	echo "No .java files found in $(pwd) to compile"
fi

# Launch the game once
java -cp .:../..:$HOME DungeonBlitz
