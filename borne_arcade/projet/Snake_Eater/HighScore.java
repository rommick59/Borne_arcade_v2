import MG2D.*;
import MG2D.geometrie.*;
import java.io.File;
import java.awt.Font;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;

class HighScore{

    // Résout un chemin de highscore pour éviter les écritures dans un mauvais dossier lorsque
    // le jeu est lancé depuis un répertoire différent. On teste plusieurs emplacements connus
    // et on retient le premier existant ou créable.
    private static String resolveHighScorePath(String chemin){
        String[] candidats = {
            chemin,
            "./"+chemin,
            "../"+chemin,
            "../../"+chemin,
            System.getProperty("user.home")+"/saé/borne_arcade/borne_arcade/"+chemin
        };
        for(String c : candidats){
            try{
                File f = new File(c);
                File parent = f.getParentFile();
                if(parent == null || parent.exists()){
                    return f.getPath();
                }
            }catch(Exception e){ /* ignore and try next */ }
        }
        return chemin;
    }

    public static char suivant(char c){
	if(c>='A' && c<'Z')
	    return (char)(c+1);
	if(c=='Z')
	    return '.';
	if(c=='.')
	    return ' ';
	return 'A';
    }

    public static char precedent(char c){
	if(c>'A' && c<='Z')
	    return (char)(c-1);
	if(c=='A')
	    return ' ';
	if(c==' ')
	    return '.';
	return 'Z';
    }

    public static void demanderEnregistrerNom(Fenetre f, ClavierBorneArcade clavier, Texture t, int s, String fichierHighScore){

	fichierHighScore = resolveHighScorePath(fichierHighScore);
	ArrayList<LigneHighScore> list = lireFichier(fichierHighScore);
	for(LigneHighScore l:list)
	    System.out.println(l);

	int position=0;
	boolean fin = false;
	while(!fin){
	    if(position==list.size())
		fin=true;
	    else
		if(s<=list.get(position).getScore())
		    position++;
		else{
		    fin=true;
		}
	}

	if(position>=10){
	    try{ Thread.sleep(5000); }catch(Exception e){}
	    System.exit(0);
	}
	
	String score=s+"";

	char cprec[]={' ',' ',' '};
	char c[]={'A','A','A'}; // trois lettres uniquement
	char csuiv[]={' ',' ',' '};
	int indexSelec=0;

	Font font;
	font = null;
	try{
	    // utiliser le chemin relatif du repo; fallback si non trouvé
	    File in = new File("fonts/PrStart.ttf");
	    if(!in.exists()){
		// tenter chemin absolu legacy sur Raspberry Pi
		in = new File("/home/pi/git/borne_arcade/fonts/PrStart.ttf");
	    }
	    font = Font.createFont(Font.TRUETYPE_FONT, in);
	    font = font.deriveFont(40.0f);
	}catch (Exception e) {
	    System.err.println("HighScore font fallback: "+e.getMessage());
	    font = new Font("Arial", Font.BOLD, 40);
	}
	Texte highscore = new Texte(Couleur.NOIR, "H  I  G  H  S  C  O  R  E", font, new Point(640,950));
	Texte scoreAtteint = new Texte(Couleur.NOIR, score, font, new Point(420,400));
	Texte enterYourName = new Texte(Couleur.NOIR, "Entrez vos 3 lettres", font, new Point(640,800));
	Texte posNum = new Texte(Couleur.NOIR, (position+1)+"eme", font, new Point(120,400));
	Texte instructions = new Texte(Couleur.NOIR, "F = valider | Haut/Bas : lettre | Gauche/Droite : position", font, new Point(640,720));

	if(position==0)
	    posNum.setTexte("1er");

	Texte posNumPrec = new Texte(Couleur.NOIR, "", font, new Point(120,580));
	Texte posNumSuiv = new Texte(Couleur.NOIR, "", font, new Point(120,170));
	
	Texte caracteres[] = new Texte[3];
	caracteres[0] = new Texte(Couleur.NOIR, c[0]+"", font, new Point(690,400));
	caracteres[1] = new Texte(Couleur.NOIR, c[1]+"", font, new Point(840,400));
	caracteres[2] = new Texte(Couleur.NOIR, c[2]+"", font, new Point(990,400));
	Texte caracteresPrec[] = new Texte[3];
	caracteresPrec[0] = new Texte(Couleur.NOIR, cprec[0]+"", font, new Point(690,580));
	caracteresPrec[1] = new Texte(Couleur.NOIR, cprec[1]+"", font, new Point(840,580));
	caracteresPrec[2] = new Texte(Couleur.NOIR, cprec[2]+"", font, new Point(990,580));
	Texte scorePrec = new Texte(Couleur.NOIR, "", font, new Point(420,580));
	Texte caracteresSuiv[] = new Texte[3];
	caracteresSuiv[0] = new Texte(Couleur.NOIR, csuiv[0]+"", font, new Point(690,170));
	caracteresSuiv[1] = new Texte(Couleur.NOIR, csuiv[1]+"", font, new Point(840,170));
	caracteresSuiv[2] = new Texte(Couleur.NOIR, csuiv[2]+"", font, new Point(990,170));
	Texte scoreSuiv = new Texte(Couleur.NOIR, "", font, new Point(420,170));
	
	Rectangle rect1 = new Rectangle(Couleur.NOIR,new Point(650,350), new Point(720,480), false);
	Rectangle rect2 = new Rectangle(Couleur.NOIR,new Point(800,350), new Point(870,480), false);
	Rectangle rect3 = new Rectangle(Couleur.NOIR,new Point(950,350), new Point(1020,480), false);
	
	Triangle select = new Triangle(Couleur.NOIR, new Point(690,340), new Point(670,300), new Point(710,300),true);

	Texture blancTrans = new Texture("img/blancTransparent.png",new Point(0,0));

	if(t!=null)
	    f.ajouter(t);
	
	f.ajouter(blancTrans);
	f.ajouter(highscore);
	f.ajouter(scoreAtteint);
	f.ajouter(scorePrec);
	f.ajouter(scoreSuiv);
	f.ajouter(enterYourName);
	f.ajouter(instructions);
	f.ajouter(caracteres[0]);
	f.ajouter(caracteres[1]);
	f.ajouter(caracteres[2]);
	f.ajouter(caracteresPrec[0]);
	f.ajouter(caracteresPrec[1]);
	f.ajouter(caracteresPrec[2]);
	f.ajouter(caracteresSuiv[0]);
	f.ajouter(caracteresSuiv[1]);
	f.ajouter(caracteresSuiv[2]);
	f.ajouter(posNum);
	f.ajouter(posNumPrec);
	f.ajouter(posNumSuiv);
	f.ajouter(rect1);
	f.ajouter(rect2);
	f.ajouter(rect3);
	f.ajouter(select);

	if(position!=0){
	    caracteresPrec[0].setTexte(list.get(position-1).getNom().charAt(0)+"");
	    caracteresPrec[1].setTexte(list.get(position-1).getNom().charAt(1)+"");
	    caracteresPrec[2].setTexte(list.get(position-1).getNom().charAt(2)+"");
	    scorePrec.setTexte(list.get(position-1).getScore()+"");
	    if(position==1)
		posNumPrec.setTexte("1er");
	    else
		posNumPrec.setTexte(position+"eme");
	}
	if(position!=list.size()){
	    caracteresSuiv[0].setTexte(list.get(position).getNom().charAt(0)+"");
	    caracteresSuiv[1].setTexte(list.get(position).getNom().charAt(1)+"");
	    caracteresSuiv[2].setTexte(list.get(position).getNom().charAt(2)+"");
	    scoreSuiv.setTexte(list.get(position).getScore()+"");
	    posNumSuiv.setTexte((position+2)+"eme");
	}

	fin=false;

	while(!fin){
	    try{
		Thread.sleep(10);
	    }catch(Exception e){}

	    if(clavier.getJoyJ1DroiteTape()){
		if(indexSelec<2){
		    indexSelec++;
		    select.translater(150,0);
		}
	    }

	    if(clavier.getJoyJ1GaucheTape()){
		if(indexSelec>0){
		    indexSelec--;
		    select.translater(-150,0);
		}
	    }

	    if(clavier.getJoyJ1HautTape()){
		if(indexSelec<3){
		    c[indexSelec]=suivant(c[indexSelec]);
		    caracteres[indexSelec].setTexte(c[indexSelec]+"");
		}
	    }

	    if(clavier.getJoyJ1BasTape()){
		if(indexSelec<3){
		    c[indexSelec]=precedent(c[indexSelec]);
		    caracteres[indexSelec].setTexte(c[indexSelec]+"");
		}
	    }

	    if(clavier.getBoutonJ1ATape())
		fin=true;
	    
	    f.rafraichir();
	}

	enregistrerFichier(fichierHighScore, list, ""+c[0]+c[1]+c[2],s);

	// nettoyer l'overlay highscore avant de rendre la main au jeu
	try{ f.supprimer(blancTrans); }catch(Exception e){}
	try{ f.supprimer(highscore); }catch(Exception e){}
	try{ f.supprimer(scoreAtteint); }catch(Exception e){}
	try{ f.supprimer(scorePrec); }catch(Exception e){}
	try{ f.supprimer(scoreSuiv); }catch(Exception e){}
	try{ f.supprimer(enterYourName); }catch(Exception e){}
	try{ f.supprimer(posNum); }catch(Exception e){}
	try{ f.supprimer(instructions); }catch(Exception e){}
	try{ f.supprimer(posNumPrec); }catch(Exception e){}
	try{ f.supprimer(posNumSuiv); }catch(Exception e){}
	try{ f.supprimer(rect1); }catch(Exception e){}
	try{ f.supprimer(rect2); }catch(Exception e){}
	try{ f.supprimer(rect3); }catch(Exception e){}
	try{ f.supprimer(select); }catch(Exception e){}
	for(int i=0;i<caracteres.length;i++){
	    try{ f.supprimer(caracteres[i]); }catch(Exception e){}
	}
	for(int i=0;i<caracteresPrec.length;i++){
	    try{ f.supprimer(caracteresPrec[i]); }catch(Exception e){}
	}
	for(int i=0;i<caracteresSuiv.length;i++){
	    try{ f.supprimer(caracteresSuiv[i]); }catch(Exception e){}
	}
	if(t!=null){
	    try{ f.supprimer(t); }catch(Exception e){}
	}
	f.rafraichir();

	try{ Thread.sleep(5000); }catch(Exception e){}
	System.exit(0);
    }

    public static ArrayList<LigneHighScore> lireFichier(String fichier){
	ArrayList<LigneHighScore> l = new ArrayList<LigneHighScore>();

	fichier = resolveHighScorePath(fichier);

	try{
	    // s'assurer que le fichier et son répertoire existent
	    try{
		File ff = new File(fichier);
		File parent = ff.getParentFile();
		if(parent!=null && !parent.exists()) parent.mkdirs();
		if(!ff.exists()) ff.createNewFile();
	    }catch(Exception ex){ System.err.println("HighScore prepare file: "+ex.getMessage()); }
	    BufferedReader reader = new BufferedReader(new FileReader(fichier));
	    String currentLine;
	    while ((currentLine = reader.readLine()) != null) {
		// ignorer les lignes vides ou ne contenant que des espaces
		currentLine = currentLine.trim();
		if(currentLine.length() == 0) continue;
		l.add(new LigneHighScore(currentLine));
	    }
	    reader.close();
	}catch(Exception e){ System.err.println("HighScore lireFichier: "+e.getMessage()); }
	
	return l;
    }

    public static void enregistrerFichier(String fichier, ArrayList<LigneHighScore> list, String nom, int score){
	fichier = resolveHighScorePath(fichier);
	int position=0;
	boolean fin = false;
	while(!fin){
	    if(position==list.size())
		fin=true;
	    else
		if(score<=list.get(position).getScore())
		    position++;
		else{
		    fin=true;
		}
	}

	list.add(position,new LigneHighScore(nom,score));
	while(list.size()>10)
	    list.remove(list.size()-1);
	
	try{
	    // s'assurer que le répertoire existe avant d'écrire
	    try{ File ff = new File(fichier); File parent = ff.getParentFile(); if(parent!=null && !parent.exists()) parent.mkdirs(); }catch(Exception ex){ System.err.println("HighScore prepare write: "+ex.getMessage()); }
	    BufferedWriter writer = new BufferedWriter(new FileWriter(fichier));
	    for(int i=0;i<list.size();i++){
		writer.write(list.get(i).toString());
		if(i!=(list.size()-1))
		    writer.write("\n");
	    }
	    writer.close();
	}catch(Exception e){ System.err.println("HighScore enregistrerFichier: "+e.getMessage()); }

	

	
    }
}
