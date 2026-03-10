# Binding des touches de la borne (Java, Python, Lua)

Ce guide explique comment détecter et binder les boutons physiques de la borne arcade
afin que les jeux (Java, Pygame, LÖVE/Lua) les reconnaissent de manière fiable.

Résumé rapide
- Navigation : flèches `left` / `right`
- Valider / Confirmer : `r`
- Retour / Annuler : `f`
- Pause : `t`

Avant de commencer
- Assurez-vous d'avoir accès au device d'entrée de la borne (généralement `/dev/input/eventX`).
- Installez `evtest` pour inspecter les événements bas‑niveau :

```bash
sudo apt update && sudo apt install evtest
evtest --list-devices
sudo evtest /dev/input/eventX  # remplacez eventX par le bon device
```

Appuyez sur chaque bouton et notez les lignes affichées (code, type d'événement). Cela permet de savoir
si la borne produit des keycodes standards, des scancodes ou des caractères.

1) Options de remapping (si les touches ne correspondent pas)
- xmodmap (temporaire, session X)

```bash
# exemple : keycode 94 -> 'r'
xmodmap -e "keycode 94 = r R"
# Pour persister dans une session X, mettez ces lignes dans ~/.Xmodmap
```

- setxkbmap / XKB (persistant sous X)
  - Créez ou modifiez un layout XKB et chargez-le avec `setxkbmap`. Le script `lancerBorne.sh` peut appeler
    `setxkbmap` : éditez le layout utilisé si nécessaire.

- Remapping au niveau kernel / udev (avancé)
  - Pour mappings persistants en dehors de X, on peut utiliser `udev` ou `hwdb` et `systemd-hwdb`.
    C'est plus complexe mais fonctionne avant l'init d'un serveur X.

2) Pattern recommandé côté application
- N'exposez pas directement les keycodes dans la logique du jeu. Créez une table de mapping "physique -> action".

Exemple général (pseudo) :

```text
mapping = {
  left = 'move_left',
  right = 'move_right',
  r = 'confirm',
  f = 'back',
  t = 'pause'
}

-- En runtime : lire l'event, convertir en key-string ou key-const, et appeler mapping[key]
```

3) Exemples concrets

Java (AWT/Swing)

```java
// Exemple minimal : centraliser les actions via une méthode handleAction(String action)
@Override
public void keyPressed(KeyEvent e) {
    int kc = e.getKeyCode();
    switch(kc) {
        case KeyEvent.VK_LEFT: handleAction("move_left"); break;
        case KeyEvent.VK_RIGHT: handleAction("move_right"); break;
        case KeyEvent.VK_R: handleAction("confirm"); break;
        case KeyEvent.VK_F: handleAction("back"); break;
        case KeyEvent.VK_T: handleAction("pause"); break;
    }
}

@Override
public void keyTyped(KeyEvent e) {
    // fallback si la borne envoie un caractère
    char c = e.getKeyChar();
    if (c == 'r') handleAction("confirm");
}
```

Python (Pygame)

```python
def handle_input(event):
    if event.type == pygame.KEYDOWN:
        # préférer event.key (constantes pygame.K_*)
        k = event.key
        if k == pygame.K_LEFT:
            move_left()
        elif k == pygame.K_RIGHT:
            move_right()
        elif k == pygame.K_r:
            confirm()
        elif k == pygame.K_f:
            back()
        elif k == pygame.K_t:
            pause()

# lecture hold
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]: move_left()
```

Lua (LÖVE)

```lua
function love.keypressed(key, scancode, isrepeat)
  if key == 'left' then move_left() end
  if key == 'right' then move_right() end
  if key == 'r' then confirm() end
  if key == 'f' then back() end
  if key == 't' then pause_game() end
end
```

4) Bonnes pratiques et robustesse
- Supportez plusieurs entrées pour la même action (ex : `left` ET `a` pour gauche).
- Fournissez un écran de calibration/test qui affiche les events reçus en temps réel.
- Documentez les bindings attendus dans le dossier du jeu (ex. `projet/<jeu>/bouton.txt`).

5) Fichiers et scripts utiles dans ce dépôt
- Script de lancement : [borne_arcade/lancerBorne.sh](borne_arcade/lancerBorne.sh)

Test rapide
- Exécutez `evtest` puis appuyez sur un bouton. Si l'event correspond à un keycode standard, mappez-le dans votre code.
- Si vous voyez uniquement scancodes ou des codes non standards, créez un mapping via `xmodmap`/XKB ou adaptez la table dans le jeu.

Besoin d'aide supplémentaire ?
- Je peux générer un `xmodmap` ou un fragment XKB si vous me fournissez la sortie d'`evtest` (ou du script de test).

---
Fichier édité : [borne_arcade/docs/BINDING_BORNE.md](borne_arcade/docs/BINDING_BORNE.md)
