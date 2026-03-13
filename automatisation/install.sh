#!/bin/bash
set -e

# ==============================
# UTILITAIRES
# ==============================

print_section() {
    echo ""
    echo "=================================================="
    echo " $1"
    echo "=================================================="
}

detect_arch() {
    ARCH=$(dpkg --print-architecture)
    echo "Architecture détectée : $ARCH"
}

# ==============================
# JAVA
# ==============================

install_java() {
    print_section "VÉRIFICATION JAVA"

    if command -v java >/dev/null 2>&1; then
        CURRENT_JAVA=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
        echo "Java déjà installé : version $CURRENT_JAVA"
        # Si Maven ou OpenJFX absent, les installer car certains jeux Java en ont besoin
        if ! command -v mvn >/dev/null 2>&1 || ! dpkg -s openjfx >/dev/null 2>&1; then
            echo "Maven/OpenJFX manquant. Installation des paquets..."
            sudo apt update || true
            sudo apt install -y maven openjfx || true
            if command -v mvn >/dev/null 2>&1; then
                echo "Maven installé : $(mvn -v | head -n1)"
            else
                echo "Échec de l'installation de Maven (ignorer si non nécessaire)"
            fi
            if dpkg -s openjfx >/dev/null 2>&1; then
                echo "OpenJFX installé"
            else
                echo "Échec de l'installation d'OpenJFX (ignorer si non nécessaire)"
            fi
        fi
    else
        echo "Java non trouvé. Installation..."
        sudo apt update
        sudo dpkg --configure -a
        # Nettoyage du cache temporaire avant installation pour éviter les problèmes d'espace
        sudo rm -rf /tmp/* || true
        # Installer OpenJDK 17, Maven et OpenJFX (nécessaire pour certains jeux Java)
        sudo apt install -y openjdk-17-jdk maven openjfx
        echo "Java installé : $(java -version 2>&1 | awk -F '"' '/version/ {print $2}')"
        if command -v mvn >/dev/null 2>&1; then
            echo "Maven installé : $(mvn -v | head -n1)"
        fi
    fi
}

# ==============================
# PYTHON
# ==============================

get_target_python_version() {
    if [ "$ARCH" = "i386" ] || [ "$ARCH" = "armhf" ]; then
        LATEST_PYTHON="3.11.11"
    else
        LATEST_PYTHON="3.13.1"
    fi
}

check_python() {
    print_section "VÉRIFICATION PYTHON"

    get_target_python_version
    echo "Version cible : $LATEST_PYTHON"

    if command -v python3.12 >/dev/null 2>&1; then
        CURRENT_PYTHON=$(python3.12 --version 2>&1 | awk '{print $2}')
        echo "Python3.12 déjà installé : $CURRENT_PYTHON"
        COMPILE_PYTHON=false
    elif command -v python3 >/dev/null 2>&1; then
        CURRENT_PYTHON=$(python3 --version | awk '{print $2}')
        echo "Python3 installé (autre version) : $CURRENT_PYTHON"
        COMPILE_PYTHON=true
    else
        echo "Aucun Python3 détecté"
        COMPILE_PYTHON=true
    fi
}

install_python() {
    if [ "${COMPILE_PYTHON:-false}" != true ]; then
        return
    fi

    print_section "INSTALLATION PYTHON 3.12"

    if command -v python3.12 >/dev/null 2>&1; then
        echo "python3.12 déjà présent"
        return
    fi

    echo "Tentative d'installation via apt..."
    sudo apt update || true
    if sudo apt install -y python3.12 python3.12-venv python3.12-dev 2>/dev/null; then
        echo "python3.12 installé via APT"
        if command -v python3.12 >/dev/null 2>&1; then
            PY_BIN=python3.12
            $PY_BIN -m ensurepip --upgrade 2>/dev/null || sudo $PY_BIN -m ensurepip --upgrade || true
            $PY_BIN -m pip install --upgrade pip setuptools wheel || sudo $PY_BIN -m pip install --upgrade pip setuptools wheel || true
            echo "pip configuré pour $PY_BIN"
            # Vérifier que le module encodings est présent (évite 'No module named encodings')
            if ! $PY_BIN -c "import encodings" >/dev/null 2>&1; then
                echo "Erreur: module 'encodings' introuvable pour $PY_BIN" >&2
                echo "--- Diagnostic python ---" >&2
                $PY_BIN -v -c "import sys; print('PREFIX', sys.prefix); print('EXEPREFIX', sys.exec_prefix); print('PATHS', sys.path)" 2>&1 || true
                echo "--- Contenu de /usr/local/lib/python3.12 (si présent) ---" >&2
                ls -la /usr/local/lib/python3.12 2>/dev/null || true
                echo "Vérifiez que l'installation a correctement installé la librairie standard." >&2
                exit 1
            fi
        fi
        return
    fi

    echo "Paquet python3.12 indisponible dans les dépôts — compilation depuis les sources"

    echo "Installation des dépendances nécessaires pour compiler Python"
    sudo apt install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev tk-dev curl git || true

    PY_SRC_VER=3.12.2
    TMP_DIR="$HOME/python_build_$PY_SRC_VER"
    rm -rf "$TMP_DIR" && mkdir -p "$TMP_DIR"
    cd "$TMP_DIR" || exit 1

    PY_TARBALL_URL="https://www.python.org/ftp/python/$PY_SRC_VER/Python-$PY_SRC_VER.tgz"
    echo "Téléchargement $PY_TARBALL_URL"
    if ! curl -fsSL -o "Python-$PY_SRC_VER.tgz" "$PY_TARBALL_URL"; then
        echo "Impossible de télécharger Python $PY_SRC_VER"
        exit 1
    fi

    tar xf "Python-$PY_SRC_VER.tgz"
    cd "Python-$PY_SRC_VER" || exit 1

    echo "Configuration et compilation (peut prendre long)"

    ./configure --enable-optimizations --with-ensurepip=install --prefix=/usr/local || true
    make -j$(nproc) || make -j1 || true
    sudo make altinstall || { echo "make altinstall a échoué"; exit 1; }
    sudo ldconfig || true

    # vérifier et créer lien
    if [ -x "/usr/local/bin/python3.12" ]; then
        sudo ln -sf /usr/local/bin/python3.12 /usr/bin/python3.12 || true
        echo "python3.12 installé depuis les sources"
    fi

    # cleanup
    cd /home || true
    sudo rm -rf "$TMP_DIR"

    if command -v python3.12 >/dev/null 2>&1; then
        sudo rm -rf "$HOME/python_build_"* || true
        sudo rm -rf /usr/local/lib/python3.12 || true
        sudo rm -f /usr/local/bin/python3.12 || true
        echo "python3.12 disponible"
        PY_BIN=python3.12
        $PY_BIN -m ensurepip --upgrade 2>/dev/null || sudo $PY_BIN -m ensurepip --upgrade || true
        $PY_BIN -m pip install --upgrade pip setuptools wheel || sudo $PY_BIN -m pip install --upgrade pip setuptools wheel || true
        echo "pip configuré pour $PY_BIN"
            # Vérifier que le module encodings est présent (évite 'No module named encodings')
            if ! $PY_BIN -c "import encodings" >/dev/null 2>&1; then
                echo "Erreur: module 'encodings' introuvable pour $PY_BIN" >&2
                echo "--- Diagnostic python ---" >&2
                $PY_BIN -v -c "import sys; print('PREFIX', sys.prefix); print('EXEPREFIX', sys.exec_prefix); print('PATHS', sys.path)" 2>&1 || true
                echo "--- Contenu de /usr/local/lib/python3.12 (si présent) ---" >&2
                ls -la /usr/local/lib/python3.12 2>/dev/null || true
                echo "Vérifiez que l'installation a correctement installé la librairie standard." >&2
                exit 1
            fi
    else
        echo "Échec final: python3.12 non installé"
        exit 1
    fi
}

# ==============================
# PYGAME
# ==============================

check_pygame() {
    print_section "VÉRIFICATION PYGAME"

    # Preferer python3.12 si disponible, sinon fallback to python3
    if command -v python3.12 >/dev/null 2>&1; then
        PYTHON_BIN=python3.12
    elif command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN=python3
    else
        echo "Aucun interpréteur Python disponible pour vérifier Pygame"
        INSTALL_PYGAME=true
        return
    fi

    if $PYTHON_BIN -c "import pygame" >/dev/null 2>&1; then
        PYGAME_VERSION=$($PYTHON_BIN -c "import pygame; print(pygame.__version__)")
        echo "Pygame déjà installé (avec $PYTHON_BIN version $PYGAME_VERSION)"
        INSTALL_PYGAME=false
    else
        INSTALL_PYGAME=true
        echo "Pygame non détecté pour $PYTHON_BIN"
    fi
}

install_pygame() {
    if [ "${INSTALL_PYGAME:-false}" != true ]; then
        return
    fi

    print_section "INSTALLATION PYGAME"

    echo "Installation de Pygame pour Python 3.12 (ou python3 si non disponible)..."

    if command -v python3.12 >/dev/null 2>&1; then
        PYTHON_BIN=python3.12
    elif command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN=python3
    else
        echo "Aucun python disponible pour installer pygame" >&2
        exit 1
    fi

    echo "Installation des dépendances système requises pour pygame..."
    sudo apt update || true
    # Nettoyage du cache temporaire avant installation des dépendances Pygame
    sudo rm -rf /tmp/* || true
    sudo apt install -y --no-install-recommends \
        libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
        libportmidi-dev libfreetype6-dev libavformat-dev libswscale-dev \
        libjpeg-dev libpng-dev libasound2-dev libpulse-dev pkg-config || true

    echo "Mise à jour/installation de pip pour $PYTHON_BIN"
    $PYTHON_BIN -m ensurepip --upgrade 2>/dev/null || true
    $PYTHON_BIN -m pip install --upgrade pip setuptools wheel || true

    echo "Installation de pygame via pip ($PYTHON_BIN -m pip install pygame)"
    $PYTHON_BIN -m pip install pygame || {
        echo "Tentative d'installation via compilation wheel échouée, réessayez manuellement" >&2
        exit 1
    }

    if $PYTHON_BIN -c "import pygame" >/dev/null 2>&1; then
        echo "Pygame installé avec succès pour $PYTHON_BIN"
    else
        echo "Erreur lors de l'installation de Pygame pour $PYTHON_BIN" >&2
        exit 1
    fi
}

# ==============================
# LUA
# ==============================

install_lua() {
    print_section "VÉRIFICATION LUA"

    if command -v lua >/dev/null 2>&1; then
        echo "Lua installé : $(lua -v 2>&1 | awk '{print $2}')"
    else
        sudo apt update
        # Nettoyage avant installation de Lua
        sudo rm -rf /tmp/* || true
        sudo apt install -y lua5.4
        echo "Lua installé : $(lua -v 2>&1 | awk '{print $2}')"
    fi
}

# ==============================
# LOVE2D
# ==============================

install_love() {
    print_section "VÉRIFICATION LOVE2D"

    if command -v love >/dev/null 2>&1; then
        echo "Love2D installé : $(love --version 2>&1 | head -n 1)"
    else
        echo "Love2D non trouvé. Installation..."
        sudo apt update
        # Nettoyage avant installation de Love2D
        sudo rm -rf /tmp/* || true
        sudo apt install -y love
        echo "Love2D installé : $(love --version 2>&1 | head -n 1)"
    fi
}

# ==============================
# MG2D
# ==============================

install_mg2d() {
    print_section "INSTALLATION MG2D"

    REPO_URL="https://github.com/synave/MG2D.git"
    TARGET_DIR="$HOME/MG2D"
    TEMP_DIR="/tmp/MG2D_install"

    if [ -d "$TARGET_DIR" ]; then
        echo "MG2D déjà présent."
        return
    fi

    if ! command -v git >/dev/null 2>&1; then
        # Nettoyage avant installation de git
        sudo rm -rf /tmp/* || true
        sudo apt install -y git
    fi

    git clone "$REPO_URL" "$TEMP_DIR"
    mv "$TEMP_DIR/MG2D" "$TARGET_DIR"
    rm -rf "$TEMP_DIR"

    echo "MG2D installé."
}


# ==============================
# MAIN
# ==============================

main() {
    print_section "VÉRIFICATION DES DÉPENDANCES"

    # Nettoyage cache temporaire pour libérer de l'espace avant l'installation
    sudo rm -rf /tmp/* || true

    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

    detect_arch
    install_java
    check_python
    install_python
    check_pygame
    install_pygame
    install_lua
    install_love
    install_mg2d

    print_summary

    # === 0. Installer le layout clavier de la borne ===
    print_section "Setup des touches de la borne"
    if [ ! -f "$SCRIPT_DIR/scripts/verify_layout.sh" ] || [ ! -f "$SCRIPT_DIR/scripts/install_layout.sh" ]; then
        echo "Erreur: scripts layout manquants dans $SCRIPT_DIR/scripts" >&2
        exit 1
    fi

    bash "$SCRIPT_DIR/scripts/verify_layout.sh"
    bash "$SCRIPT_DIR/scripts/install_layout.sh"

    # === 0.5. Setup lancement automatique
    print_section "Setup du lancement automatique"
    mkdir -p $HOME/.config/autostart
    sudo cp $SCRIPT_DIR/../borne_arcade/borne.desktop $HOME/.config/autostart

    chmod +x ./automatisation/hooks/setup-hooks.sh
    ./automatisation/hooks/setup-hooks.sh

    # === 1. Lancer la borne ===
    chmod +x "$SCRIPT_DIR/../borne_arcade/lancerBorne.sh"
    cd "$SCRIPT_DIR/../borne_arcade" || exit 1
    bash lancerBorne.sh

    # === 2. Revenir dans borne ===
    cd "$SCRIPT_DIR/.." || exit 1

    # === 3. Lancer la vérification Python ===
    python3 "$SCRIPT_DIR/scripts/manager.py" --force

    # === 4. Nettoyage du cache temporaire ===
    sudo rm -rf /tmp/*

}

print_summary() {
    print_section "SCRIPT TERMINÉ"
    echo "Java    : $(java -version 2>&1 | awk -F '"' '/version/ {print $2}')"
    if command -v python3.12 >/dev/null 2>&1; then
        echo "Python3.12 : $(python3.12 --version 2>&1 | awk '{print $2}')"
    else
        echo "Python3.12 : non installé"
    fi
    echo "Python3  : $(python3 --version 2>/dev/null || echo 'non installé')"
    if command -v mvn >/dev/null 2>&1; then
        echo "Maven   : $(mvn -v | head -n1)"
    else
        echo "Maven   : non installé"
    fi
    if dpkg -s openjfx >/dev/null 2>&1; then
        echo "OpenJFX : installé"
    else
        echo "OpenJFX : non installé"
    fi
    echo "Lua     : $(lua -v 2>&1 | awk '{print $2}')"
    if command -v love >/dev/null 2>&1; then
        echo "Love2D  : $(love --version 2>&1 | head -n 1)"
    else
        echo "Love2D  : non installé"
    fi
}

main
