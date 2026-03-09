#!/bin/bash

# Dossier du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/compilation.log"
WARN_FILE="$LOG_DIR/warnings_errors.log"

# Création du dossier log s'il n'existe pas
mkdir -p "$LOG_DIR"

# Vide les anciens logs
> "$LOG_FILE"
> "$WARN_FILE"


echo "===== Compilation du menu de la borne d'arcade =====" | tee -a "$LOG_FILE"
echo "Veuillez patienter" | tee -a "$LOG_FILE"

# Compiler le menu avec affichage des warnings de dépréciation
javac -Xlint:deprecation -cp .:$HOME *.java 2>&1 \
| tee -a "$LOG_FILE" \
| grep -E "warning|error|deprecated" >> "$WARN_FILE"

cd projet

# PENSER A REMETTRE COMPILATION JEUX!!!
for i in *
do
    cd "$i"
    # Vérifier s'il y a des fichiers .java dans le dossier
    if ls *.java 1> /dev/null 2>&1; then
        PROJECT_NAME="$i"

        echo "===== Compilation $PROJECT_NAME =====" | tee -a "$LOG_FILE"
        echo "Veuillez patienter" | tee -a "$LOG_FILE"
        javac -Xlint:deprecation -cp ".:../..:$HOME" *.java 2>&1 \
        | tee -a "$LOG_FILE" \
        | grep -E "warning|error|deprecated" \
        | sed "s/^/[$PROJECT_NAME] /" >> "$WARN_FILE"

    else
        echo "Pas de compilation nécessaire pour $i (projet Python ou autre)" | tee -a "$LOG_FILE"
    fi
    cd ..
done

cd ..

echo "Compilation terminée. Les logs sont dans $LOG_FILE"
