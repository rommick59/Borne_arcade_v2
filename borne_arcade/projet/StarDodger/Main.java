import MG2D.*;
import MG2D.geometrie.*;

import java.awt.Color;
import java.awt.Font;
import java.io.File;
import java.util.ArrayList;
import java.util.Random;

public class Main {
    private static final int WIDTH = 1280;
    private static final int HEIGHT = 1024;

    private static final int PLAYER_SIZE = 60;
    private static final int BASE_SPEED = 6;
    private static final int BOOST_SPEED = 12;
    private static final int BOOST_FRAMES = 20;
    private static final int BOOST_COOLDOWN = 60;

    private final FenetrePleinEcran f;
    private final ClavierBorneArcade clavier;
    private final Random rng = new Random();

    private Rectangle player;
    private Rectangle limitLeft, limitRight, limitTop, limitBottom;

    private final ArrayList<Cercle> stars = new ArrayList<>();
    private final ArrayList<Integer> starSpeed = new ArrayList<>();
    private final ArrayList<Integer> starY = new ArrayList<>();

    private final ArrayList<Cercle> bombs = new ArrayList<>();
    private final ArrayList<Integer> bombSpeed = new ArrayList<>();
    private final ArrayList<Integer> bombY = new ArrayList<>();

    private final ArrayList<Cercle> shields = new ArrayList<>();
    private final ArrayList<Integer> shieldSpeed = new ArrayList<>();
    private final ArrayList<Integer> shieldY = new ArrayList<>();

    private int score = 0;
    private int level = 1;
    private boolean shieldActive = false;

    private boolean running = false;
    private boolean gameOver = false;
    private boolean scoreSaved = false;

    private long lastStar = 0;
    private long lastBomb = 0;
    private long lastShield = 0;

    private int boostTimer = 0;
    private int boostCooldown = 0;

    private Font hudFont;
    private Font titleFont;

    private Texte title;
    private Texte help;
    private Texte scoreText;
    private Texte levelText;
    private Texte shieldText;
    private Texte overText;
    private Texte restartText;

    public Main() {
        f = new FenetrePleinEcran("Star Dodger");
        f.setVisible(true);
        f.setBackground(Color.BLACK);

        clavier = new ClavierBorneArcade();
        f.addKeyListener(clavier);
        f.getP().addKeyListener(clavier);

        loadFonts();
        initHud();
        initPlayer();
        initBounds();
    }

    private void loadFonts() {
        try {
            File in = new File("../../fonts/PrStart.ttf");
            Font base = Font.createFont(Font.TRUETYPE_FONT, in);
            hudFont = base.deriveFont(24.0f);
            titleFont = base.deriveFont(48.0f);
        } catch (Exception e) {
            hudFont = new Font("Calibri", Font.TYPE1_FONT, 24);
            titleFont = new Font("Calibri", Font.BOLD, 48);
        }
    }

    private void initHud() {
        title = new Texte(Couleur.BLANC, "STAR DODGER", titleFont, new Point(640, 900));
        help = new Texte(Couleur.BLANC, "A: START / Z: QUIT", hudFont, new Point(640, 820));

        scoreText = new Texte(Couleur.BLANC, "SCORE: 0", hudFont, new Point(120, 960));
        levelText = new Texte(Couleur.BLANC, "LEVEL: 1", hudFont, new Point(120, 920));
        shieldText = new Texte(Couleur.BLANC, "SHIELD: OFF", hudFont, new Point(120, 880));

        overText = new Texte(Couleur.ROUGE, "GAME OVER", titleFont, new Point(640, 650));
        restartText = new Texte(Couleur.BLANC, "A: RESTART / Z: QUIT", hudFont, new Point(640, 580));

        f.ajouter(title);
        f.ajouter(help);
        f.ajouter(scoreText);
        f.ajouter(levelText);
        f.ajouter(shieldText);
    }

    private void initPlayer() {
        int x1 = (WIDTH - PLAYER_SIZE) / 2;
        int y1 = 120;
        player = new Rectangle(Couleur.BLEU, new Point(x1, y1), new Point(x1 + PLAYER_SIZE, y1 + PLAYER_SIZE), true);
        f.ajouter(player);
    }

    private void initBounds() {
        limitLeft = new Rectangle(Couleur.NOIR, new Point(0, 0), new Point(5, HEIGHT), false);
        limitRight = new Rectangle(Couleur.NOIR, new Point(WIDTH - 5, 0), new Point(WIDTH, HEIGHT), false);
        limitBottom = new Rectangle(Couleur.NOIR, new Point(0, 0), new Point(WIDTH, 5), false);
        limitTop = new Rectangle(Couleur.NOIR, new Point(0, HEIGHT - 5), new Point(WIDTH, HEIGHT), false);
    }

    private void resetGame() {
        clearEntities();
        score = 0;
        level = 1;
        shieldActive = false;
        running = true;
        gameOver = false;
        scoreSaved = false;
        boostTimer = 0;
        boostCooldown = 0;
        updateHud();
    }

    private void clearEntities() {
        for (Cercle c : stars) {
            f.supprimer(c);
        }
        for (Cercle c : bombs) {
            f.supprimer(c);
        }
        for (Cercle c : shields) {
            f.supprimer(c);
        }
        stars.clear();
        starSpeed.clear();
        starY.clear();
        bombs.clear();
        bombSpeed.clear();
        bombY.clear();
        shields.clear();
        shieldSpeed.clear();
        shieldY.clear();
    }

    private void updateHud() {
        scoreText.setTexte("SCORE: " + score);
        levelText.setTexte("LEVEL: " + level);
        shieldText.setTexte("SHIELD: " + (shieldActive ? "ON" : "OFF"));
    }

    private void spawnStar() {
        int x = 40 + rng.nextInt(WIDTH - 80);
        int y = HEIGHT + 30;
        int r = 14 + rng.nextInt(10);
        Cercle star = new Cercle(Couleur.JAUNE, new Point(x, y), r, true);
        stars.add(star);
        starSpeed.add(3 + level);
        starY.add(y);
        f.ajouter(star);
    }

    private void spawnBomb() {
        int x = 40 + rng.nextInt(WIDTH - 80);
        int y = HEIGHT + 30;
        int r = 16 + rng.nextInt(12);
        Cercle bomb = new Cercle(Couleur.ROUGE, new Point(x, y), r, true);
        bombs.add(bomb);
        bombSpeed.add(4 + level);
        bombY.add(y);
        f.ajouter(bomb);
    }

    private void spawnShield() {
        int x = 40 + rng.nextInt(WIDTH - 80);
        int y = HEIGHT + 30;
        int r = 18;
        Cercle shield = new Cercle(Couleur.VERT, new Point(x, y), r, true);
        shields.add(shield);
        shieldSpeed.add(3 + level);
        shieldY.add(y);
        f.ajouter(shield);
    }

    private void updateEntities() {
        for (int i = stars.size() - 1; i >= 0; i--) {
            Cercle c = stars.get(i);
            int newY = starY.get(i) - starSpeed.get(i);
            starY.set(i, newY);
            c.translater(0, -starSpeed.get(i));
            if (newY < -40) {
                f.supprimer(c);
                stars.remove(i);
                starSpeed.remove(i);
                starY.remove(i);
                score += 1;
                if (score % 15 == 0) {
                    level++;
                }
            } else if (c.intersectionRapide(player)) {
                f.supprimer(c);
                stars.remove(i);
                starSpeed.remove(i);
                starY.remove(i);
                score += 5;
                if (score % 15 == 0) {
                    level++;
                }
            }
        }

        for (int i = bombs.size() - 1; i >= 0; i--) {
            Cercle c = bombs.get(i);
            int newY = bombY.get(i) - bombSpeed.get(i);
            bombY.set(i, newY);
            c.translater(0, -bombSpeed.get(i));
            if (newY < -40) {
                f.supprimer(c);
                bombs.remove(i);
                bombSpeed.remove(i);
                bombY.remove(i);
            } else if (c.intersectionRapide(player)) {
                f.supprimer(c);
                bombs.remove(i);
                bombSpeed.remove(i);
                bombY.remove(i);
                if (shieldActive) {
                    shieldActive = false;
                } else {
                    triggerGameOver();
                }
            }
        }

        for (int i = shields.size() - 1; i >= 0; i--) {
            Cercle c = shields.get(i);
            int newY = shieldY.get(i) - shieldSpeed.get(i);
            shieldY.set(i, newY);
            c.translater(0, -shieldSpeed.get(i));
            if (newY < -40) {
                f.supprimer(c);
                shields.remove(i);
                shieldSpeed.remove(i);
                shieldY.remove(i);
            } else if (c.intersectionRapide(player)) {
                f.supprimer(c);
                shields.remove(i);
                shieldSpeed.remove(i);
                shieldY.remove(i);
                shieldActive = true;
            }
        }
    }

    private void triggerGameOver() {
        running = false;
        gameOver = true;
        f.ajouter(overText);
        f.ajouter(restartText);
        if (!scoreSaved) {
            HighScore.enregistrerFichier("highscore", HighScore.lireFichier("highscore"), "YOU", score);
            scoreSaved = true;
        }
    }

    private void updatePlayer() {
        int speed = BASE_SPEED;
        if (boostTimer > 0) {
            speed = BOOST_SPEED;
            boostTimer--;
        }
        if (boostCooldown > 0) {
            boostCooldown--;
        }

        if (clavier.getBoutonJ1ATape() && boostCooldown == 0 && running) {
            boostTimer = BOOST_FRAMES;
            boostCooldown = BOOST_COOLDOWN;
        }

        if (clavier.getJoyJ1HautEnfoncee() && !player.intersectionRapide(limitTop)) {
            player.translater(0, speed);
        }
        if (clavier.getJoyJ1BasEnfoncee() && !player.intersectionRapide(limitBottom)) {
            player.translater(0, -speed);
        }
        if (clavier.getJoyJ1GaucheEnfoncee() && !player.intersectionRapide(limitLeft)) {
            player.translater(-speed, 0);
        }
        if (clavier.getJoyJ1DroiteEnfoncee() && !player.intersectionRapide(limitRight)) {
            player.translater(speed, 0);
        }
    }

    private void spawnLoop() {
        long now = System.currentTimeMillis();
        int starInterval = Math.max(450 - level * 15, 180);
        int bombInterval = Math.max(700 - level * 20, 260);
        int shieldInterval = 5000;

        if (now - lastStar > starInterval) {
            spawnStar();
            lastStar = now;
        }
        if (now - lastBomb > bombInterval) {
            spawnBomb();
            lastBomb = now;
        }
        if (now - lastShield > shieldInterval) {
            spawnShield();
            lastShield = now;
        }
    }

    private void updateStartScreen() {
        if (!gameOver) {
            if (clavier.getBoutonJ1ATape()) {
                f.supprimer(title);
                f.supprimer(help);
                resetGame();
            }
        } else {
            if (clavier.getBoutonJ1ATape()) {
                f.supprimer(overText);
                f.supprimer(restartText);
                resetGame();
            }
        }
    }

    public void loop() {
        while (true) {
            try {
                Thread.sleep(16);
            } catch (Exception e) {
                // ignore
            }

            if (clavier.getBoutonJ1ZTape()) {
                System.exit(0);
            }

            if (!running) {
                updateStartScreen();
                f.rafraichir();
                continue;
            }

            updatePlayer();
            spawnLoop();
            updateEntities();
            updateHud();
            f.rafraichir();
        }
    }

    public static void main(String[] args) {
        Main game = new Main();
        game.loop();
    }
}
