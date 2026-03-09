1 PROBLÈME :  
Utilisation de constructeurs dépréciés pour les classes Integer et Long dans plusieurs fichiers Java, générant des warnings de compilation.

2 COMPILATIONS CONCERNÉES :  
- JavaSpace :  
- Entree.java : Ligne 20 : Création d'un Integer via le constructeur déprécié  
- Entree.java : Ligne 28 : Création d'un Long via le constructeur déprécié  
- Entree.java : Ligne 60 : Création d'un Integer via le constructeur déprécié  
- Entree.java : Ligne 64 : Création d'un Long via le constructeur déprécié  
- Entree.java : Ligne 69 : Création d'un Integer via le constructeur déprécié  
- Case.java : Ligne 30 : Création d'un Integer via le constructeur déprécié  
- ChoixValeurItem.java : Ligne 135 : Création d'un Integer via le constructeur déprécié  
- VraiIA.java : Ligne 44 : Création d'un Integer via le constructeur déprécié  

3 SOLUTION :  
Remplacer les constructeurs dépréciés de Integer et Long par Integer.valueOf(), Long.valueOf() ou utiliser l'autoboxing (conversion automatique des primitives en objets).  

4 EXEMPLE DE CORRECTION :  
AVANT :  
Integer toucheInteger = new Integer(touche);  
derniereRecupTouche.put(toucheInteger, new Long(maintenant));  

APRÈS :  
Integer toucheInteger = Integer.valueOf(touche);  
derniereRecupTouche.put(toucheInteger, Long.valueOf(maintenant));