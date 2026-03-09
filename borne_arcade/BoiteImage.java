import MG2D.geometrie.Point;
import MG2D.geometrie.Rectangle;
import MG2D.geometrie.Texture;
import java.io.File;


public class BoiteImage extends Boite{

    Texture image;

    private static final String DEFAULT_COVER = "img/bouton2.png";

    // Try a few relative paths to find the game's cover image.
    private static String resolveCoverPath(String base){
        if(base == null || base.isEmpty()){
            return DEFAULT_COVER;
        }
        String candidate = base+"/photo_small.png";
        File f = new File(candidate);
        if(f.exists()) return candidate;
        String[] prefixes = {"./", "../", "../../"};
        for(String p : prefixes){
            f = new File(p+candidate);
            if(f.exists()) return p+candidate;
        }
        // If the path was truncated (e.g. "rojet/..."), try to restore leading 'p'.
        if(base.startsWith("rojet/")){
            candidate = "p"+base+"/photo_small.png";
            f = new File(candidate);
            if(f.exists()) return candidate;
        }
        return DEFAULT_COVER;
    }

    private void setImageSafe(String path){
        try{
            this.image.setImg(resolveCoverPath(path));
        }catch(Exception e){
            this.image.setImg(DEFAULT_COVER);
        }
        this.image.setTaille(400, 320);
    }

    BoiteImage(Rectangle rectangle, String image) {
	super(rectangle);
	this.image = new Texture(resolveCoverPath(image), new Point(760, 648));
    setImageSafe(image);
    }

    public Texture getImage() {
	return this.image;
    }

    public void setImage(String chemin) {
	setImageSafe(chemin);
    }

}
