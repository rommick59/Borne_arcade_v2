import java.awt.Font;
import java.io.IOException;
import java.nio.file.*;
import javax.swing.*;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;
import MG2D.geometrie.Rectangle;
import MG2D.Clavier;
import MG2D.audio.*;
import java.io.File;
import MG2D.geometrie.Texte;
import MG2D.Couleur;


public class BoiteSelection extends Boite{
    Pointeur pointeur;
    Font font;
    private final File fichierSonSelection;
	private Clip clipSonSelection;
    private boolean erreurSonSelectionLoggee;

    private static final String[] CANDIDATS_SON_SELECTION = {
	"sound/bip.wav",
	"./sound/bip.wav",
	"borne_arcade/sound/bip.wav",
	"../borne_arcade/sound/bip.wav"
    };

    public BoiteSelection(Rectangle rectangle, Pointeur pointeur) {
	super(rectangle);
	this.pointeur = pointeur;
	this.fichierSonSelection = chargerFichierSonSelection();
	this.clipSonSelection = null;
	this.erreurSonSelectionLoggee = false;
	initialiserClipSonSelection();
    }

    private File chargerFichierSonSelection() {
	for (String chemin : CANDIDATS_SON_SELECTION) {
	    File fichier = new File(chemin);
	    if (fichier.exists() && fichier.isFile()) {
		return fichier;
	    }
	}
	return null;
    }

    private void initialiserClipSonSelection() {
	if (fichierSonSelection == null) {
	    return;
	}

	try (AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(fichierSonSelection)) {
	    clipSonSelection = AudioSystem.getClip();
	    clipSonSelection.open(audioInputStream);
	} catch (Exception e) {
	    clipSonSelection = null;
	    if (!erreurSonSelectionLoggee) {
		erreurSonSelectionLoggee = true;
		System.err.println("[BoiteSelection] Erreur init bip WAV: " + e.getMessage());
	    }
	}
    }

    private synchronized void jouerSonSelection() {
	if (fichierSonSelection == null) {
	    if (!erreurSonSelectionLoggee) {
		erreurSonSelectionLoggee = true;
		System.err.println("[BoiteSelection] bip introuvable. CWD=" + new File(".").getAbsolutePath());
	    }
	    return;
	}

	if (clipSonSelection != null) {
	    try {
		if (clipSonSelection.isRunning()) {
		    clipSonSelection.stop();
		}
		clipSonSelection.setFramePosition(0);
		clipSonSelection.start();
		return;
	    } catch (Exception e) {
		try {
		    clipSonSelection.close();
		} catch (Exception ignore) {
		}
		clipSonSelection = null;
		initialiserClipSonSelection();
	    }
	}

	if (!erreurSonSelectionLoggee) {
	    erreurSonSelectionLoggee = true;
	    System.err.println("[BoiteSelection] Bip WAV non initialise: " + fichierSonSelection.getPath());
	}
    }

    public boolean selection(ClavierBorneArcade clavier){
	font = null;
	try{
	    File in = new File("fonts/PrStart.ttf");
	    font = font.createFont(Font.TRUETYPE_FONT, in);
	    font = font.deriveFont(26.0f);
	}catch (Exception e) {
	    System.out.println(e.getMessage());
	}
	
	//Modifier le 07/11/2019 pour améliorer la navigation
	/*
	*	BACK:
	*	repasse au premier élément du tableau lorsque la valeur du pointeur est égale à la 	*	taille du tableau-1
	*
	*	FRONT:
	*	descend au dernier jeux de la liste afficher sur le menu  
	*/
	if(clavier.getJoyJ1HautTape() &&( pointeur.getValue() <= Graphique.tableau.length - 1)){
		if(Graphique.textesAffiches[pointeur.getValue()]==false){
			Graphique.afficherTexte(pointeur.getValue());
			Graphique.textesAffiches[pointeur.getValue()]=true;
		}
	    jouerSonSelection();
		if(pointeur.getValue() == Graphique.tableau.length -1){
			pointeur.setValue(0);
				for(int i = 0 ; i < Graphique.tableau.length ; i++){
					Graphique.tableau[i].getTexte().translater(0, 110*(Graphique.tableau.length -1));
					Graphique.tableau[i].getTexture().translater(0, 110*(Graphique.tableau.length -1));
					Graphique.tableau[i].getTexte().setPolice(font);
					Graphique.tableau[i].getTexte().setCouleur(Couleur.BLANC);
				}
		}else{
			for(int i = 0 ; i < Graphique.tableau.length ; i++){
				Graphique.tableau[i].getTexte().translater(0, -110);
				Graphique.tableau[i].getTexture().translater(0, -110);
				Graphique.tableau[i].getTexte().setPolice(font);
				Graphique.tableau[i].getTexte().setCouleur(Couleur.BLANC);
			}
			pointeur.setValue(pointeur.getValue() + 1);
		}	
	}
	//Modifier le 07/11/2019 pour améliorer la navigation
	/*
	*	BACK:
	*	repasse au dernier élément du tableau lorsque la valeur du pointeur est égale à 0
	*
	*	FRONT:
	*	Remonte au premier jeux de la liste afficher sur le menu 
	*/
	if(clavier.getJoyJ1BasTape() && pointeur.getValue() >= 0){
		if(Graphique.textesAffiches[pointeur.getValue()]==false){
			Graphique.afficherTexte(pointeur.getValue());
			Graphique.textesAffiches[pointeur.getValue()]=true;
		}
	    jouerSonSelection();
			if(pointeur.getValue() == 0){
				pointeur.setValue(Graphique.tableau.length-1);	
				for(int i = 0 ; i < Graphique.tableau.length ; i++){
					Graphique.tableau[i].getTexte().translater(0, -110*(Graphique.tableau.length-1));
					Graphique.tableau[i].getTexture().translater(0, -110*(Graphique.tableau.length-1));
					Graphique.tableau[i].getTexte().setPolice(font);
					Graphique.tableau[i].getTexte().setCouleur(Couleur.BLANC);
						
				}
			}else{
				for(int i = 0 ; i < Graphique.tableau.length ; i++){
					Graphique.tableau[i].getTexte().translater(0, 110);
					Graphique.tableau[i].getTexture().translater(0, 110);
					Graphique.tableau[i].getTexte().setPolice(font);
					Graphique.tableau[i].getTexte().setCouleur(Couleur.BLANC);
						
				}
			
				pointeur.setValue(pointeur.getValue() -1);	
				System.out.println(pointeur.getValue());		
			}
	}
	

	if(clavier.getBoutonJ1ZTape()){
	    return false;
	}
	return true;
    }

    public Pointeur getPointeur() {
	return pointeur;
    }

    public void setPointeur(Pointeur pointeur) {
	this.pointeur = pointeur;
    }

}
