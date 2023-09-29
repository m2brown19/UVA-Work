package project;

import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.Select;
import org.junit.jupiter.api.Test;

/*
 * @Sources: https://stackoverflow.com/questions/38684175/how-to-click-allow-on-show-notifications-popup-using-selenium-webdriver
 * 
 * Possible sites to test
 * https://www.easyunitconverter.com/base-calculator
 * https://www.inchcalculator.com/base-calculator/ 
 * https://calculator-online.net/base-calculator/ -- too slow and popups
 * 
 */




class baseCalcTest {
	
	
	
	
	//Create prefs map to store all preferences 
	//HashMap<String, Object> prefs = new HashMap<String, Object>();
	    
	private WebDriver driver;
	private String url = "https://www.inchcalculator.com/base-calculator/";
	
	//WebDriverManager.chromedriver().setup();
	
	
	//options.setExperimentalOption("excludeSwitches", Arrays.asList("disable-popup-blocking"));
	
	//options.addArgument("disable-popup-blocking");
	
	//new Actions().sendKeys(Keys.ESCAPE).build().perform();
	

    @BeforeEach
    public void setUp() 
    {
    	System.setProperty("webdriver.chrome.driver", "/Users/michaeljbrown/Desktop/chromedriver");   	   
    	
    	//Put this into prefs map to switch off browser notification
    	//prefs.put("profile.default_content_setting_values.notifications", 2);

    	//Create chrome options to set this prefs
    	//ChromeOptions options = new ChromeOptions();
    	//options.setExperimentalOption("prefs", prefs);
    	    
    	//Now initialize chrome driver with chrome options which will switch off this browser notification on the chrome browser
    	//driver = new ChromeDriver(options);
    	ChromeOptions options = new ChromeOptions();
    	options.addArguments("disable-popup-blocking");
    	
    	//options.addArguments("load-extension=/Users/michaeljbrown/Desktop/extension_5_3_0_0.crx");

    	
    	//options.setExperimentalOption("excludeSwitches", Arrays.asList("disable-popup-blocking"));
    	//options.addExtensions(new File("/Users/michaeljbrown/Desktop/extension_5_3_0_0.crx"));
    	
    	//DesiredCapabilities capabilities = new DesiredCapabilities();
    	//capabilities.setCapability(ChromeOptions.CAPABILITY, options);
    	//driver = new ChromeDriver(capabilities);
    	
        driver = new ChromeDriver(options);
      
        driver.get(url);      		   	   
    }

	@AfterEach
	public void teardown()
	{ 
	    driver.close();   
	}
	
	//INDICES SELECT-- 
	//BASE
	//Binary - 0
	//Octal - 6th
	//Decimal -- 8 index
	//Hex - 14
	//36 - 34
	
	//Indices for op
	//add - 0
	//subtract - 1
	//multiply - 2
	//divide - 3
	
	
//	C1A1 C2B1 C3C1 C4D1 C5E1
	@Test
	void binaryAddValidValidTest() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(0); 
		op.selectByIndex(0);
		
		firstNum.sendKeys("1");
		secondNum.sendKeys("0");
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
		
		//System.out.println(res.getText());
		
		String result = res.getText().toString();		

		assertEquals("1", result);
		
		
	}
	
	
	
//	C1A1 C2B2 C3C1 C4D1 C5E1
	@Test
	void binarySubtractValidValidTest() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(0); //binary
		op.selectByIndex(1); //subtract
		
		firstNum.sendKeys("0"); //valid
		secondNum.sendKeys("1"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();	

		assertEquals("-1", result);
	}
	
	
//	C1A1 C2B3 C3C1 C4D1 C5E1
	@Test
	void binaryMultiplyValidValidTest() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(0); //binary
		op.selectByIndex(2); //multiply
		
		firstNum.sendKeys("0"); //valid
		secondNum.sendKeys("0"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("0", result);
		
		
	}
	
	
	
//	C1A1 C2B4 C3C1 C4D1 C5E1
	@Test
	void binaryDivideValidValidTest() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(0); //binary
		op.selectByIndex(3); //divide
		
		firstNum.sendKeys("1"); //valid
		secondNum.sendKeys("1"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("1", result);
		
		
	}
	
	
	
//
//	C1A2 C2B1 C3C1 C4D1 C5E1
	@Test
	void octalAddValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(6); //octal
		op.selectByIndex(0); //add
		
		firstNum.sendKeys("2"); //valid
		secondNum.sendKeys("2"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("4", result);
		
		
		
	}
	
////	C1A2 C2B2 C3C1 C4D1 C5E1
	@Test
	void octalSubtractValidValidTest() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(6); //octal
		op.selectByIndex(1); //subtract
		
		firstNum.sendKeys("4"); //valid
		secondNum.sendKeys("1"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("3", result);
		
		
	}

////	C1A2 C2B3 C3C1 C4D1 C5E1
	@Test
	void octalMultiplyValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(6); //octal
		op.selectByIndex(2); //multiply
		
		firstNum.sendKeys("7"); //valid
		secondNum.sendKeys("3"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("25", result);
		
		
	}
//	
////	C1A2 C2B4 C3C1 C4D1 C5E1
	@Test
	void octalDivideValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(6); //octal
		op.selectByIndex(3); //divide
		
		firstNum.sendKeys("6"); //valid
		secondNum.sendKeys("6"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("1", result);
		
		
	}
//	
////
////	C1A3 C2B1 C3C1 C4D1 C5E1
	@Test
	void deciAddValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(8); //decimal
		op.selectByIndex(0); //add
		
		firstNum.sendKeys("1"); //valid
		secondNum.sendKeys("9"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("10", result);
		
		
	}
//	
////	C1A3 C2B2 C3C1 C4D1 C5E1
	@Test 
	void deciSubtractValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(8); //decimal
		op.selectByIndex(1); //subtract
		
		firstNum.sendKeys("7"); //valid
		secondNum.sendKeys("3"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("4", result);
		
		
	}
//	
////	C1A3 C2B3 C3C1 C4D1 C5E1
	@Test
	void deciMultiplyValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(8); //decimal
		op.selectByIndex(2); //multiply
		
		firstNum.sendKeys("2"); //valid
		secondNum.sendKeys("8"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("16", result);
		
		
	}
//	
////	C1A3 C2B4 C3C1 C4D1 C5E1
	@Test
	void deciDivideValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(8); //decimal
		op.selectByIndex(3); //divide
		
		firstNum.sendKeys("8"); //valid
		secondNum.sendKeys("2"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("4", result);
		
//		String wholePage = driver.getPageSource();
//		assertTrue(wholePage.contains("Number One has invalid symbols"));
//		assertTrue(!wholePage.contains("Number Two has invalid symbols"));
	}
//	
////
////	C1A4 C2B1 C3C1 C4D1 C5E1
	@Test
	void hexAddValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(14); //hex
		op.selectByIndex(0); //add
		
		firstNum.sendKeys("E"); //valid
		secondNum.sendKeys("E"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("1c", result);
		
		
	}
//	
////	C1A4 C2B2 C3C1 C4D1 C5E1
	@Test
	void hexSubtractValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(14); //hex
		op.selectByIndex(1); //subtract
		
		firstNum.sendKeys("C"); //valid
		secondNum.sendKeys("2"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("a", result);
		
	
	}
//	
////	C1A4 C2B3 C3C1 C4D1 C5E1
	@Test
	void hexMultiplyValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(14); //hex
		op.selectByIndex(2); //multiply
		
		firstNum.sendKeys("A"); //valid
		secondNum.sendKeys("A"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("64", result);
		
		
	}
//	
////	C1A4 C2B4 C3C1 C4D1 C5E1
	@Test
	void hexDivideValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(14); //hex
		op.selectByIndex(3); //divide
		
		firstNum.sendKeys("F"); //valid
		secondNum.sendKeys("3"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("5", result);
		
		
	}
//	
////
////	C1A5 C2B1 C3C1 C4D1 C5E1
	@Test
	void maxBaseAddValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(34); //36 base
		op.selectByIndex(0); //add
		
		firstNum.sendKeys("Z"); //valid
		secondNum.sendKeys("Z"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("1y", result);
		
		
	}

	
////	C1A5 C2B2 C3C1 C4D1 C5E1
	@Test
	void maxBaseSubtractValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(34); //36 base
		op.selectByIndex(1); //subtract
		
		firstNum.sendKeys("L"); //valid
		secondNum.sendKeys("M"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("-1", result);
		
	}
//	
////	C1A5 C2B3 C3C1 C4D1 C5E1
	@Test
	void maxBaseMultiplyValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(34); //36 base
		op.selectByIndex(2); //multiply
		
		firstNum.sendKeys("Y"); //valid
		secondNum.sendKeys("Y"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("w4", result);
		
		
	}
//	
//	
////	C1A5 C2B4 C3C1 C4D1 C5E1
	@Test
	void maxBaseDivideValidValid() {
		WebElement firstNum = driver.findElement(By.id("number_one"));
		WebElement secondNum = driver.findElement(By.id("number_two"));
		WebElement calcButton = driver.findElement(By.xpath("(//input[@value='Calculate'])")); 
		
		Select base = new Select(driver.findElement(By.xpath("//*[@id='base']")));
		Select op = new Select(driver.findElement(By.xpath("//*[@id='operator']")));
		// Select the option by index
		base.selectByIndex(34); //36 base
		op.selectByIndex(3); //divide
		
		firstNum.sendKeys("W"); //valid
		secondNum.sendKeys("G"); //valid
		
		calcButton.click();
		
		WebElement res = driver.findElement(By.className("uc_calculator_results_value"));
				
		String result = res.getText().toString();		

		assertEquals("2", result);
		
		
	}
//	
//
}
