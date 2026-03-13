import MG2D.*;
import MG2D.audio.Bruitage;
import MG2D.audio.Musique;
import MG2D.geometrie.*;
import java.awt.Font;
import java.util.Scanner;

public class Main{

    public static void main(String[] args)
    {

        Scanner reponse = new Scanner(System.in);
        boolean lancer = false;
        int defaut = 0;
        int vies;
        int vitesseCoeur;
        int vitesseObstaclesMin;
        int vitesseObstaclesMax;
        int tailleObstacles;

        //System.out.print("1 : Jeu par défaut\n2 : Paramétrage\nRéponse : ");
        defaut = 1;

        if (defaut == 2) 
        {
            System.out.print("\nNombre de vies : ");
            vies = reponse.nextInt();
    
            System.out.print("\nVitesse de coeur ( 5 conseillé ) : ");
            vitesseCoeur = reponse.nextInt();
    
            System.out.print("\nVitesse minimale et maximale des obstacles ( 4  8 conseillé ) : ");
            vitesseObstaclesMin = reponse.nextInt();
            vitesseObstaclesMax = reponse.nextInt() - vitesseObstaclesMin;
    
            System.out.print("\nTaille des obstacles ( 15 conseillé ): ");
            tailleObstacles = reponse.nextInt();
        }
        else
        {
            vies = 5;
            vitesseCoeur = 4;
            vitesseObstaclesMin = 4;
            vitesseObstaclesMax = 8;
            tailleObstacles = 15;
        }
        reponse.close();

        System.out.print("\nVous pouvez ouvrir la fenêtre.");
        double points = 0;

        Fenetre f = new Fenetre("Mon jeu" , 800 , 700);
        //Clavier clavier = f.getClavier();
        ClavierBorneArcade clavier = new ClavierBorneArcade();

        clavier = new ClavierBorneArcade();
        f.addKeyListener(clavier);
        f.getP().addKeyListener(clavier);

        Rectangle fond = new Rectangle (Couleur.NOIR, new Point(0,0), new Point(800,700), true);
        Rectangle cadre_haut = new Rectangle (Couleur.BLANC, new Point(100,595), new Point(700,600), true);
        Rectangle cadre_bas = new Rectangle (Couleur.BLANC, new Point(100,95), new Point(700,100), true);
        Rectangle cadre_droite = new Rectangle (Couleur.BLANC, new Point(695,95), new Point(700,600), true);
        Rectangle cadre_gauche = new Rectangle (Couleur.BLANC, new Point(95,95), new Point(100,600), true);

        Triangle coeur_millieu = new Triangle (Couleur.ROUGE, new Point(400,350), new Point(420,350), new Point(410,335), true);
        Cercle coeur_haut1 = new Cercle(Couleur.ROUGE, new Point(404,351), 5, true);
        Cercle coeur_haut2 = new Cercle(Couleur.ROUGE, new Point(416,351), 5, true);

        Texte menu1 = new Texte(new Texte(Couleur.BLANC, "Utilisez les flèches directionnelles pour \n esquiver les projectiles", new Font("Arial", Font.TYPE1_FONT, 25), new Point(400,550)));
        Texte menu2 = new Texte(new Texte(Couleur.BLANC, "Appuyez sur A pour commencer", new Font("Arial", Font.TYPE1_FONT, 30), new Point(400,500)));


        Texte infos1 = new Texte(Couleur.VERT, (int) points + "pts", new Font("Arial", Font.TYPE1_FONT, 25), new Point(50,700));
        Texte infos2 = new Texte(Couleur.BLANC, vies + "HP", new Font("Arial", Font.TYPE1_FONT, 25), new Point(750,700));

        int o1 = (int) (Math.random()*12);
        int o2 = (int) (Math.random()*12);
        int o3 = (int) (Math.random()*12);
        int o4 = (int) (Math.random()*12);
        int o5 = (int) (Math.random()*12);
        int o6 = (int) (Math.random()*12);
        int o7 = (int) (Math.random()*12);
        int o8 = (int) (Math.random()*12);
        int o9 = (int) (Math.random()*12);
        int o10 = (int) (Math.random()*12);


        int v1 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v2 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v3 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v4 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v5 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v6 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v7 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v8 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v9 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
        int v10 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;

        f.ajouter(fond);


        f.ajouter(coeur_millieu);
        f.ajouter(coeur_haut1);
        f.ajouter(coeur_haut2);

        
        f.ajouter(menu1);
        f.ajouter(menu2);

        while (!lancer) 
        {
            if (clavier.getBoutonJ1ATape())
                lancer = true;

            f.rafraichir();
        }

        f.ajouter(cadre_haut);
        f.ajouter(cadre_bas);
        f.ajouter(cadre_droite);
        f.ajouter(cadre_gauche);


        Cercle obstacle1  = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle2 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle3 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle4 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle5 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle6 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle7 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle8 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle9 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        Cercle obstacle10 = new Cercle (Couleur.BLANC, new Point(0 , 0), tailleObstacles, true);
        

        Bruitage touche;
        Bruitage mort = new Bruitage("mort.mp3");

        replacerPoint(obstacle1, o1);
        replacerPoint(obstacle2, o2);
        replacerPoint(obstacle3, o3);
        replacerPoint(obstacle4, o4);
        replacerPoint(obstacle5, o5);
        replacerPoint(obstacle6, o6);
        replacerPoint(obstacle7, o7);
        replacerPoint(obstacle8, o8);
        replacerPoint(obstacle9, o9);
        replacerPoint(obstacle10, o10);

        f.ajouter(obstacle1);
        f.ajouter(obstacle2);
        f.ajouter(obstacle3);
        f.ajouter(obstacle4);
        f.ajouter(obstacle5);
        f.ajouter(obstacle6);
        f.ajouter(obstacle7);
        f.ajouter(obstacle8);
        f.ajouter(obstacle9);
        f.ajouter(obstacle10);

        BoiteEnglobante boiteH = cadre_haut.getBoiteEnglobante();
        BoiteEnglobante boiteB = cadre_bas.getBoiteEnglobante();
        BoiteEnglobante boiteD = cadre_droite.getBoiteEnglobante();
        BoiteEnglobante boiteG = cadre_gauche.getBoiteEnglobante();


        Musique musique = new Musique("musique.mp3");
        musique.lecture();

        long dernierTemps = System.nanoTime();

        while(vies > 0)
        {
            long frameStart = System.nanoTime();
            long tempsActuel = System.nanoTime();
            double deltaTime = (tempsActuel - dernierTemps) / 1_000_000_000.0;
            dernierTemps = tempsActuel;


            try{
            f.supprimer(menu1);
            f.supprimer(menu2);
            f.supprimer(infos1);
            f.supprimer(infos2);
            infos1 = new Texte(Couleur.VERT, (int) points + "pts", new Font("Arial", Font.TYPE1_FONT, 25), new Point(50,675));
            infos2 = new Texte(Couleur.BLANC, vies + "HP", new Font("Arial", Font.TYPE1_FONT, 25), new Point(750,675));
            if (vies == 1) {
                infos2.setCouleur(Couleur.ROUGE);
            }
            f.ajouter(infos1);
            f.ajouter(infos2);

            BoiteEnglobante boiteCoeur_HG = coeur_haut1.getBoiteEnglobante();
            BoiteEnglobante boiteCoeur_BD = coeur_millieu.getBoiteEnglobante();

            boolean collisionH = boiteH.intersection(boiteCoeur_HG);
            boolean collisionB = boiteB.intersection(boiteCoeur_BD);
            boolean collisionD = boiteD.intersection(boiteCoeur_BD);
            boolean collisionG = boiteG.intersection(boiteCoeur_HG);



            int v = (int)Math.round(vitesseCoeur * deltaTime * 60);
            if (clavier.getJoyJ1HautEnfoncee() && !collisionH) {
                coeur_millieu.translater(0, v);
                coeur_haut1.translater(0, v);
                coeur_haut2.translater(0, v);
            }

            if (clavier.getJoyJ1BasEnfoncee() && !collisionB) {
                coeur_millieu.translater(0, -v);
                coeur_haut1.translater(0, -v);
                coeur_haut2.translater(0, -v);
            }

            if (clavier.getJoyJ1DroiteEnfoncee() && !collisionD) {
                coeur_millieu.translater(v, 0);
                coeur_haut1.translater(v, 0);
                coeur_haut2.translater(v, 0);
            }

            if (clavier.getJoyJ1GaucheEnfoncee() && !collisionG) {
                coeur_millieu.translater(-v, 0);
                coeur_haut1.translater(-v, 0);
                coeur_haut2.translater(-v, 0);
            }


            deplacer(obstacle1, o1 , v1, deltaTime);
            deplacer(obstacle2, o2 , v2, deltaTime);
            deplacer(obstacle3, o3 , v3, deltaTime);
            deplacer(obstacle4, o4 , v4, deltaTime);
            deplacer(obstacle5, o5 , v5, deltaTime);
            deplacer(obstacle6, o6 , v6, deltaTime);
            deplacer(obstacle7, o7 , v7, deltaTime);
            deplacer(obstacle8, o8 , v8, deltaTime);
            deplacer(obstacle9, o9 , v9, deltaTime);
            deplacer(obstacle10, o10 , v10, deltaTime);


            boolean collision1 = obstacle1.intersection(boiteCoeur_HG) || obstacle1.intersection(boiteCoeur_BD);
            boolean collision2 = obstacle2.intersection(boiteCoeur_HG) || obstacle2.intersection(boiteCoeur_BD);
            boolean collision3 = obstacle3.intersection(boiteCoeur_HG) || obstacle3.intersection(boiteCoeur_BD);
            boolean collision4 = obstacle4.intersection(boiteCoeur_HG) || obstacle4.intersection(boiteCoeur_BD);
            boolean collision5 = obstacle5.intersection(boiteCoeur_HG) || obstacle5.intersection(boiteCoeur_BD);
            boolean collision6 = obstacle6.intersection(boiteCoeur_HG) || obstacle6.intersection(boiteCoeur_BD);
            boolean collision7 = obstacle7.intersection(boiteCoeur_HG) || obstacle7.intersection(boiteCoeur_BD);
            boolean collision8 = obstacle8.intersection(boiteCoeur_HG) || obstacle8.intersection(boiteCoeur_BD);
            boolean collision9 = obstacle9.intersection(boiteCoeur_HG) || obstacle9.intersection(boiteCoeur_BD);
            boolean collision10 = obstacle10.intersection(boiteCoeur_HG) || obstacle10.intersection(boiteCoeur_BD);

            if (collision1 || collision2 || collision3 || collision4 || collision5 || collision6 || collision7 || collision8 || collision9 || collision10) {

                touche = new Bruitage("touche.mp3");
                touche.lecture();

                try{
                    Thread.sleep(75);
                    }catch(Exception e){}

                f.ajouter(fond);
                f.rafraichir();

                try {
                    Thread.sleep(500);
                } catch(Exception e) {}


                f.ajouter(fond);
                f.ajouter(cadre_haut);
                f.ajouter(cadre_bas);
                f.ajouter(cadre_droite);
                f.ajouter(cadre_gauche);

                f.ajouter(coeur_millieu);
                f.ajouter(coeur_haut1);
                f.ajouter(coeur_haut2);

                replacerPoint(obstacle1, o1);
                replacerPoint(obstacle2, o2);
                replacerPoint(obstacle3, o3);
                replacerPoint(obstacle4, o4);
                replacerPoint(obstacle5, o5);
                replacerPoint(obstacle6, o6);
                replacerPoint(obstacle7, o7);
                replacerPoint(obstacle8, o8);
                replacerPoint(obstacle9, o9);
                replacerPoint(obstacle10, o10);

                f.ajouter(obstacle1);
                f.ajouter(obstacle2);
                f.ajouter(obstacle3);
                f.ajouter(obstacle4);
                f.ajouter(obstacle5);
                f.ajouter(obstacle6);
                f.ajouter(obstacle7);
                f.ajouter(obstacle8);
                f.ajouter(obstacle9);
                f.ajouter(obstacle10);

                vies--;
            }

            if (sortie(obstacle1))
            {
                o1 = (int) (Math.random()*12);
                v1 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle1, o1);
            }

            if (sortie(obstacle2))
            {
                o2 = (int) (Math.random()*12);
                v2 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle2, o2);
            }

            if (sortie(obstacle3))
            {
                o3 = (int) (Math.random()*12);
                v3 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle3, o3);
            }

            if (sortie(obstacle4))
            {
                o4 = (int) (Math.random()*12);
                v4 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle4, o4);
            }

            if (sortie(obstacle5))
            {
                o5 = (int) (Math.random()*12);
                v5 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle5, o5);
            }

            if (sortie(obstacle6))
            {
                o6 = (int) (Math.random()*12);
                v6 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle6, o6);
            }

            if (sortie(obstacle7))
            {
                o7 = (int) (Math.random()*12);
                v7 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle7, o7);
            }

            if (sortie(obstacle8))
            {
                o8 = (int) (Math.random()*12);
                v8 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle8, o8);
            }

            if (sortie(obstacle9))
            {
                o9 = (int) (Math.random()*12);
                v9 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle9, o9);
            }

            if (sortie(obstacle10))
            {
                o10 = (int) (Math.random()*12);
                v10 = (int)(Math.random() * (vitesseObstaclesMax - vitesseObstaclesMin + 1)) + vitesseObstaclesMin;
                points += 0.2;
                replacerPoint(obstacle10, o10);
            }


            f.rafraichir();

                long frameTime = System.nanoTime() - frameStart;
                long sleepTime = (16_666_666 - frameTime) / 1_000_000;

    if (sleepTime > 0)
        Thread.sleep(sleepTime);

        }catch(Exception e){}
        }

        f.effacer();
        f.ajouter(fond);
        musique.arret();
        mort.lecture();

        for (int i = 0; i < 10; i++) 
        {
            f.ajouter(coeur_haut1);
            f.ajouter(coeur_haut2);
            f.ajouter(coeur_millieu);
            f.rafraichir();

            try{
                Thread.sleep(75);
                }catch(Exception e){}

            f.supprimer(coeur_haut1);
            f.supprimer(coeur_haut2);
            f.supprimer(coeur_millieu);
            f.rafraichir();

            try{
                Thread.sleep(75);
                }catch(Exception e){}
        }

        try{
            Thread.sleep(2000);
            }catch(Exception e){}



        f.fermer();
        musique.arret();
        System.out.println(" \n\nVous avez gagné " + (int) points + " points !");
    }

    public static void replacerPoint( Cercle obs , int direction)
    {
        int y;

        if (direction == 0) 
        {
            y = (int) (Math.random()*500 + 100 );
            obs.setO(new Point(0 , y));
        }
        else if (direction == 1) 
        {
            y = (int) (Math.random()*600 + 100 );
            obs.setO(new Point(y , 0));
        }
        else if (direction == 2 ) 
        {
            y = (int) (Math.random()*600 + 100 );
            obs.setO(new Point(y , 700));
        }
        else if (direction == 3)
        {
            y = (int) (Math.random()*500 + 100 );
            obs.setO(new Point(800 , y));
        }
        else if (direction == 4 || direction == 5) 
        {
            y = (int) (Math.random()*800);
            obs.setO(new Point(y , 0));
        }
        else if (direction == 6 || direction == 7 ) 
        {
            y = (int) (Math.random()*700);
            obs.setO(new Point(0 ,y));
        }
        else if (direction == 8 || direction == 9) 
        {
            y = (int) (Math.random()*700);
            obs.setO(new Point(800 , y));
        }
        else if (direction == 10 || direction == 11 ) 
        {
            y = (int) (Math.random()*800);
            obs.setO(new Point(y ,700));
        }
    }

public static void deplacer(Cercle obs, int direction, int vit, double deltaTime)
{
    double v = vit * deltaTime * 60;
    int vx = (int)Math.round(v);
    int vdiag = (int)Math.round(v / Math.sqrt(2.0));

    if (direction == 0)
    {
        obs.translater(vx ,0);
    }
    else if (direction == 1)
    {
        obs.translater(0 ,vx);
    }
    else if (direction == 2)
    {
        obs.translater(0 ,-vx);
    }
    else if (direction == 3)
    {
        obs.translater(-vx ,0);
    }
    else if (direction == 4 || direction == 9)
    {
        obs.translater(-vdiag ,vdiag);
    }
    else if (direction == 5 || direction == 7)
    {
        obs.translater(vdiag ,vdiag);
    }
    else if (direction == 6 || direction == 11)
    {
        obs.translater(vdiag ,-vdiag);
    }
    else if (direction == 8 || direction == 10)
    {
        obs.translater(-vdiag ,-vdiag);
    }
}

    public static boolean sortie( Cercle obs )
    {
        if (obs.getO().getX() > 810 || obs.getO().getX() < -10 || obs.getO().getY() > 710 || obs.getO().getY() < -10 )
        {   
            return true;
        }
        else
        {
            return false;
        }
    }

}
        
