package fr.zwartkat.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import fr.zwartkat.Piece;
import fr.zwartkat.Position;
import fr.zwartkat.Tray;
import fr.zwartkat.pokemon.Pokemon;
import fr.zwartkat.IPlayer;
import MG2D.Couleur;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe ActionService")
class ActionServiceTest {

    private ActionService actionService;
    private EventBus eventBus;
    private CombatService combatService;
    private DamageCalculator damageCalculator;
    private Tray tray;
    private Piece piece;
    private Pokemon pokemon;
    private IPlayer mockPlayer;

    // Mock implementation of IPlayer
    static class MockPlayer implements IPlayer {
        private int id;
        
        MockPlayer(int id) {
            this.id = id;
        }

        @Override
        public int getId() {
            return id;
        }

        @Override
        public Couleur getColor() {
            return null;
        }

        @Override
        public void setColor(Couleur color) {
        }

        @Override
        public void addPiece(Piece piece) {
        }

        @Override
        public boolean removePiece(Piece piece) {
            return false;
        }

        @Override
        public boolean removePieceAtPosition(Position position) {
            return false;
        }

        @Override
        public void setPieces(Piece piece) {
        }

        @Override
        public Piece getMasterPiece() {
            return null;
        }

        @Override
        public void setMasterPiece(Piece piece) {
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (!(obj instanceof MockPlayer)) return false;
            return id == ((MockPlayer) obj).id;
        }
    }



    @BeforeEach
    void setup() {
        eventBus = new EventBus();
        damageCalculator = new DamageCalculator();
        combatService = new CombatService(damageCalculator);
        actionService = new ActionService(eventBus, combatService);
        
        tray = new Tray(9);
        pokemon = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        mockPlayer = new MockPlayer(1);
        piece = new Piece(pokemon, mockPlayer, 4, 4);
        
        tray.add(piece.getPosition(), piece);
    }

    @Test
    @DisplayName("Test calculatePossibleMoves au centre du plateau")
    void testCalculatePossibleMovesInCenter() {
        List<Position> moves = actionService.calculatePossibleMoves(tray, piece);
        
        assertNotNull(moves);
        // Vérifier que les mouvements sont autour de la pièce
        assertTrue(moves.stream().allMatch(pos -> 
            Math.abs(pos.getX() - piece.getPosition().getX()) <= 1 &&
            Math.abs(pos.getY() - piece.getPosition().getY()) <= 1
        ));
    }

    @Test
    @DisplayName("Test calculatePossibleMoves au coin du plateau")
    void testCalculatePossibleMovesAtCorner() {
        Piece cornerPiece = new Piece(pokemon, mockPlayer, 0, 0);
        tray = new Tray(9);
        tray.add(cornerPiece.getPosition(), cornerPiece);
        
        List<Position> moves = actionService.calculatePossibleMoves(tray, cornerPiece);
        
        assertTrue(moves.size() <= 3, "Au coin, il ne peut y avoir que 3 mouvements max");
        assertTrue(moves.stream().allMatch(pos -> pos.getX() >= 0 && pos.getY() >= 0));
    }

    @Test
    @DisplayName("Test calculatePossibleMoves n'inclut pas les positions occupées")
    void testCalculatePossibleMovesExcludesOccupiedPositions() {
        Piece otherPiece = new Piece(pokemon, mockPlayer, 5, 4);
        tray.add(otherPiece.getPosition(), otherPiece);
        
        List<Position> moves = actionService.calculatePossibleMoves(tray, piece);
        
        assertFalse(moves.contains(otherPiece.getPosition()));
    }

    @Test
    @DisplayName("Test calculatePossibleMoves n'inclut pas la position actuelle")
    void testCalculatePossibleMovesExcludesCurrentPosition() {
        List<Position> moves = actionService.calculatePossibleMoves(tray, piece);
        
        assertFalse(moves.contains(piece.getPosition()));
    }

    @Test
    @DisplayName("Test calculatePossibleAttacks retourne les adversaires")
    void testCalculatePossibleAttacks() {
        IPlayer adversary = new MockPlayer(2);
        Piece enemyPiece = new Piece(pokemon, adversary, 5, 4);
        tray.add(enemyPiece.getPosition(), enemyPiece);
        
        List<Position> attacks = actionService.calculatePossibleAttacks(tray, piece);
        
        assertTrue(attacks.contains(enemyPiece.getPosition()));
    }

    @Test
    @DisplayName("Test calculatePossibleAttacks n'inclut pas les alliés")
    void testCalculatePossibleAttacksExcludesAllies() {
        Piece allyPiece = new Piece(pokemon, mockPlayer, 5, 4);
        tray.add(allyPiece.getPosition(), allyPiece);
        
        List<Position> attacks = actionService.calculatePossibleAttacks(tray, piece);
        
        assertFalse(attacks.contains(allyPiece.getPosition()));
    }

    @Test
    @DisplayName("Test getAroundCase retourne les positions autour")
    void testGetAroundCaseReturnsSurroundingPositions() {
        List<Position> around = actionService.getAroundCase(tray, piece, 1);
        
        assertNotNull(around);
        assertFalse(around.contains(piece.getPosition()));
        assertTrue(around.size() > 0);
    }

    @Test
    @DisplayName("Test getAroundCase avec range 2")
    void testGetAroundCaseWithRange2() {
        List<Position> around = actionService.getAroundCase(tray, piece, 2);
        List<Position> around1 = actionService.getAroundCase(tray, piece, 1);
        
        assertTrue(around.size() >= around1.size());
    }

    @Test
    @DisplayName("Test move change la position de la pièce")
    void testMoveChangesPosition() {
        Position newPos = new Position(5, 4);
        actionService.move(tray, piece, newPos);
        
        assertEquals(newPos, piece.getPosition());
    }

    @Test
    @DisplayName("Test move met à jour le plateau")
    void testMoveUpdatesTray() {
        Position newPos = new Position(5, 4);
        actionService.move(tray, piece, newPos);
        
        assertNull(tray.getCase(4, 4));
        assertEquals(piece, tray.getCase(5, 4));
    }

    @Test
    @DisplayName("Test attack retourne un CombatResult")
    void testAttackReturnsCombatResult() {
        IPlayer adversary = new MockPlayer(2);
        Piece enemyPiece = new Piece(
            new Pokemon(26, "Raichu", 60, 90, 55, 100, "ELECTRIK", "SANS"),
            adversary, 5, 4
        );
        tray.add(enemyPiece.getPosition(), enemyPiece);
        
        CombatResult result = actionService.attack(piece, enemyPiece);
        
        assertNotNull(result);
    }

    @Test
    @DisplayName("Test getAroundCase respecte les limites du plateau")
    void testGetAroundCaseRespectsBoardLimits() {
        Piece cornerPiece = new Piece(pokemon, mockPlayer, 0, 0);
        List<Position> around = actionService.getAroundCase(tray, cornerPiece, 1);
        
        assertTrue(around.stream().allMatch(pos -> 
            pos.getX() >= 0 && pos.getX() < tray.getSize() &&
            pos.getY() >= 0 && pos.getY() < tray.getSize()
        ));
    }
}
