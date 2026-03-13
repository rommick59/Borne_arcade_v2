package fr.zwartkat.pokemon;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe Pokemon")
class PokemonTest {

    private Pokemon pikachu;
    private Pokemon charizard;
    private Pokemon squirtle;

    @BeforeEach
    void setup() {
        pikachu = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        charizard = new Pokemon(6, "Charizard", 78, 84, 78, 100, "FEU", "VOL");
        squirtle = new Pokemon(7, "Squirtle", 44, 48, 65, 43, "EAU", "SANS");
    }

    @Test
    @DisplayName("Création d'un Pokemon avec tous les paramètres")
    void testConstructor() {
        assertEquals("Pikachu", pikachu.getName());
        assertEquals(25, pikachu.getId());
        assertEquals(35, pikachu.getHp());
        assertEquals(55, pikachu.getAtk());
        assertEquals(40, pikachu.getDef());
        assertEquals(90, pikachu.getSpeed());
    }

    @Test
    @DisplayName("Test getName")
    void testGetName() {
        assertEquals("Pikachu", pikachu.getName());
        assertEquals("Charizard", charizard.getName());
    }

    @Test
    @DisplayName("Test getId")
    void testGetId() {
        assertEquals(25, pikachu.getId());
        assertEquals(6, charizard.getId());
        assertEquals(7, squirtle.getId());
    }

    @Test
    @DisplayName("Test getHp")
    void testGetHp() {
        assertEquals(35, pikachu.getHp());
        assertEquals(78, charizard.getHp());
    }

    @Test
    @DisplayName("Test getAtk")
    void testGetAtk() {
        assertEquals(55, pikachu.getAtk());
        assertEquals(84, charizard.getAtk());
    }

    @Test
    @DisplayName("Test getDef")
    void testGetDef() {
        assertEquals(40, pikachu.getDef());
        assertEquals(78, charizard.getDef());
    }

    @Test
    @DisplayName("Test getSpeed")
    void testGetSpeed() {
        assertEquals(90, pikachu.getSpeed());
        assertEquals(100, charizard.getSpeed());
    }

    @Test
    @DisplayName("Test equals avec le même Pokemon (par référence)")
    void testEqualsWithSamePokemon() {
        assertTrue(pikachu.equals(pikachu));
    }

    @Test
    @DisplayName("Test equals avec des Pokemon différents")
    void testEqualsWithDifferentPokemons() {
        assertFalse(pikachu.equals(charizard));
        assertFalse(pikachu.equals(squirtle));
    }

    @Test
    @DisplayName("Test toString contient les informations du Pokemon")
    void testToString() {
        String result = pikachu.toString();
        assertNotNull(result);
        assertTrue(result.contains("25"), "toString devrait contenir l'ID");
        assertTrue(result.contains("Pikachu"), "toString devrait contenir le nom");
    }

    @Test
    @DisplayName("Test takeDamage sans dommages")
    void testTakeDamageNoDamage() {
        int initialHp = pikachu.getHp();
        pikachu.takeDamage(0);
        assertEquals(initialHp, pikachu.getHp());
    }

    @Test
    @DisplayName("Test takeDamage avec dommages")
    void testTakeDamageWithDamage() {
        int initialHp = pikachu.getHp();
        pikachu.takeDamage(10);
        assertEquals(initialHp - 10, pikachu.getHp());
    }

    @Test
    @DisplayName("Test takeDamage avec plusieurs appels")
    void testTakeDamageMultiple() {
        int initialHp = pikachu.getHp();
        pikachu.takeDamage(5);
        pikachu.takeDamage(3);
        assertEquals(initialHp - 8, pikachu.getHp());
    }

    @Test
    @DisplayName("Test getType1")
    void testGetType1() {
        assertEquals(Type.ELECTRIK, pikachu.getType1());
        assertEquals(Type.FEU, charizard.getType1());
    }

    @Test
    @DisplayName("Test getType2")
    void testGetType2() {
        assertEquals(Type.SANS, pikachu.getType2());
        assertEquals(Type.VOL, charizard.getType2());
    }

    @Test
    @DisplayName("Test isKo avec PV intacts")
    void testIsKoWithFullHp() {
        assertFalse(pikachu.isKo());
    }

    @Test
    @DisplayName("Test isKo avec PV réduits à zéro")
    void testIsKoWithZeroHp() {
        pikachu.takeDamage(pikachu.getHp());
        assertTrue(pikachu.isKo());
    }

    @Test
    @DisplayName("Test isKo avec dégâts supérieurs aux PV")
    void testIsKoWithExcessiveDamage() {
        pikachu.takeDamage(pikachu.getHp() + 10);
        assertTrue(pikachu.isKo());
    }

    @Test
    @DisplayName("Test getTexture retourne le chemin de l'image")
    void testGetTexture() {
        String texture = pikachu.getTexture();
        assertNotNull(texture);
        assertTrue(texture.contains("25"), "La texture devrait contenir l'ID du Pokemon");
    }

    @Test
    @DisplayName("Test getCry retourne une Bruitage")
    void testGetCry() {
        assertNotNull(pikachu.getCry());
    }
}
