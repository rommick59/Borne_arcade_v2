package fr.zwartkat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import fr.zwartkat.pokemon.Pokemon;
import MG2D.Couleur;

import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Tests de la classe Tray")
class TrayTest {

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
    }

    @BeforeEach
    void setup() {
        tray = new Tray(9);
        pokemon = new Pokemon(25, "Pikachu", 35, 55, 40, 90, "ELECTRIK", "SANS");
        mockPlayer = new MockPlayer(1);
        piece = new Piece(pokemon, mockPlayer, 3, 4);
    }

    @Test
    @DisplayName("Création d'un Tray avec une taille")
    void testConstructor() {
        Tray tray = new Tray(9);
        assertEquals(9, tray.getSize());
    }

    @Test
    @DisplayName("Test add ajoute une pièce au plateau")
    void testAddPiece() {
        tray.add(piece.getPosition(), piece);
        
        assertEquals(piece, tray.getCase(piece.getPosition()));
    }

    @Test
    @DisplayName("Test getCase avec Position")
    void testGetCaseWithPosition() {
        tray.add(piece.getPosition(), piece);
        
        assertEquals(piece, tray.getCase(new Position(3, 4)));
    }

    @Test
    @DisplayName("Test getCase avec coordonnées int")
    void testGetCaseWithIntegers() {
        tray.add(piece.getPosition(), piece);
        
        assertEquals(piece, tray.getCase(3, 4));
    }

    @Test
    @DisplayName("Test getCase avec String")
    void testGetCaseWithString() {
        tray.add(piece.getPosition(), piece);
        
        assertEquals(piece, tray.getCase(piece.getPosition().toString()));
    }

    @Test
    @DisplayName("Test getCase retourne null si vide")
    void testGetCaseReturnsNullIfEmpty() {
        assertNull(tray.getCase(new Position(5, 5)));
    }

    @Test
    @DisplayName("Test remove avec Position")
    void testRemoveWithPosition() {
        tray.add(piece.getPosition(), piece);
        tray.remove(piece.getPosition());
        
        assertNull(tray.getCase(piece.getPosition()));
    }

    @Test
    @DisplayName("Test remove avec Piece")
    void testRemoveWithPiece() {
        tray.add(piece.getPosition(), piece);
        tray.remove(piece);
        
        assertNull(tray.getCase(piece.getPosition()));
    }

    @Test
    @DisplayName("Test getSize")
    void testGetSize() {
        assertEquals(9, tray.getSize());
    }

    @Test
    @DisplayName("Test getPieces retourne la HashMap")
    void testGetPieces() {
        tray.add(piece.getPosition(), piece);
        HashMap<String, Piece> pieces = tray.getPieces();
        
        assertNotNull(pieces);
        assertEquals(1, pieces.size());
    }

    @Test
    @DisplayName("Test ajouter plusieurs pièces")
    void testAddMultiplePieces() {
        Piece piece2 = new Piece(pokemon, mockPlayer, 5, 5);
        
        tray.add(piece.getPosition(), piece);
        tray.add(piece2.getPosition(), piece2);
        
        assertEquals(2, tray.getPieces().size());
        assertEquals(piece, tray.getCase(piece.getPosition()));
        assertEquals(piece2, tray.getCase(piece2.getPosition()));
    }

    @Test
    @DisplayName("Test supprimer une pièce sur plusieurs")
    void testRemoveOnePieceOutOfMultiple() {
        Piece piece2 = new Piece(pokemon, mockPlayer, 5, 5);
        
        tray.add(piece.getPosition(), piece);
        tray.add(piece2.getPosition(), piece2);
        tray.remove(piece);
        
        assertEquals(1, tray.getPieces().size());
        assertNull(tray.getCase(piece.getPosition()));
        assertEquals(piece2, tray.getCase(piece2.getPosition()));
    }

    @Test
    @DisplayName("Test remplacer une pièce à la même position")
    void testReplacePieceAtSamePosition() {
        Piece piece2 = new Piece(pokemon, mockPlayer, 3, 4);
        
        tray.add(piece.getPosition(), piece);
        tray.add(piece2.getPosition(), piece2);
        
        // La deuxième pièce remplace la première
        assertEquals(piece2, tray.getCase(3, 4));
    }

    @Test
    @DisplayName("Test Tray avec différentes tailles")
    void testTrayWithDifferentSizes() {
        Tray tray8 = new Tray(8);
        Tray tray10 = new Tray(10);
        
        assertEquals(8, tray8.getSize());
        assertEquals(10, tray10.getSize());
    }

    @Test
    @DisplayName("Test getCase avec position invalide retourne null")
    void testGetCaseWithInvalidPosition() {
        assertNull(tray.getCase(8, 8));
    }

    @Test
    @DisplayName("Test getPieces est initialement vide")
    void testGetPiecesInitiallyEmpty() {
        assertEquals(0, tray.getPieces().size());
    }
}
