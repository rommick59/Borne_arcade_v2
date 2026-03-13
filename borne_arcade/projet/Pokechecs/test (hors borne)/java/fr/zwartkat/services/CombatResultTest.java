package fr.zwartkat.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe CombatResult")
class CombatResultTest {

    private CombatResult result;

    @Test
    @DisplayName("Création d'un CombatResult avec tous les paramètres")
    void testConstructor() {
        result = new CombatResult(10, 20, false, false);
        
        assertEquals(10, result.getDamageToAttacker());
        assertEquals(20, result.getDamageToDefender());
        assertFalse(result.isAttackerKo());
        assertFalse(result.isDefenderKo());
    }

    @Test
    @DisplayName("Test getDamageToAttacker")
    void testGetDamageToAttacker() {
        result = new CombatResult(15, 25, false, false);
        assertEquals(15, result.getDamageToAttacker());
    }

    @Test
    @DisplayName("Test getDamageToDefender")
    void testGetDamageToDefender() {
        result = new CombatResult(15, 25, false, false);
        assertEquals(25, result.getDamageToDefender());
    }

    @Test
    @DisplayName("Test isAttackerKo avec attacker en vie")
    void testIsAttackerKoAlive() {
        result = new CombatResult(10, 20, false, false);
        assertFalse(result.isAttackerKo());
    }

    @Test
    @DisplayName("Test isAttackerKo avec attacker KO")
    void testIsAttackerKoKnockedOut() {
        result = new CombatResult(10, 20, true, false);
        assertTrue(result.isAttackerKo());
    }

    @Test
    @DisplayName("Test isDefenderKo avec defender en vie")
    void testIsDefenderKoAlive() {
        result = new CombatResult(10, 20, false, false);
        assertFalse(result.isDefenderKo());
    }

    @Test
    @DisplayName("Test isDefenderKo avec defender KO")
    void testIsDefenderKoKnockedOut() {
        result = new CombatResult(10, 20, false, true);
        assertTrue(result.isDefenderKo());
    }

    @Test
    @DisplayName("Test avec dégâts égaux")
    void testWithEqualDamages() {
        result = new CombatResult(15, 15, false, false);
        assertEquals(result.getDamageToAttacker(), result.getDamageToDefender());
    }

    @Test
    @DisplayName("Test avec dégâts nuls")
    void testWithZeroDamages() {
        result = new CombatResult(0, 0, false, false);
        assertEquals(0, result.getDamageToAttacker());
        assertEquals(0, result.getDamageToDefender());
    }

    @Test
    @DisplayName("Test avec les deux pokemons KO")
    void testWithBothKnockedOut() {
        result = new CombatResult(10, 20, true, true);
        assertTrue(result.isAttackerKo());
        assertTrue(result.isDefenderKo());
    }

    @Test
    @DisplayName("Test avec dégâts très élevés")
    void testWithHighDamages() {
        result = new CombatResult(1000, 2000, false, false);
        assertEquals(1000, result.getDamageToAttacker());
        assertEquals(2000, result.getDamageToDefender());
    }
}
