package fr.zwartkat;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe Position")
class PositionTest {

    @Test
    @DisplayName("Création d'une position avec des coordonnées valides")
    void testConstructorWithValidCoordinates() {
        Position pos = new Position(3, 4);
        assertEquals(3, pos.getX());
        assertEquals(4, pos.getY());
    }

    @Test
    @DisplayName("Création d'une position avec des coordonnées invalides (x négatif)")
    void testConstructorWithNegativeX() {
        assertThrows(IllegalArgumentException.class, () -> new Position(-1, 4));
    }

    @Test
    @DisplayName("Création d'une position avec des coordonnées invalides (y négatif)")
    void testConstructorWithNegativeY() {
        assertThrows(IllegalArgumentException.class, () -> new Position(3, -1));
    }

    @Test
    @DisplayName("Création d'une position avec des coordonnées invalides (x > 8)")
    void testConstructorWithXTooLarge() {
        assertThrows(IllegalArgumentException.class, () -> new Position(9, 4));
    }

    @Test
    @DisplayName("Création d'une position avec des coordonnées invalides (y > 8)")
    void testConstructorWithYTooLarge() {
        assertThrows(IllegalArgumentException.class, () -> new Position(3, 9));
    }

    @Test
    @DisplayName("Création d'une position à partir d'une chaîne valide")
    void testConstructorWithValidString() {
        Position pos = new Position("A1");
        assertEquals(0, pos.getX());
        assertEquals(0, pos.getY());
    }

    @Test
    @DisplayName("Création d'une position à partir d'une chaîne avec majuscule")
    void testConstructorWithUppercaseString() {
        Position pos = new Position("e5");
        assertEquals(4, pos.getX());
        assertEquals(4, pos.getY());
    }

    @Test
    @DisplayName("Création d'une position à partir d'une chaîne invalide (trop courte)")
    void testConstructorWithTooShortString() {
        assertThrows(IllegalArgumentException.class, () -> new Position("A"));
    }

    @Test
    @DisplayName("Création d'une position à partir d'une chaîne invalide (pas de lettre)")
    void testConstructorWithInvalidStringNoLetter() {
        assertThrows(IllegalArgumentException.class, () -> new Position("11"));
    }

    @Test
    @DisplayName("Création d'une position à partir d'une chaîne invalide (pas de chiffre)")
    void testConstructorWithInvalidStringNoDigit() {
        assertThrows(IllegalArgumentException.class, () -> new Position("AA"));
    }

    @Test
    @DisplayName("Création d'une position à partir d'une autre position")
    void testConstructorWithPositionCopy() {
        Position original = new Position(3, 4);
        Position copy = new Position(original);
        assertEquals(3, copy.getX());
        assertEquals(4, copy.getY());
    }

    @Test
    @DisplayName("Test d'égalité entre deux positions identiques")
    void testEqualsWithIdenticalPositions() {
        Position pos1 = new Position(3, 4);
        Position pos2 = new Position(3, 4);
        assertEquals(pos1, pos2);
    }

    @Test
    @DisplayName("Test d'égalité entre deux positions différentes")
    void testEqualsWithDifferentPositions() {
        Position pos1 = new Position(3, 4);
        Position pos2 = new Position(3, 5);
        assertNotEquals(pos1, pos2);
    }

    @Test
    @DisplayName("Test du hashCode")
    void testHashCode() {
        Position pos1 = new Position(3, 4);
        Position pos2 = new Position(3, 4);
        assertEquals(pos1.hashCode(), pos2.hashCode());
    }

    @Test
    @DisplayName("Test de toString")
    void testToString() {
        Position pos = new Position("A1");
        assertEquals("A1", pos.toString());
    }

    @Test
    @DisplayName("Test de setX")
    void testSetX() {
        Position pos = new Position(3, 4);
        pos.setX(5);
        assertEquals(5, pos.getX());
    }

    @Test
    @DisplayName("Test de setY")
    void testSetY() {
        Position pos = new Position(3, 4);
        pos.setY(6);
        assertEquals(6, pos.getY());
    }

    @ParameterizedTest
    @DisplayName("Test de positions valides supplémentaires")
    @ValueSource(ints = {0, 1, 4, 7, 8})
    void testValidPositions(int coord) {
        Position pos = new Position(coord, coord);
        assertEquals(coord, pos.getX());
        assertEquals(coord, pos.getY());
    }
}
