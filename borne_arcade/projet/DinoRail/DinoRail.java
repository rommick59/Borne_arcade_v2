
import MG2D.FenetrePleinEcran;
import MG2D.Couleur;
import MG2D.geometrie.Point;
import MG2D.geometrie.Rectangle;
import MG2D.geometrie.Texte;
import java.awt.Font;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;

public class DinoRail {

    // Attributs //
    final static int largeur = 1275;
    final static int hauteur = 1020;
    private static final int FRAME_DELAY_MS = 20;
    private static final String HIGHSCORE_FILE = "./highscore";
    private static final int MAX_SCORES = 10;

    //static Fenetre f = new Fenetre("DinoRail", largeur, hauteur);
    static FenetrePleinEcran f = new FenetrePleinEcran("fen");

    private static ClavierBorneArcade clavier;
    private static final Font calibri = new Font("Calibri", Font.TYPE1_FONT, 40);
    private static Texte gameover = new Texte(
            Couleur.ROUGE,
            "",
            calibri,
            f.getMilieu()
    );
    private static Texte stats = new Texte(
            Couleur.NOIR,
            "",
            calibri,
            new Point(f.getMilieu().getX(), f.getMilieu().getY() + 50)
    );

    private static boolean gameFinished = false;

    private enum MenuChoice {
        PLAY, QUIT
    }

    private static class ScoreEntry {
        private final String name;
        private final int score;

        ScoreEntry(String name, int score) {
            this.name = name;
            this.score = score;
        }
    }

    public static void main(String[] args) {
        f.setVisible(true);
        clavier = new ClavierBorneArcade();
        f.addKeyListener(clavier);
        f.getP().addKeyListener(clavier);

        f.ajouter(gameover);
        f.ajouter(stats);

        while (true) {
            MenuChoice choice = showMenu();
            if (choice == MenuChoice.QUIT) {
                System.exit(0);
            }

            int score = runGame();
            boolean newHigh = updateHighscores(score);
            showGameOver(score, newHigh);
        }
    }

    private static MenuChoice showMenu() {
        int selectedIndex = 0;
        int best = getBestScore();

        Texte title = new Texte(Couleur.NOIR, "DinoRail", calibri, new Point(f.getMilieu().getX(), f.getMilieu().getY() + 200));
        Texte play = new Texte(Couleur.VERT, "> Jouer", calibri, new Point(f.getMilieu().getX(), f.getMilieu().getY() + 50));
        Texte quit = new Texte(Couleur.NOIR, "  Quitter", calibri, new Point(f.getMilieu().getX(), f.getMilieu().getY() - 30));
        Texte bestScore = new Texte(Couleur.NOIR, "Highscore : " + best, calibri, new Point(f.getMilieu().getX(), f.getMilieu().getY() + 120));
        Texte hint = new Texte(Couleur.NOIR, "F pour valider", calibri, new Point(f.getMilieu().getX(), f.getMilieu().getY() - 150));

        f.ajouter(title);
        f.ajouter(play);
        f.ajouter(quit);
        f.ajouter(bestScore);
        f.ajouter(hint);

        while (true) {
            if (clavier.getJoyJ1HautTape()) {
                selectedIndex = 0;
            }
            if (clavier.getJoyJ1BasTape()) {
                selectedIndex = 1;
            }

            play.setTexte((selectedIndex == 0 ? "> " : "  ") + "Jouer");
            quit.setTexte((selectedIndex == 1 ? "> " : "  ") + "Quitter");
            play.setCouleur(selectedIndex == 0 ? Couleur.VERT : Couleur.NOIR);
            quit.setCouleur(selectedIndex == 1 ? Couleur.VERT : Couleur.NOIR);

            f.rafraichir();
            if (clavier.getBoutonJ1ATape()) {
                break;
            }
            sleepQuietly(FRAME_DELAY_MS);
        }

        f.supprimer(title);
        f.supprimer(play);
        f.supprimer(quit);
        f.supprimer(bestScore);
        f.supprimer(hint);
        f.rafraichir();
        clavier.reinitialisation();

        return selectedIndex == 0 ? MenuChoice.PLAY : MenuChoice.QUIT;
    }

    private static int runGame() {
        gameFinished = false;
        int score = 0;

        long lastObstacleTime = System.currentTimeMillis();
        int minDelayObstacle = 850;
        long now;

        Rectangle sol = new Rectangle(Couleur.NOIR, new Point(0, 0), new Point(largeur, 150));
        sol.setPlein(true);
        Rectangle player = new Rectangle(Couleur.VERT, new Point(100, 150), new Point(200, 300));
        player.setPlein(true);

        boolean hasJump = false;
        boolean isAscended = false;
        int limitHeight = 550;

        ArrayList<Obstacle> listObstacle = new ArrayList<>();
        Iterator<Obstacle> it;

        listObstacle.add(new Obstacle(new Point(largeur, 150), new Point(largeur + 40, 200), "./assets/img/cactus.png"));

        f.ajouter(listObstacle.get(0));
        f.ajouter(sol);
        f.ajouter(player);

        int bestScore = getBestScore();
        gameover.setTexte("");
        stats.setTexte("Score : 0 | High : " + bestScore);

        while (!gameFinished) {

            now = System.currentTimeMillis();

            if (now - lastObstacleTime >= minDelayObstacle + Math.random() * (3500 - minDelayObstacle)) {
                if (Math.random() > 0.3) {
                    listObstacle.add(new Obstacle(new Point(largeur, 150), new Point(largeur + 40, 200), "./assets/img/cactus.png"));
                } else {
                    listObstacle.add(new Obstacle(new Point(largeur, 250), new Point(largeur + 40, 300), "./assets/img/bird.png"));
                }

                f.ajouter(listObstacle.get(listObstacle.size() - 1));
                lastObstacleTime = now;
            }

            if (clavier.getJoyJ1HautEnfoncee() && !hasJump) {
                hasJump = true;
                isAscended = true;
            }

            if (clavier.getJoyJ1BasEnfoncee() && !hasJump) {
                player.setTaille(100, 70);
            } else {
                player.setTaille(100, 150);
            }

            if (hasJump) {
                if (isAscended && player.getB().getY() < limitHeight) {
                    player.translater(0, 15);
                } else {
                    isAscended = false;
                    if (player.getA().getY() > sol.getB().getY()) {
                        player.translater(0, -15);
                    } else {
                        hasJump = false;
                    }
                }
            }

            it = listObstacle.iterator();
            while (it.hasNext()) {
                Obstacle obstacle = it.next();

                if (obstacle.intersectionRapide(player)) {
                    gameFinished = true;
                }

                if (obstacle.isOffScreen()) {
                    f.supprimer(obstacle);
                    it.remove();
                } else {
                    obstacle.translater(-10, 0);
                }
            }
            score += 1;
            int displayedBest = Math.max(bestScore, score);
            stats.setTexte("Score : " + score + " | High : " + displayedBest);
            f.rafraichir();
            sleepQuietly(FRAME_DELAY_MS);
        }

        for (Obstacle obstacle : listObstacle) {
            f.supprimer(obstacle);
        }
        f.supprimer(sol);
        f.supprimer(player);
        stats.setTexte("");
        f.rafraichir();
        clavier.reinitialisation();
        return score;
    }

    private static void showGameOver(int score, boolean newHigh) {
        gameover.setCouleur(newHigh ? Couleur.VERT : Couleur.ROUGE);
        gameover.setTexte(newHigh ? "Nouveau highscore : " + score : "Game over ! Score : " + score);
        stats.setTexte("F pour retourner au menu");
        f.rafraichir();

        while (!clavier.getBoutonJ1ATape()) {
            sleepQuietly(50);
        }

        gameover.setTexte("");
        stats.setTexte("");
        f.rafraichir();
        clavier.reinitialisation();
    }

    private static boolean updateHighscores(int newScore) {
        List<ScoreEntry> scores = loadHighscores();
        int bestBefore = scores.isEmpty() ? -1 : scores.get(0).score;
        int threshold = scores.isEmpty() ? -1 : scores.get(Math.min(scores.size() - 1, MAX_SCORES - 1)).score;
        boolean qualifies = scores.size() < MAX_SCORES || newScore >= threshold;
        if (!qualifies) {
            return false;
        }

        HighScore.demanderEnregistrerNom(f, clavier, null, newScore, HIGHSCORE_FILE);
        clavier.reinitialisation();
        return newScore >= bestBefore;
    }

    private static int getBestScore() {
        List<ScoreEntry> scores = loadHighscores();
        if (scores.isEmpty()) {
            return 0;
        }
        return scores.get(0).score;
    }

    private static List<ScoreEntry> loadHighscores() {
        List<ScoreEntry> scores = new ArrayList<>();
        File file = new File(HIGHSCORE_FILE);
        if (!file.exists()) {
            return scores;
        }

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) {
                    continue;
                }
                String[] parts = line.split("-");
                if (parts.length != 2) {
                    continue;
                }
                try {
                    String name = parts[0].trim();
                    int score = Integer.parseInt(parts[1].trim());
                    scores.add(new ScoreEntry(name, score));
                } catch (NumberFormatException ignored) {
                    // Ignore malformed score lines.
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        scores.sort(Comparator.comparingInt((ScoreEntry s) -> s.score).reversed());
        if (scores.size() > MAX_SCORES) {
            return new ArrayList<>(scores.subList(0, MAX_SCORES));
        }
        return scores;
    }

    private static void sleepQuietly(int millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
