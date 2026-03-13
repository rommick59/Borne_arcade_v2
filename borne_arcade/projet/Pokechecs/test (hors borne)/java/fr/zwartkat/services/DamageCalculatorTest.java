package fr.zwartkat.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import fr.zwartkat.pokemon.Pokemon;
import fr.zwartkat.pokemon.IPokemon;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe DamageCalculator")
class DamageCalculatorTest {

    private DamageCalculator damageCalculator;
    private Pokemon pikachu;
    private Pokemon charizard;
    private Pokemon squirtle;
    private Pokemon bulbasaur;

    @BeforeEach
    void setup() {
        damageCalculator = new DamageCalculator();
        pikachu = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        charizard = new Pokemon(6, "Charizard", 78, 84, 78, 100, "FEU", "VOL");
        squirtle = new Pokemon(7, "Squirtle", 44, 48, 65, 43, "EAU", "SANS");
        bulbasaur = new Pokemon(1, "Bulbasaur", 45, 49, 49, 45, "PLANTE", "POISON");
    }

    @Test
    @DisplayName("Test calculateDamage retourne un nombre positif")
    void testCalculateDamageIsPositive() {
        int damage = damageCalculator.calculateDamage(pikachu, charizard);
        assertTrue(damage > 0, "Les dégâts doivent être positifs");
    }

    @Test
    @DisplayName("Test calculateDamage avec attaque super efficace")
    void testCalculateDamageWithSuperEffectiveness() {
        // Eau vs Feu est super efficace
        int damageWaterVsFire = damageCalculator.calculateDamage(squirtle, charizard);
        assertTrue(damageWaterVsFire > 0);
    }

    @Test
    @DisplayName("Test calculateDamage augmente avec l'attaque")
    void testCalculateDamageIncreaseWithAttack() {
        Pokemon weakAttacker = new Pokemon(1, "Weak", 20, 10, 20, 20, "NORMAL", "SANS");
        Pokemon strongAttacker = new Pokemon(2, "Strong", 20, 100, 20, 20, "NORMAL", "SANS");
        
        int weakDamage = damageCalculator.calculateDamage(weakAttacker, squirtle);
        int strongDamage = damageCalculator.calculateDamage(strongAttacker, squirtle);
        
        assertTrue(strongDamage > weakDamage, "L'attaquant fort doit faire plus de dégâts");
    }

    @Test
    @DisplayName("Test calculateDamage diminue avec la défense")
    void testCalculateDamageDecreaseWithDefense() {
        Pokemon weakDefender = new Pokemon(3, "Weak", 20, 20, 10, 20, "NORMAL", "SANS");
        Pokemon strongDefender = new Pokemon(4, "Strong", 20, 20, 100, 20, "NORMAL", "SANS");
        
        int damageVsWeak = damageCalculator.calculateDamage(pikachu, weakDefender);
        int damageVsStrong = damageCalculator.calculateDamage(pikachu, strongDefender);
        
        assertTrue(damageVsWeak > damageVsStrong, "Les dégâts sur un défenseur faible doivent être plus grands");
    }

    @Test
    @DisplayName("Test calculateDamage avec type neutre")
    void testCalculateDamageNeutralType() {
        Pokemon normal = new Pokemon(100, "Normal", 50, 50, 50, 50, "NORMAL", "SANS");
        int damage = damageCalculator.calculateDamage(normal, normal);
        assertTrue(damage > 0);
    }

    @Test
    @DisplayName("Test calculateDamage est déterministe")
    void testCalculateDamageIsDeterministic() {
        int damage1 = damageCalculator.calculateDamage(pikachu, charizard);
        int damage2 = damageCalculator.calculateDamage(pikachu, charizard);
        
        assertEquals(damage1, damage2, "Le même combat doit produire les mêmes dégâts");
    }

    @Test
    @DisplayName("Test calculateDamage avec même Pokemon")
    void testCalculateDamageWithSamePokemon() {
        int damage = damageCalculator.calculateDamage(pikachu, pikachu);
        assertTrue(damage > 0);
    }
}
