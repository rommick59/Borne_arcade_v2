package fr.zwartkat.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import fr.zwartkat.pokemon.Pokemon;
import fr.zwartkat.pokemon.IPokemon;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe CombatService")
class CombatServiceTest {

    private CombatService combatService;
    private DamageCalculator damageCalculator;
    private Pokemon pikachu;
    private Pokemon charizard;
    private Pokemon squirtle;

    @BeforeEach
    void setup() {
        damageCalculator = new DamageCalculator();
        combatService = new CombatService(damageCalculator);
        
        pikachu = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        charizard = new Pokemon(6, "Charizard", 78, 84, 78, 100, "FEU", "VOL");
        squirtle = new Pokemon(7, "Squirtle", 44, 48, 65, 43, "EAU", "SANS");
    }

    @Test
    @DisplayName("Test fight entre deux pokemons valides")
    void testFightBetweenValidPokemons() {
        CombatResult result = combatService.fight(pikachu, charizard);
        
        assertNotNull(result);
        assertTrue(result.getDamageToAttacker() >= 0);
        assertTrue(result.getDamageToDefender() >= 0);
    }

    @Test
    @DisplayName("Test fight quand l'attaquant est plus rapide")
    void testFightAttackerFaster() {
        // Pikachu (vitesse 90) vs Squirtle (vitesse 43)
        CombatResult result = combatService.fight(pikachu, squirtle);
        
        // Pikachu devrait attaquer en premier
        assertTrue(result.getDamageToDefender() > 0);
    }

    @Test
    @DisplayName("Test fight quand le défenseur est plus rapide")
    void testFightDefenderFaster() {
        // Charizard (vitesse 100) vs Pikachu (vitesse 90)
        CombatResult result = combatService.fight(charizard, pikachu);
        
        assertTrue(result.getDamageToAttacker() > 0);
        assertTrue(result.getDamageToDefender() > 0);
    }

    @Test
    @DisplayName("Test fight avec vitesses égales")
    void testFightEqualSpeed() {
        Pokemon fast1 = new Pokemon(10, "Fast1", 50, 50, 50, 100, "NORMAL", "SANS");
        Pokemon fast2 = new Pokemon(11, "Fast2", 50, 50, 50, 100, "NORMAL", "SANS");
        
        CombatResult result = combatService.fight(fast1, fast2);
        assertNotNull(result);
    }

    @Test
    @DisplayName("Test fight avec un attaquant KO")
    void testFightWithAttackerKo() {
        pikachu.takeDamage(pikachu.getHp() + 10);
        
        assertThrows(IllegalStateException.class, 
                    () -> combatService.fight(pikachu, charizard));
    }

    @Test
    @DisplayName("Test fight avec un défenseur KO")
    void testFightWithDefenderKo() {
        charizard.takeDamage(charizard.getHp() + 10);
        
        assertThrows(IllegalStateException.class, 
                    () -> combatService.fight(pikachu, charizard));
    }

    @Test
    @DisplayName("Test fight avec les deux pokemons KO")
    void testFightWithBothKo() {
        pikachu.takeDamage(pikachu.getHp());
        charizard.takeDamage(charizard.getHp());
        
        assertThrows(IllegalStateException.class, 
                    () -> combatService.fight(pikachu, charizard));
    }

    @Test
    @DisplayName("Test fight le défenseur peut être KO")
    void testFightDefenderCanBeKo() {
        Pokemon lowHpDefender = new Pokemon(100, "LowHp", 1, 10, 10, 10, "NORMAL", "SANS");
        Pokemon highAtk = new Pokemon(101, "HighAtk", 100, 100, 10, 10, "NORMAL", "SANS");
        
        CombatResult result = combatService.fight(highAtk, lowHpDefender);
        
        assertTrue(result.getDamageToDefender() > 0);
        assertTrue(result.isDefenderKo() || result.getDamageToAttacker() > 0);
    }

    @Test
    @DisplayName("Test fight l'attaquant peut être KO")
    void testFightAttackerCanBeKo() {
        Pokemon lowHpAttacker = new Pokemon(100, "LowHp", 1, 10, 10, 100, "NORMAL", "SANS");
        Pokemon highAtk = new Pokemon(101, "HighAtk", 100, 100, 10, 10, "NORMAL", "SANS");
        
        CombatResult result = combatService.fight(lowHpAttacker, highAtk);
        
        // L'attaquant étant plus rapide, il devrait attaquer en premier
        assertTrue(result.getDamageToDefender() > 0);
    }

    @Test
    @DisplayName("Test fight retourne un CombatResult non null")
    void testFightReturnsNonNullResult() {
        CombatResult result = combatService.fight(pikachu, charizard);
        assertNotNull(result);
    }

    @Test
    @DisplayName("Test fight avec même pokemon")
    void testFightWithSamePokemon() {
        CombatResult result = combatService.fight(pikachu, pikachu);
        assertNotNull(result);
    }

    @Test
    @DisplayName("Test fight modifie les HP des pokemons")
    void testFightModifiesHealthPoints() {
        int initialHp1 = pikachu.getHp();
        int initialHp2 = charizard.getHp();
        
        combatService.fight(pikachu, charizard);
        
        // Au moins l'un des deux devrait avoir des dégâts
        assertTrue(pikachu.getHp() < initialHp1 || charizard.getHp() < initialHp2);
    }
}
