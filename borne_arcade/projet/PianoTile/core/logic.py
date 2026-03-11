import pygame
from core.player import Player
from ui.layout.gameView import GameView
from ui.layout.timerView import TimerView
from ui.utils.color import Color
from core.pageState import PageState
from core.button import Button

class Logic:
    def __init__(self, game) -> None:
        """Initialisation de l'interface."""
        self.__game = game
        self.__interface = game.getInterface()
        self.__color: Color = Color()
        self.__button: Button = Button()

    def getGame(self):
        """Game du jeu."""
        return self.__game
    
    def getColor(self):
        """Getter de la color."""
        return self.__color
    
    def getInterface(self):
        """Getter de l'interface."""
        return self.__interface
    
    def getButton(self):
        """Getter du bouton."""
        return self.__button
    
    def actionPageProfil(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:    
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Se connecter"):
                        self.getInterface().setPage(PageState.CONNEXION)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "S'inscrire"):
                        self.getInterface().setPage(PageState.INSCRIPTION)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        # Reste sur le bouton bas pour retoggle rapidement
                        selection = self.getInterface().getWindowManager().getSelection()
                        if selection and selection.getSelection():
                            selection_dict = selection.getSelection()[1]
                            bottom_y = max(pos[1] for pos in selection_dict.keys()) if selection_dict else 0
                            selection.setPosition((1, bottom_y))
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Solo"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        selection = self.getInterface().getWindowManager().getSelection()
                        if selection and selection.getSelection():
                            selection_dict = selection.getSelection()[1]
                            bottom_y = max(pos[1] for pos in selection_dict.keys()) if selection_dict else 0
                            selection.setPosition((1, bottom_y))
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):            
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageInscription(self):
        # ✅ Ne continue que si la page courante est bien CONNEXION
        if self.getInterface().getPage() != PageState.INSCRIPTION:
            return

        # ✅ Récupère la page Connexion
        page = self.getInterface().getWindowManager().getMenu().getPage()
        if page is None:
            return  # Sécurité : évite crash si getPage() retourne None

        self.getInterface().setUpdate(False)

        for event in pygame.event.get():
            # Toujours transmettre les événements à la page
            page.handle_event(event)

            username_active = page.input_username.active
            password_active = page.input_password.active
            password_confirm_active = page.input_confirmPassword.active

            # ✅ Si un champ est actif, gérer les touches
            if username_active or password_active or password_confirm_active:
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # ⬅️➡️⬆️⬇️ désactivent la saisie
                    page.input_username.active = False
                    page.input_password.active = False
                    page.input_confirmPassword.active = False
                    page.input_username.color = page.input_username.color_inactive
                    page.input_password.color = page.input_password.color_inactive
                    page.input_confirmPassword.color = page.input_confirmPassword.color_inactive

                self.getInterface().setUpdate(True)
                continue  # ⛔ Ignore le reste (navigation)

            # 🎮 Navigation clavier
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    selection = self.getInterface().getWindowManager().getSelection()
                    current_item = selection.getSelection()[1][selection.getPosition()][0]

                    if current_item == "Retour":
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())

                    elif current_item == "Valider":
                        username = page.input_username.get_text()
                        password = page.input_password.get_text()
                        confirmPassword = page.input_confirmPassword.get_text()

                        db = self.getInterface().getGame().getDatabase()
                        users = db.getPlayers()

                        matched_user = next(
                            (u for u in users if u[1] == username and u[2] == password), None
                        )

                        if matched_user and confirmPassword == password:
                            page.erreur_inscription = False

                            player_id, name, password = matched_user
                            player_obj = Player(player_id, name, password)

                            self.getInterface().getWindowManager().setCurrentUser(player_obj)
                            self.getInterface().setPage(PageState.ACCUEIL)
                        else:
                            page.erreur_inscription = True

                        self.getInterface().setUpdate(True)

                    elif current_item == "Profil":
                        self.getInterface().setPage(PageState.PROFIL)
                    elif current_item == "Accueil":
                        self.getInterface().setPage(PageState.ACCUEIL)
                    elif current_item == "Nom d'utilisateur":
                        page.input_username.active = True
                        page.input_password.active = False
                        page.input_confirmPassword.active = False
                        page.input_username.color = page.input_username.color_active
                        page.input_password.color = page.input_password.color_inactive
                        page.input_confirmPassword.color = page.input_password.color_inactive
                    elif current_item == "Mot de passe":
                        page.input_password.active = True
                        page.input_username.active = False
                        page.input_confirmPassword.active = False
                        page.input_password.color = page.input_password.color_active
                        page.input_username.color = page.input_username.color_inactive
                        page.input_confirmPassword.color = page.input_confirmPassword.color_inactive
                    elif current_item == "Confirmer le mot de passe":
                        page.input_confirmPassword.active = True
                        page.input_password.active = False
                        page.input_username.active = False
                        page.input_confirmPassword.color = page.input_confirmPassword.color_active
                        page.input_password.color = page.input_password.color_inactive
                        page.input_username.color = page.input_username.color_inactive
                    elif current_item == "Multijoueur":
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                    elif current_item == "Statistique":
                        self.getInterface().setPage(PageState.STATISTIQUE)
                    elif current_item == "Quitter":
                        self.getInterface().setPage(PageState.QUITTER)

                    self.getInterface().setUpdate(True)

                elif isinstance(direction, tuple):
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageConnexion(self):
        # ✅ Ne continue que si la page courante est bien CONNEXION
        if self.getInterface().getPage() != PageState.CONNEXION:
            return

        # ✅ Récupère la page Connexion
        page = self.getInterface().getWindowManager().getMenu().getPage()
        if page is None:
            return  # Sécurité : évite crash si getPage() retourne None

        self.getInterface().setUpdate(False)

        for event in pygame.event.get():
            # Toujours transmettre les événements à la page
            page.handle_event(event)

            username_active = page.input_username.active
            password_active = page.input_password.active

            # ✅ Si un champ est actif, gérer les touches
            if username_active or password_active:
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # ⬅️➡️⬆️⬇️ désactivent la saisie
                    page.input_username.active = False
                    page.input_password.active = False
                    page.input_username.color = page.input_username.color_inactive
                    page.input_password.color = page.input_password.color_inactive

                self.getInterface().setUpdate(True)
                continue  # ⛔ Ignore le reste (navigation)

            # 🎮 Navigation clavier
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    selection = self.getInterface().getWindowManager().getSelection()
                    current_item = selection.getSelection()[1][selection.getPosition()][0]

                    if current_item == "Retour":
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())

                    elif current_item == "Valider":
                        username = page.input_username.get_text()
                        password = page.input_password.get_text()

                        db = self.getInterface().getGame().getDatabase()
                        users = db.getPlayers()

                        matched_user = next(
                            (u for u in users if u[1] == username and u[2] == password), None
                        )

                        if matched_user:
                            page.erreur_connexion = False

                            player_id, name, password = matched_user
                            player_obj = Player(player_id, name, password)

                            self.getInterface().getWindowManager().setCurrentUser(player_obj)
                            self.getInterface().setPage(PageState.ACCUEIL)
                        else:
                            page.erreur_connexion = True

                        self.getInterface().setUpdate(True)

                    elif current_item == "Profil":
                        self.getInterface().setPage(PageState.PROFIL)
                    elif current_item == "Accueil":
                        self.getInterface().setPage(PageState.ACCUEIL)
                    elif current_item == "Nom d'utilisateur":
                        page.input_username.active = True
                        page.input_password.active = False
                        page.input_username.color = page.input_username.color_active
                        page.input_password.color = page.input_password.color_inactive
                    elif current_item == "Mot de passe":
                        page.input_password.active = True
                        page.input_username.active = False
                        page.input_password.color = page.input_password.color_active
                        page.input_username.color = page.input_username.color_inactive
                    elif current_item == "Multijoueur":
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                    elif current_item == "Statistique":
                        self.getInterface().setPage(PageState.STATISTIQUE)
                    elif current_item == "Quitter":
                        self.getInterface().setPage(PageState.QUITTER)

                    self.getInterface().setUpdate(True)

                elif isinstance(direction, tuple):
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageFiltrer(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif "Difficulte " in self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0]:
                        self.getInterface().getWindowManager().getSorted().changeFilter(self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0])
                        self.getInterface().setUpdate(True)
                    elif "Annee " in self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0]:
                        self.getInterface().getWindowManager().setMusicSelect(self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0].replace("Detail musique ", ""))
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        # Basculer immédiatement en mode multi pour refléter le label/typo
                        self.getInterface().getWindowManager().setMultiplayer(True)
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):            
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageAide(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().getWindowManager().setMultiplayer(True)
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)                
                elif isinstance(direction, tuple):            
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
    def actionPageDetail(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):         
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPagePlay(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction == "enter":
                selection = self.getInterface().getWindowManager().getSelection()
                item = selection.getSelection()[1][selection.getPosition()][0]
                if item == "Retour":
                    self.getInterface().setPage(self.getInterface().getPagePrecedente())
                    self.getInterface().setUpdate(True)
                elif item == "Profil":
                    self.getInterface().setPage(PageState.PROFIL)
                    self.getInterface().setUpdate(True)
                elif item == "Accueil":
                    self.getInterface().setPage(PageState.ACCUEIL)
                    self.getInterface().setUpdate(True)
                elif item == "Multijoueur":
                    self.getInterface().setPage(PageState.MULTIJOUEUR)
                    self.getInterface().setUpdate(True)
                elif item == "Statistique":
                    self.getInterface().setPage(PageState.STATISTIQUE)
                    self.getInterface().setUpdate(True)
                elif item == "Quitter":
                    self.getInterface().setPage(PageState.QUITTER)
                    self.getInterface().setUpdate(True)
                elif item == "Play":
                    timer = TimerView(self.getInterface().getWindowManager())
                    timer.start()
                    clock = pygame.time.Clock()
                    running = True
                    game_started = False

                    wm = self.getInterface().getWindowManager()

                    if wm.isMultiplayer():
                        # Split-screen : deux GameView côte à côte
                        half_width = wm.getScreenWidth() // 2
                        game_left = GameView(wm, offset_x=0, area_width=half_width)
                        game_right = GameView(wm, offset_x=half_width, area_width=half_width)

                        # On conserve le GameView principal (gauche) pour la compatibilité éventuelle
                        wm.setGame(game_left)

                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                if event.type == pygame.KEYDOWN:
                                    # Joueur 1 (gauche)
                                    if event.key in (pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_f, pygame.K_g):
                                        col = {pygame.K_r: 0, pygame.K_t: 1, pygame.K_y: 2, pygame.K_f: 3, pygame.K_g: 4}.get(event.key)
                                        game_left.checkHit(col)
                                    # Joueur 2 (droite)
                                    if event.key in (pygame.K_a, pygame.K_z, pygame.K_e, pygame.K_q, pygame.K_s):
                                        col = {pygame.K_a: 0, pygame.K_z: 1, pygame.K_e: 2, pygame.K_q: 3, pygame.K_s: 4}.get(event.key)
                                        game_right.checkHit(col)

                            wm.getWindow().fill((30, 30, 30))

                            if not game_started:
                                timer.draw()
                                if timer.getFinished():
                                    game_left.getPiano().play()  # une seule lecture pour les deux
                                    game_started = True
                                    self.getInterface().setUpdate(True)
                            else:
                                game_left.update()
                                game_right.update()
                                game_left.affichagePiano()
                                game_right.affichagePiano()
                                self.getInterface().setUpdate(True)

                                if game_left.isGameOver() or game_right.isGameOver():
                                    pygame.mixer.music.stop()
                                    running = False
                                    self.getInterface().setUpdate(True)

                            pygame.display.flip()
                            # Baisser la fréquence d'images pour réduire la charge CPU/RAM
                            clock.tick(30)

                    else:
                        # Mode solo inchangé
                        new_game_view = GameView(wm)
                        wm.setGame(new_game_view)

                        game_view = new_game_view
                        piano = game_view.getPiano()

                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                            keys = pygame.key.get_pressed()
                            # En mode solo, ne considérer que les touches du Joueur 1
                            J1_KEYS = (pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_f)
                            key_to_col = {
                                pygame.K_r: 0,
                                pygame.K_t: 1,
                                pygame.K_y: 2,
                                pygame.K_f: 3,
                            }
                            for key in J1_KEYS:
                                try:
                                    if keys[key]:
                                        col = key_to_col.get(key)
                                        if col is not None:
                                            game_view.checkHit(col)
                                except IndexError:
                                    # Defensive: get_pressed() may be smaller on some platforms
                                    continue

                            wm.getWindow().fill((30, 30, 30))

                            if not game_started:
                                timer.draw()
                                if timer.getFinished():
                                    piano.play()
                                    game_started = True
                                    self.getInterface().setUpdate(True)
                            else:
                                game_view.update()
                                game_view.affichagePiano()
                                self.getInterface().setUpdate(True)

                                if game_view.isGameOver():
                                    pygame.mixer.music.stop()
                                    running = False
                                    self.getInterface().setUpdate(True)

                            pygame.display.flip()
                            # Baisser la fréquence d'images pour réduire la charge CPU/RAM
                            clock.tick(30)

            elif isinstance(direction, tuple):
                self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                self.getInterface().setUpdate(True)

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageAccueil(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Filtrer"):
                        self.getInterface().setPage(PageState.FILTRER)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Aide"):
                        self.getInterface().setPage(PageState.AIDE)
                        self.getInterface().setUpdate(True)
                    elif "Detail " in self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0]:
                        self.getInterface().getWindowManager().setMusicSelect(self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0].replace("Detail musique ", ""))
                        self.getInterface().setPage(PageState.DETAIL)
                        self.getInterface().setUpdate(True)
                    elif "Play " in self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0]:
                        self.getInterface().getWindowManager().setMusicSelect(self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0].replace("Play musique ", ""))
                        self.getInterface().getWindowManager().setMultiplayer(False)
                        self.getInterface().setPage(PageState.PLAY)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                
                elif isinstance(direction, tuple):            
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    def actionPageMultijoueur(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:    
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().getWindowManager().setMultiplayer(False)
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Solo"):
                        # Bascule vers solo depuis la page multi
                        self.getInterface().getWindowManager().setMultiplayer(False)
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().getWindowManager().setMultiplayer(True)
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                    elif "Play " in self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0]:
                        # Lancer en mode multi local (split screen)
                        self.getInterface().getWindowManager().setMusicSelect(self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0].replace("Play musique ", ""))
                        self.getInterface().getWindowManager().setMultiplayer(True)
                        self.getInterface().setPage(PageState.PLAY)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):  
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    def actionPageStatistique(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):  
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageQuitter(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:  
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Non"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Oui"):
                        self.getInterface().setPage(PageState.FERMER)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):  
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageFinGagne(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):  
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def actionPageFinPerdu(self):
        self.getInterface().setUpdate(False)
        for event in pygame.event.get():
            direction = self.getButton().update(event, navigation_mode=True)
            if direction:
                if direction == "enter":
                    if (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Retour"):
                        self.getInterface().setPage(self.getInterface().getPagePrecedente())
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Profil"):
                        self.getInterface().setPage(PageState.PROFIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Accueil"):
                        self.getInterface().setPage(PageState.ACCUEIL)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Multijoueur"):
                        self.getInterface().setPage(PageState.MULTIJOUEUR)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Statistique"):
                        self.getInterface().setPage(PageState.STATISTIQUE)
                        self.getInterface().setUpdate(True)
                    elif (self.getInterface().getWindowManager().getSelection().getSelection()[1][self.getInterface().getWindowManager().getSelection().getPosition()][0] == "Quitter"):
                        self.getInterface().setPage(PageState.QUITTER)
                        self.getInterface().setUpdate(True)
                elif isinstance(direction, tuple):  
                    self.getInterface().getWindowManager().getSelection().updatePosition(direction)
                    self.getInterface().setUpdate(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()