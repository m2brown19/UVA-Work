import java.security.*;

//ADDED FILES: BROWNCOIN
import java.security.*;
//RSA FILE
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.spec.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.security.*;

/*
 * Michael Brown (mjb4us)
 * 
 * Sources: https://www.devglan.com/java8/rsa-encryption-decryption-java
 * 
 */
public class Main {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		brownCoin brownChain = new brownCoin();
		
		if (args[0].equals("name")) {
			brownCoin.name();
		}
		
		else if (args[0].equals("genesis")) {
			brownCoin.genesis();
			brownCoin.block_num = 1;
			
		} else if (args[0].equals("generate")) {
			//Create a wallet:pub and private key pair made via RSA
			//Save to a file as hex
			
			//from the site on rsa key generation
			RSAKeyPairGenerator keyPairGenerator = new RSAKeyPairGenerator();
	        KeyPair newKeyPair = keyPairGenerator.getKeyPair();
	        
	        //Now use with bloomfield fns. SAVE THE 1024 BIT KEY!
	        String walletFile = args[1];
	        try {
//	        	System.out.println(newKeyPair.getPrivate());
//	        	System.out.println();
	        	//System.out.println(newKeyPair.getPublic());
				brownCoin.SaveKeyPair(walletFile, newKeyPair);
				
				System.out.println("New wallet generated in '" + walletFile + "' with tag " + brownCoin.getTag(newKeyPair));
				
			} catch (Exception e) {
				
				e.printStackTrace();
			}
			
		} else if (args[0].equals("address")) {
			//Print the tag of the wallet out
			KeyPair loadedKeys = brownCoin.LoadKeyPair(args[1]); 
			System.out.println(brownCoin.getTag(loadedKeys));
			
			
			
		} else if (args[0].equals("fund")) {
			//Fund the wallet
			//daddy_warbucks spexial case id
			//next params: dest wallet tag, int amount, file name to save transaction statement to
			
			//Write a transaction statement. 
			brownCoin.fund("Daddy_warbucks", args[1], Integer.valueOf(args[2]), args[3]);
			
			
		} else if (args[0].equals("transfer")) {
			brownCoin.transfer(args[1], args[2], Integer.valueOf(args[3]), args[4]);
			
		} else if (args[0].equals("balance")) {
			
			System.out.println(brownCoin.balance(args[1]));
			
		} else if (args[0].equals("verify")) {
			brownCoin.verify(args[1], args[2]);
			
		} else if (args[0].equals("mine")) {
			brownCoin.mine(Integer.valueOf(args[1]));
			
		} else if (args[0].equals("validate")) {
			
			brownCoin.validate();
		}
		
		else {
			System.out.println("Debug");
		}
		
		
	}

}
//END MAIN
class brownCoin {
	
	public static int block_num = 1;

	//Constructor
	public brownCoin() {
		
		
	}

    // this converts an array of bytes into a hexadecimal number in
    // text format
    static String getHexString(byte[] b) {
	String result = "";
	for (int i = 0; i < b.length; i++) {
	    int val = b[i];
	    if ( val < 0 )
		val += 256;
	    if ( val <= 0xf )
		result += "0";
	    result += Integer.toString(val, 16);
	}
	return result;
    }

    // this converts a hexadecimal number in text format into an array
    // of bytes
    static byte[] getByteArray(String hexstring) {
	byte[] ret = new byte[hexstring.length()/2];
	for (int i = 0; i < hexstring.length(); i += 2) {
	    String hex = hexstring.substring(i,i+2);
	    if ( hex.equals("") )
		continue;
	    ret[i/2] = (byte) Integer.parseInt(hex,16);
	}
	return ret;
    }
    
    // This will write the public/private key pair to a file in text
    // format.  It is adapted from the code from
    // https://snipplr.com/view/18368/saveload--private-and-public-key-tofrom-a-file/
    static void SaveKeyPair(String filename, KeyPair keyPair) throws Exception {
	X509EncodedKeySpec x509EncodedKeySpec = new X509EncodedKeySpec(keyPair.getPublic().getEncoded());
	PKCS8EncodedKeySpec pkcs8EncodedKeySpec = new PKCS8EncodedKeySpec(keyPair.getPrivate().getEncoded());
	PrintWriter fout = new PrintWriter(new FileOutputStream(filename));
	fout.println(getHexString(x509EncodedKeySpec.getEncoded()));
	fout.println(getHexString(pkcs8EncodedKeySpec.getEncoded()));
	fout.close();
    }

    // This will read a public/private key pair from a file.  It is
    // adapted from the code from
    // https://snipplr.com/view/18368/saveload--private-and-public-key-tofrom-a-file/
    static KeyPair LoadKeyPair(String filename) throws Exception {
	// Read wallet
	Scanner sin = new Scanner(new File(filename));
	byte[] encodedPublicKey = getByteArray(sin.next());
	byte[] encodedPrivateKey = getByteArray(sin.next());
	sin.close();
	// Generate KeyPair.
	KeyFactory keyFactory = KeyFactory.getInstance("RSA");
	X509EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(encodedPublicKey);
	PublicKey publicKey = keyFactory.generatePublic(publicKeySpec);
	PKCS8EncodedKeySpec privateKeySpec = new PKCS8EncodedKeySpec(encodedPrivateKey);
	PrivateKey privateKey = keyFactory.generatePrivate(privateKeySpec);
	return new KeyPair(publicKey, privateKey);
    }

    // This will get the SHA-256 hash of a file, and is the same as
    // calling the `sha256sum` command line program
    static String getHashOfFile(String filename) throws Exception {
	byte[] filebytes = Files.readAllBytes(Paths.get(filename));
	MessageDigest digest = MessageDigest.getInstance("SHA-256");
	byte[] encodedHash = digest.digest(filebytes);
	return getHexString(encodedHash);
    }


	static void name() {
		System.out.println("BrownCoin");
	}

	//Create the genesis block in the blockchain. Create the mempool here too. 
	static void genesis() {
		
		try {
			FileWriter text_file = new FileWriter("block_0.txt");
			text_file.write("Genesis block created in 'block_0.txt'"); // Found code on w3schools src
			text_file.close();
			
			System.out.println("Genesis block created in 'block_0.txt'");
			
			FileWriter mem_file = new FileWriter("mempool.txt");
			mem_file.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	static void fund(String source, String destTag, int amount, String filename) {
		try {
			FileWriter text_file = new FileWriter(filename);
			text_file.write("From: " + source + "\n");
			text_file.write("To: " + destTag + "\n");
			text_file.write("Amount: " + amount + "\n");
			LocalDateTime dateObj = LocalDateTime.now(); //Got date code from w3schools
		    DateTimeFormatter formatObj = DateTimeFormatter.ofPattern("MM-dd-yyyy HH:mm:ss");

		    String cleanDate = dateObj.format(formatObj);
		    String zone = TimeZone.getDefault().getID();
		    
			
			text_file.write("Date: " + cleanDate + " " + zone + "\n");
			
			text_file.close();
			System.out.println(source + " funded wallet " + destTag + " with " + amount + " BrownCoins on " + cleanDate + " " + zone);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	//Get the tag of a wallet. pass key pair as a param. 
	static String getTag(KeyPair keys) throws NoSuchAlgorithmException {
		//only do it to n and e. 
		String loadedPubString = keys.getPublic().toString();
//		System.out.println(loadedPubString);
//		System.out.println("DEBUG");
		
		MessageDigest digest = MessageDigest.getInstance("SHA-256");
//		byte[] hash = digest.digest(loadedPubbytes.getBytes(StandardCharsets.UTF_8));
		String modu = loadedPubString.substring(56, 365);
//		String exponent = loadedPubString.substring(385, 389);
//		System.out.println(exponent);
		String modexp = modu + "65537"; //pub exponent
		
		byte[] hash = digest.digest(modexp.getBytes(StandardCharsets.UTF_8));
		
		String tag = getHexString(hash).substring(0, 16);

		return tag;
	}
	
	static void transfer(String walletFileSrc, String destTag, int amount, String transactionStatement) {
		
		//Make a transaction statement. From the source wallet file, get the tag
		//load key pair from wallet
		try {
			KeyPair keys = brownCoin.LoadKeyPair(walletFileSrc);
			String srcTag = brownCoin.getTag(keys);
			//Save src to file
			FileWriter text_file = new FileWriter(transactionStatement);
			text_file.write("From: " + srcTag + "\n");
			text_file.write("To: " + destTag + "\n"); //DEST TAG
			text_file.write("Amount: " + amount + "\n");
			
			LocalDateTime dateObj = LocalDateTime.now(); //Got date code from w3schools
		    DateTimeFormatter formatObj = DateTimeFormatter.ofPattern("MM-dd-yyyy HH:mm:ss");

		    String cleanDate = dateObj.format(formatObj);
		    String zone = TimeZone.getDefault().getID();
		    
			
			text_file.write("Date: " + cleanDate + " " + zone + "\n");
			
			//GET DIGITAL SIGNATURE
			//jdo sha-256 hash of the file
			text_file.close();
			
			//String oldSig = brownCoin.getHashOfFile(transactionStatement).toString(); //CLOSED WITH NEW EDIT
			//OPEN IT?
			String fourLines = "";
			//String signature = "";
			LineNumberReader reader;
			String strLine = "";
			
			reader = new LineNumberReader(new InputStreamReader(new FileInputStream(transactionStatement), "UTF-8"));
			while (((strLine = reader.readLine()) != null) && reader.getLineNumber() <= 4){
				fourLines += strLine + "\n";
				
			}
			reader.close();
			
//			System.out.println(fourLines);
			
			MessageDigest digest = MessageDigest.getInstance("SHA-256");
			byte[] hash = digest.digest(fourLines.getBytes(StandardCharsets.UTF_8));
			
			//System.out.println(hash);
			//signature = getHexString(hash);
			
			
			//NEW EDIT
			PrivateKey privateKey = keys.getPrivate();
			Signature privateSignature = Signature.getInstance("SHA256withRSA");
		    privateSignature.initSign(privateKey);
		    privateSignature.update(fourLines.getBytes(StandardCharsets.UTF_8)); //sign with these four lines

		    byte[] signature = privateSignature.sign();

		    String sig = Base64.getEncoder().encodeToString(signature); //digitally signed
		    //System.out.println("DEBUG" + sig);
			
			
			//END SIG EDIT
		    //BufferedWriter tranFile = new BufferedWriter(new FileWriter(transactionStatement));
	 
	            // Writing on. file
	        //tranFile.write(sig);
	 
	            // Closing file connections
	        //tranFile.close();
			
		    Files.write(Paths.get(transactionStatement), sig.getBytes(), StandardOpenOption.APPEND);
			//Files.write(Paths.get(transactionStatement), signature.getBytes(), StandardOpenOption.APPEND);
			
			
			System.out.println("Transferred " + amount + " from " + walletFileSrc + " to " + destTag + " and saved the statement to '" + transactionStatement + "' on " +cleanDate + " " + zone);

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	//
	static int balance(String tag) throws IOException {
		int total = 0;
		//Search blockchain and mempool transactions for balance. 
		
		//BLCOKS FIRST!
		for (int i = 1; i < Integer.MAX_VALUE; i++) {
			File block = new File("block_" + i + ".txt");
			if(!block.exists()) {
				//if file does not exist, do not look in it. break. 
				break;
			} else {
				//Search inside block for transactions.
				LineNumberReader reader;
				String strLine = "";
				reader = new LineNumberReader(new InputStreamReader(new FileInputStream(block), "UTF-8"));
				while (((strLine = reader.readLine()) != null)){
					if (reader.getLineNumber() != 1 && !strLine.contains("nonce")) {
						//First line in a block is hash of prev block. do not use this line for balance. 
						//nonce is in last line of block. dont use that either
						
						//Grab tags in the line and amount
						String[ ] tranLine = strLine.split(" ");
						String srcTag = tranLine[0];
						String destTag = tranLine[4];
						int amount = Integer.valueOf(tranLine[2]);
						
						//If src, subtract amount from total bc they paid it. 
						//DO NOT MAKE THESE EXCLUSIVE!
						//if dest, add amount to total
						
						if (srcTag.equals(tag)) {
							total = total - amount;
						}
						if (destTag.equals(tag)) {
							total = total + amount;
						}
						
					}
					
				}
				reader.close();
			}
		}
		
		//Check the mempool. this only has transaction lines. less checks needed. 
		LineNumberReader reader;
		String strLine = "";
		reader = new LineNumberReader(new InputStreamReader(new FileInputStream("mempool.txt"), "UTF-8"));
		while (((strLine = reader.readLine()) != null)){
			String[ ] tranLine = strLine.split(" ");
			String srcTag = tranLine[0];
			String destTag = tranLine[4];
			int amount = Integer.valueOf(tranLine[2]);
			
			//If src, subtract amount from total bc they paid it. 
			//DO NOT MAKE THESE EXCLUSIVE!
			//if dest, add amount to total
			
			if (srcTag.equals(tag)) {
				total = total - amount;
			}
			if (destTag.equals(tag)) {
				total = total + amount;
			}
		}
		
		reader.close();
		
		return total;
	}
	
	
	//walletSrcFile can also be the dest wllet of a fund cmd
	static boolean verify(String walletSrcFile, String transactionStatement) throws Exception {
		//Check signature
		BufferedReader br = null;
        String strLine = "";
        String fourLines = "";
        String signature = "";
        String amount = "";
        String srcTag = "";
        String destTag = "";
        String date = "";
        
        LineNumberReader reader;
		try {
			reader = new LineNumberReader(new InputStreamReader(new FileInputStream(transactionStatement), "UTF-8"));
			while (((strLine = reader.readLine()) != null) && reader.getLineNumber() <= 5){
				
				if (reader.getLineNumber() <= 4) { 
					fourLines += strLine + "\n"; //removed \n
					
					if (reader.getLineNumber() == 1) {
						srcTag = strLine.substring(6);
					}
					
					else if (reader.getLineNumber() == 2) {
						destTag = strLine.substring(4);
					}
					
					//Get balance if l=on line 3
					else if (reader.getLineNumber() == 3) {
						amount = strLine.substring(8);
					} else {
						date = strLine.substring(6);
					}
					
				} else {
					signature = strLine;
				}
                
			}
			reader.close();
			
			//IF THE SENDER HAS SPECIAL ID, ALLOW IT!
			if (srcTag.equals("Daddy_warbucks")) {
				String tranLine = srcTag + " transferred " + amount + " to " + destTag + " on " + date + "\n";
				Files.write(Paths.get("mempool.txt"), tranLine.getBytes(), StandardOpenOption.APPEND); //MEMPOOL IS MADE BEFORE AT GENERATION
				
				System.out.println("Any funding request (i.e., from Daddy_warbucks) is considered valid; written to the mempool\n");
				return true;
			}
			
			
			
			//Hash first four lines and verify digital signature is the same
//			MessageDigest digest = MessageDigest.getInstance("SHA-256");
//			byte[] hash = digest.digest(fourLines.getBytes(StandardCharsets.UTF_8));
//
//			String encoded = getHexString(hash);
			Signature publicSignature = Signature.getInstance("SHA256withRSA");
			KeyPair keys = brownCoin.LoadKeyPair(walletSrcFile);
		    publicSignature.initVerify(keys.getPublic());
		    publicSignature.update(fourLines.getBytes(StandardCharsets.UTF_8));

		    byte[] signatureBytes = Base64.getDecoder().decode(signature);

		    boolean verified = publicSignature.verify(signatureBytes);
			
			//String encoded = Base64.getEncoder().encodeToString(hash);
			//Compare to digital signature in file
			if (verified == true) {
				//Check balance now
				KeyPair keysSet = brownCoin.LoadKeyPair(walletSrcFile);
				String tag = brownCoin.getTag(keysSet);
				//get balance. compare to amount in balance statement. 
				if (brownCoin.balance(tag) >= Integer.valueOf(amount)) { //TODO
					String tranLine = srcTag + " transferred " + amount + " to " + destTag + " on " + date + "\n";
					Files.write(Paths.get("mempool.txt"), tranLine.getBytes(), StandardOpenOption.APPEND); //MEMPOOL IS MADE BEFORE AT GENERATION

					System.out.println("The transaction in file " + transactionStatement + " with wallet '" + walletSrcFile + "' is valid, and was written to the mempool");
					return true;
				} else {
					System.out.println("The transaction in file " + transactionStatement + " with wallet '" + walletSrcFile + "' is not valid due to a balance issue, and was not written to the mempool");
					return false;
				}
				
			} else {
//				System.out.println(encoded);
//				
//				System.out.println();
//				System.out.println(signature);
				
				System.out.println("The transaction in file " + transactionStatement + " with wallet '" + walletSrcFile + "' is not valid due to a digital signature comparison, and was not written to the mempool");

				return false;
			}
			
			
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return false;
        
         
	}
	
	//Block num starts at 1. increment after making block
	static void mine(int difficulty) throws Exception {
		//Get a nonce via brute force. 
		String entireNewBlock = "";
		String leadZeros = "";
		for (int i = 0; i < difficulty; i++) {
			leadZeros += "0";
		}
		//built substring of zeros
		
		for (int i = 0; i < Integer.MAX_VALUE; i++) {
			File f = new File("block_" + i + ".txt");
			if(!f.exists()) {
				//if file does not exist, create it after loop and break
				block_num = i;
				break;
			}
		}
		
		//get prev file hash. 
		int oldNum = (block_num - 1); 
		String prevfile = "block_" + oldNum + ".txt";
		String hashPrevFile = brownCoin.getHashOfFile(prevfile); //add this to the new block
		
		FileWriter newBlock = new FileWriter("block_" + block_num + ".txt");
		//Empty the mempool with for loop and add each line by line to block. Append!
		entireNewBlock += hashPrevFile + "\n";
		//newBlock.write(hashPrevFile + "\n");
		
		
		//READ THE MEMPOOL AND TRANSFER OVER TO NEW BLOCK
		LineNumberReader reader;
		String strLine = "";
		try {
			reader = new LineNumberReader(new InputStreamReader(new FileInputStream("mempool.txt"), "UTF-8"));
			while (((strLine = reader.readLine()) != null)){
				//newBlock.write(strLine + "\n");
				entireNewBlock += strLine + "\n";
			}
			reader.close();
			
			//newBlock.write("nonce: ");
			entireNewBlock += "nonce: ";
			
			//NOW FIND NUMBER TO PUT IN FOR NONCE. Hash string to experiment
			MessageDigest digest = MessageDigest.getInstance("SHA-256");
			int newDifficulty = difficulty;
			
			//now get the nonce
			for (int nonce = 0; nonce < Integer.MAX_VALUE; nonce++) {
				//Now, check that the hash is correct in difficulty. 
				//check with leading zeros
				String experimentString = entireNewBlock + nonce; //trial
				
				
				byte[] hash = digest.digest(experimentString.getBytes(StandardCharsets.UTF_8));
				String newBlockHash = getHexString(hash);
				
				String actualZeros = newBlockHash.substring(0, newDifficulty);
				
				if (actualZeros.equals(leadZeros)) {
					//DEBUG
					
					entireNewBlock += nonce;
					//newBlock.write(nonce);
					newBlock.write(entireNewBlock);
					
					//WRITE THE STRING TO FILE
					break;
				}
				
			}
			newBlock.close(); 
			
			//Now empty mempool
			PrintWriter writer = new PrintWriter("mempool.txt");
			writer.print("");
			writer.close();
			
		}  catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			//System.out.println("Error 1");
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			//System.out.println("Error 2");
			e.printStackTrace();
		}
	}
	
	//Validate the blockchain. only called if genesis block exists already
	
	static void validate() throws Exception {
		
		for (int i = 1; i < Integer.MAX_VALUE; i++) {
			File curBlock = new File("block_" + i + ".txt");
			if(curBlock.exists()) {
				//validate it by checking the hash of previous block
				LineNumberReader reader;
				String strLine = "";
				String curHash = "";
				
				reader = new LineNumberReader(new InputStreamReader(new FileInputStream(curBlock), "UTF-8"));
				while (((strLine = reader.readLine()) != null) && reader.getLineNumber() <= 1){
					curHash = strLine;
				}
				reader.close();
				
				//Hash of previous block
				String prevHash = brownCoin.getHashOfFile("block_" + (i -1) + ".txt"); 
				
				if ( !prevHash.equals(curHash)) {
					System.out.println("False");
					break;
				}
				
			} else {
				System.out.println("True");
				break;
			}
		}
	}
	


}



//I used the source linked from the class website to get this code for RSA
//https://www.devglan.com/java8/rsa-encryption-decryption-java


class RSAKeyPairGenerator {

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