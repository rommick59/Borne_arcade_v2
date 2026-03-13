package fr.zwartkat.pokemon;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe Type")
class TypeTest {

    @Test
    @DisplayName("Test getNomType pour NORMAL")
    void testGetNomTypeNormal() {
        assertEquals("NORMAL", Type.getNomType(Type.NORMAL));
    }

    @Test
    @DisplayName("Test getNomType pour FEU")
    void testGetNomTypeFeu() {
        assertEquals("FEU", Type.getNomType(Type.FEU));
    }

    @Test
    @DisplayName("Test getNomType pour EAU")
    void testGetNomTypeEau() {
        assertEquals("EAU", Type.getNomType(Type.EAU));
    }

    @Test
    @DisplayName("Test getNomType pour PLANTE")
    void testGetNomTypePlante() {
        assertEquals("PLANTE", Type.getNomType(Type.PLANTE));
    }

    @Test
    @DisplayName("Test getNomType pour ELECTRIK")
    void testGetNomTypeElectrik() {
        assertEquals("ELECTRIK", Type.getNomType(Type.ELECTRIK));
    }

    @Test
    @DisplayName("Test getNomType pour tous les types")
    void testGetNomTypeAllTypes() {
        String[] expectedNames = {"NORMAL", "FEU", "EAU", "PLANTE", "ELECTRIK", "GLACE", "COMBAT", "POISON", 
                                  "SOL", "VOL", "PSY", "INSECTE", "ROCHE", "SPECTRE", "DRAGON", "TENEBRES", 
                                  "ACIER", "FEE", "SANS"};
        
        for (int i = 0; i < expectedNames.length; i++) {
            assertEquals(expectedNames[i], Type.getNomType(i), 
                        "Le nom du type à l'indice " + i + " devrait être " + expectedNames[i]);
        }
    }

    @Test
    @DisplayName("Test getIndiceType avec chaines valides")
    void testGetIndiceType() {
        assertEquals(Type.NORMAL, Type.getIndiceType("NORMAL"));
        assertEquals(Type.FEU, Type.getIndiceType("FEU"));
        assertEquals(Type.EAU, Type.getIndiceType("EAU"));
        assertEquals(Type.PLANTE, Type.getIndiceType("PLANTE"));
    }

    @Test
    @DisplayName("Test getEfficacite EAU vs FEU (super efficace)")
    void testGetEfficaciteEauVsFeu() {
        assertEquals(Type.SUPER_EFFICACE, Type.getEfficacite(Type.EAU, Type.FEU));
    }

    @Test
    @DisplayName("Test getEfficacite FEU vs EAU (peu efficace)")
    void testGetEfficaciteFeuVsEau() {
        assertEquals(Type.PAS_EFFICACE, Type.getEfficacite(Type.FEU, Type.EAU));
    }

    @Test
    @DisplayName("Test getEfficacite NORMAL vs NORMAL (neutre)")
    void testGetEfficaciteNormalVsNormal() {
        assertEquals(Type.NEUTRE, Type.getEfficacite(Type.NORMAL, Type.NORMAL));
    }

    @Test
    @DisplayName("Test getEfficacite ELECTRIK vs VOL (super efficace)")
    void testGetEfficaciteElektrikVsVol() {
        assertEquals(Type.SUPER_EFFICACE, Type.getEfficacite(Type.ELECTRIK, Type.VOL));
    }

    @Test
    @DisplayName("Test getEfficacite NORMAL vs SPECTRE (inefficace)")
    void testGetEfficaciteNormalVsSpectre() {
        assertEquals(Type.INEFFICACE, Type.getEfficacite(Type.NORMAL, Type.SPECTRE));
    }

    @Test
    @DisplayName("Test constantes d'efficacité")
    void testEfficaciteConstants() {
        assertEquals(1.0, Type.NEUTRE);
        assertEquals(0.0, Type.INEFFICACE);
        assertEquals(0.5, Type.PAS_EFFICACE);
        assertEquals(2.0, Type.SUPER_EFFICACE);
    }

    @Test
    @DisplayName("Test constantes de types")
    void testTypeConstants() {
        assertEquals(0, Type.NORMAL);
        assertEquals(1, Type.FEU);
        assertEquals(2, Type.EAU);
        assertEquals(3, Type.PLANTE);
        assertEquals(4, Type.ELECTRIK);
        assertEquals(17, Type.FEE);
        assertEquals(18, Type.SANS);
    }
}
