import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.*;
import java.util.Base64;

//I used the source linked from the class website to get this code for RSA
//https://www.devglan.com/java8/rsa-encryption-decryption-java


public class RSAKeyPairGenerator {

    private PrivateKey privateKey;
    private PublicKey publicKey;
    private KeyPair pair;

    public RSAKeyPairGenerator() throws NoSuchAlgorithmException, NoSuchProviderException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        SecureRandom random = SecureRandom.getInstance("SHA1PRNG", "SUN"); //Added line of code from https://stackoverflow.com/questions/5352978/keypairgenerator-is-not-generating-random-keys
        random.setSeed(random.generateSeed(8));
        keyGen.initialize(1024, random);
        this.pair = keyGen.generateKeyPair(); //modified
        this.privateKey = pair.getPrivate();
        this.publicKey = pair.getPublic();
    }

    public void writeToFile(String path, byte[] key) throws IOException {
        File f = new File(path);
        f.getParentFile().mkdirs();

        FileOutputStream fos = new FileOutputStream(f);
        fos.write(key);
        fos.flush();
        fos.close();
    }
    
    //modification. get key pair to use with bloomfield fns
    public KeyPair getKeyPair() {
    	return pair;
    }

    public PrivateKey getPrivateKey() {
        return privateKey;
    }

    public PublicKey getPublicKey() {
        return publicKey;
    }
    
    
}