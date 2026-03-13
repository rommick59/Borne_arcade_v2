package fr.zwartkat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import fr.zwartkat.pokemon.Pokemon;
import MG2D.Couleur;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe Piece")
class PieceTest {

    private Piece piece;
    private Pokemon pokemon;
    private IPlayer mockPlayer;

    // Simple mock implementation of IPlayer for testing
    static class MockPlayer implements IPlayer {
        @Override
        public int getId() {
            return 1;
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
    }

    @BeforeEach
    void setup() {
        pokemon = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        mockPlayer = new MockPlayer();
    }

    @Test
    @DisplayName("Création d'une pièce avec tous les paramètres (int, int)")
    void testConstructorWithIntCoordinates() {
        piece = new Piece(pokemon, mockPlayer, 3, 4);
        
        assertEquals(pokemon, piece.getPokemon());
        assertEquals(mockPlayer, piece.getPlayer());
        assertEquals(3, piece.getPosition().getX());
        assertEquals(4, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Création d'une pièce avec Position en tant qu'objet")
    void testConstructorWithPositionObject() {
        Position pos = new Position(5, 6);
        piece = new Piece(pokemon, mockPlayer, pos);
        
        assertEquals(pokemon, piece.getPokemon());
        assertEquals(mockPlayer, piece.getPlayer());
        assertEquals(5, piece.getPosition().getX());
        assertEquals(6, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Création d'une pièce avec Position en tant que chaîne")
    void testConstructorWithStringPosition() {
        piece = new Piece(pokemon, mockPlayer, "C3");
        
        assertEquals(pokemon, piece.getPokemon());
        assertEquals(mockPlayer, piece.getPlayer());
        assertEquals(2, piece.getPosition().getX());
        assertEquals(2, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Création d'une pièce par copie")
    void testConstructorWithPieceCopy() {
        Piece original = new Piece(pokemon, mockPlayer, 3, 4);
        Piece copy = new Piece(original);
        
        assertEquals(original.getPokemon(), copy.getPokemon());
        assertEquals(original.getPlayer(), copy.getPlayer());
        assertEquals(original.getPosition().getX(), copy.getPosition().getX());
        assertEquals(original.getPosition().getY(), copy.getPosition().getY());
    }

    @Test
    @DisplayName("Test getPokemon")
    void testGetPokemon() {
        piece = new Piece(pokemon, mockPlayer, 0, 0);
        assertEquals(pokemon, piece.getPokemon());
    }

    @Test
    @DisplayName("Test getPlayer")
    void testGetPlayer() {
        piece = new Piece(pokemon, mockPlayer, 0, 0);
        assertEquals(mockPlayer, piece.getPlayer());
    }

    @Test
    @DisplayName("Test getPosition")
    void testGetPosition() {
        piece = new Piece(pokemon, mockPlayer, 3, 4);
        Position pos = piece.getPosition();
        
        assertEquals(3, pos.getX());
        assertEquals(4, pos.getY());
    }

    @Test
    @DisplayName("Position indépendante lors de la copie")
    void testPositionIndependenceAfterCopy() {
        Piece original = new Piece(pokemon, mockPlayer, 3, 4);
        Piece copy = new Piece(original);
        
        copy.getPosition().setX(7);
        
        assertEquals(3, original.getPosition().getX());
        assertEquals(7, copy.getPosition().getX());
    }

    @Test
    @DisplayName("Test avec coordonnées limites (0, 0)")
    void testPieceAtOrigin() {
        piece = new Piece(pokemon, mockPlayer, 0, 0);
        
        assertEquals(0, piece.getPosition().getX());
        assertEquals(0, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Test avec coordonnées limites (8, 8)")
    void testPieceAtMaxCoordinates() {
        piece = new Piece(pokemon, mockPlayer, 8, 8);
        
        assertEquals(8, piece.getPosition().getX());
        assertEquals(8, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Test avec position au centre")
    void testPieceAtCenter() {
        piece = new Piece(pokemon, mockPlayer, 4, 4);
        
        assertEquals(4, piece.getPosition().getX());
        assertEquals(4, piece.getPosition().getY());
    }

    @Test
    @DisplayName("Test avec coordonnées négatives (invalide)")
    void testPieceWithNegativeCoordinates() {
        assertThrows(IllegalArgumentException.class, 
                    () -> new Piece(pokemon, mockPlayer, -1, 4));
    }

    @Test
    @DisplayName("Test avec coordonnées dépassant 8 (invalide)")
    void testPieceWithCoordinatesGreaterThan8() {
        assertThrows(IllegalArgumentException.class, 
                    () -> new Piece(pokemon, mockPlayer, 9, 4));
    }

    @Test
    @DisplayName("Test avec position en chaîne invalide")
    void testPieceWithInvalidStringPosition() {
        assertThrows(IllegalArgumentException.class, 
                    () -> new Piece(pokemon, mockPlayer, "ZZ"));
    }
}
