import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
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

//ADDED FILES


