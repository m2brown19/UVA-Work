// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

import "./IDEX.sol";
//import "./IERC20Receiver.sol";
import "./ITokenCC.sol";


//use transfer instead of transfer from


contract DEX is IDEX {

    constructor (){
        //TokenCC mytoken = new TokenCC("MagicToken", "MT");
        // address ethPriceCon = address(new EtherPriceOracleConstant());
        
        //decimals = TokenCC(mytoken).decimals(); //check
        deployer = msg.sender;
        created_pool = false;
        adjustingLiquidity = false;
    }

    bool public adjustingLiquidity;

    address public deployer;

    bool public created_pool;


    //------------------------------------------------------------

    //------------------------------------------------------------
    // Getting the exchange rates and prices

    // How many decimals the token is shown to.  This can just call the ERC-20
    // contract to get that information, or you can save it in public
    // variable.  As the other asset is ether, we know that is to 18
    // decimals, and thus do not need a corresponding function for ether.
    //function decimals() external view returns (uint);
    uint public override decimals;




    // Get the symbol of the ERC-20 cryptocurrency.  This can just call the
    // ERC-20 contract to get that information, or you can save it in public
    // variable
    function symbol() public override view returns (string memory) {
        //return TokenCC(mytoken).symbol();
        //require(created_pool == true, "Haven't created the pool yet!");

        return ITokenCC(erc20Address).symbol();
    }

    // Get the price of 1 ETH using the EtherPricer contract; return it in
    // cents.  This just gets the price from the EtherPricer contract.
    //TODO
    function getEtherPrice() public override view returns (uint) {
        return IEtherPriceOracle(etherPricer).price();
    }

    // Get the price of 1 Token using the EtherPricer contract; return it in
    // cents.  This gets the price of ETH from the EtherPricer contract, and
    // then scales it -- based on the exchange ratio -- to determine the
    // price of the token cryptocurrency.
    //TODO
    function getTokenPrice() public override view returns (uint) {
        //TODO -- manage decimals -- token is 8 decimals. Ether is how many decimals
        //return ( x * getEtherPrice() ) / y;

        //multiple first
        return ((x * getEtherPrice()) / y) / (10 ** 10); //wrong, divide by difference of decimals. 
        //y is not num of tokens -- its num * 10 ^ 8. counteract by multiplying it over, thus getting a difference. 
        //10 to number of decimals
    }

    //------------------------------------------------------------
    // Getting the liquidity of the pool or part thereof

    // Get the k value.  If 100 ETH were added along with 1,000 of the token
    // cryptocurrency, and the former has 18 decimals and the latter 10
    // decimals, then this will return 10^33.  This can just be a public
    // variable.
    //function k() external view returns (uint);
    uint public override k;

    // How much ether is in the pool; this can just be a public variable. This is
    // in wei, so 1.5 ETH -- which has 18 decimals -- would return
    // 1,500,000,000,000,000,000.  This can just be a public variable.
    //function x() external view returns (uint);
    uint public override x;

    // How many tokens are in the pool; this can just be a public variable. As
    // with the previous, this is returned with all the decimals.  So 15 of
    // the token cryptocurrency coin, which has (say) 10 decimals, this would
    // return 150,000,000,000.  This can just be a public variable.
    //function y() external view returns (uint);
    uint public override y;

    // Get the amount of pool liquidity in USD (actually cents) using the
    // EtherPricer contract.  We assume that the ETH and the token
    // cryptocurrency have the same value, and we know (from the EtherPricer
    // smart contract) how much the ETH is worth.
    function getPoolLiquidityInUSDCents() public override view returns (uint) {
        
        //edit to get it in correct amounts. i did 100 * the price bc it is in cents...
        return (2 * (x * getEtherPrice())) / (10**18);   //assumes 1:1 ratio at beginning
    }

    // How much ETH does the address have in the pool.  This is the number in
    // wei.  This can be just be a public mapping variable.
    //function etherLiquidityForAddress(address who) external view returns (uint);
    mapping(address => uint) public override etherLiquidityForAddress;

    // How much of the token cryptocurrency does the address have in the pool.
    // This is with however many decimals the token cryptocurrency has.  This
    // can be just be a public mapping variable.
    //function tokenLiquidityForAddress(address who) external view returns (uint);
    mapping(address => uint) public override tokenLiquidityForAddress;

    //------------------------------------------------------------
    // Pool creation

    // This can be called exactly once, and creates the pool; only the
    // deployer of the contract call this.  Some amount of ETH is passed in
    // along with this call.  For purposes of this assignment, the ratio is
    // then defined based on the amount of ETH paid with this call and the
    // amount of the token cryptocurrency stated in the first parameter.  The
    // first parameter is how many of the token cryptocurrency (with all the
    // decimals) to add to the pool; the ERC-20 contract that manages that
    // token cryptocurrency is the fourth parameter (the caller needs to
    // approve this contract for that much of the token cryptocurrency before
    // the call).  The second and third parameters define the fraction --
    // 0.1% would be 1 and 1000, for example.  The last parameter is the
    // contract address of the EtherPricer contract being used, and can be
    // updated later via the setEtherPricer() function.
    function createPool(uint _tokenAmount, uint _feeNumerator, uint _feeDenominator, 
                        address _erc20token, address _etherPricer) public override payable {

                            //REQUIRE IT IS CALLED ONLY ONCE
                            require(created_pool == false, "Pool already created! Cant call again!");

                            require(msg.sender == deployer, "only deployer can call this!");

                            require(msg.value > 0, "must pass in ether with the call");

                            feeNumerator = _feeNumerator;
                            feeDenominator = _feeDenominator;

                            //The token address and etherPricer address is passed in here. Use those addresses to set up stuff. 

                            x = msg.value; // * (10**18);
                            y = _tokenAmount; // * (10**decimals);
                            k = x * y;

                            setEtherPricer(_etherPricer);
                            erc20Address = _erc20token;

                            decimals = ITokenCC(erc20Address).decimals();

                            created_pool = true;

                            //transfer from sender to dex contract
                            //transferfrom returns bool
                            //require its true
                            bool success = ITokenCC(erc20Address).transferFrom(msg.sender, address(this), _tokenAmount);
                            //bool success = ITokenCC(erc20Address).transfer(address(this), _tokenAmount);
                            require(success == true, "Failed to transfer tokens to dex contract in create pool");

                            etherLiquidityForAddress[address(this)] = (x * getEtherPrice()) / (10**18);
                            tokenLiquidityForAddress[address(this)] = (y * getTokenPrice()) / (10**8);

                            emit liquidityChangeEvent();
                            
                        }

    //------------------------------------------------------------
    // Fees

    // Get the numerator of the fee fraction; this can just be a public
    // variable.
    //function feeNumerator() external view returns (uint);
    uint public override feeNumerator;

    // Get the denominator of the fee fraction; this can just be a public
    // variable.
    //function feeDenominator() external view returns (uint);
    uint public override feeDenominator;

    // Get the amount of fees accumulated, in wei, for all addresses so far; this
    // can just be a public variable.
    //function feesEther() external view returns (uint);
    uint public override feesEther;

    // Get the amount of token fees accumulated for all addresses so far; this
    // can just be a public variable.  This will have as many decimals as the
    // token cryptocurrency has.
    //function feesToken() external view returns (uint);
    uint public override feesToken;

    //------------------------------------------------------------
    // Managing pool liquidity

    // Anybody can add liquidity to the pool.  The amount of ETH is paid along
    // with the function call.  The caller will have to approve the
    // appropriate amount of token cryptocurrency, via the ERC-20 contract,
    // for this call to complete successfully.  Note that this function does
    // NOT remove any fees.
    function addLiquidity() public override payable {
        require(created_pool == true, "Haven't created the pool yet!");
        require(msg.value > 0, "to add liquidity, it must be positive ether");
        //ether amount is in msg.value

        uint tcc_add = (msg.value * y) / x;

        //msg.val and tcc_add are the new ether and tcc to add
        //x = x + (msg.value * (10**18));
        x = x + msg.value;

        //y = y + (tcc_add * (10**decimals));
        y = y + tcc_add;

        
        k = x * y;

        //TODO pay to dex
        //ether should be implied...
        adjustingLiquidity = true;

        //token pay
        bool success = ITokenCC(erc20Address).transferFrom(msg.sender, address(this), tcc_add);
        //bool success = ITokenCC(erc20Address).transfer(address(this), tcc_add);
        require(success == true, "Failed to transfer tokens to dex contract in create pool");

        adjustingLiquidity = false;

        etherLiquidityForAddress[address(this)] = (x * getEtherPrice()) / (10**18);
        tokenLiquidityForAddress[address(this)] = (y * getTokenPrice()) / (10**8);

        emit liquidityChangeEvent();


    }

    // Remove liquidity -- both ether and token -- from the pool.  The ETH is
    // paid to the caller, and the token cryptocurrency is transferred back
    // as well.  If the parameter amount is more than the amount the address
    // has stored in the pool, this should revert.  See the homework
    // description for how fees are managed and paid out, but note that this
    // function does NOT remove any fees.  For this assignment, they cannot
    // take out more ether than they put in, and the amount of TCC that comes
    // with that cannot be more than they put in.  If the exchange rates are
    // much different, this could cause issues, but we are not going to deal
    // with those issues in this assignment, so you can ignore factoring in
    // different exchange rates.
    function removeLiquidity(uint amountEther) public override {
        require(created_pool == true, "Haven't created the pool yet!");
        require(amountEther > 0, "to subtract liquidity, it must be positive ether");
        //ether amount is in msg.value

        //check there's enough ether and tokens
        //require(msg.value * (10**18) <= address(this).balance, "cannot remove more ether than have");
        require(amountEther <= address(this).balance, "cannot remove more ether than have");
        
        uint tcc_sub = (amountEther * y) / x;

        require(tcc_sub <= ITokenCC(erc20Address).balanceOf(address(this)));

        //msg.val and tcc_add are the new ether and tcc to add
        //x = x - (msg.value * (10**18));
        x = x - amountEther;

        //y = y - (tcc_sub * (10**decimals));
        y = y - tcc_sub;

        k = x * y;

        //todo - pay to caller
        (bool success, ) = payable(msg.sender).call{value: amountEther}("");
        require (success, "payment didn't work");

        adjustingLiquidity = true;

        //bool successTwo = ITokenCC(erc20Address).transferFrom(address(this), msg.sender, tcc_sub);
        bool successTwo = ITokenCC(erc20Address).transfer(msg.sender, tcc_sub);
        require(successTwo == true, "Failed to transfer tokens to dex contract in create pool");

        adjustingLiquidity = false;

        etherLiquidityForAddress[address(this)] = (x * getEtherPrice()) / (10**18);
        tokenLiquidityForAddress[address(this)] = (y * getTokenPrice()) / (10**8);

        emit liquidityChangeEvent();
    }

    //------------------------------------------------------------
    // Exchanging currencies

    // Swaps ether for token.  The amount of ETH is passed in as payment along
    // with this call.  Note that the receive() function is of a special form, 
    // and does not have the `function` keyword.
    receive() payable external {
        require(created_pool == true, "Haven't created the pool yet!");
        require(msg.value > 0, "Positive ether required");
        //send ether to dex and get back token

        //new pool ether amount
        //x = x + (msg.value * 10**18);
        x = x + msg.value;

        uint oldy = y;
        //oldy = oldy / (10**decimals);


        y = k / x;

        //uint give_tcc_amount = oldy - (y / 10**decimals);
        uint give_tcc_amount = oldy - y;

        feesToken = feesToken + ((feeNumerator * give_tcc_amount) / feeDenominator);

        //MUST HAVE THE TOKEN AMOUNT TO GIVE BACK

        require(give_tcc_amount <= ITokenCC(erc20Address).balanceOf(address(this)));

        bool success = ITokenCC(erc20Address).transfer(msg.sender, give_tcc_amount);
        require(success == true, "Failed to transfer tokens to dex contract in receive fn");

        //etherLiquidityForAddress[address(this)] = (x * getEtherPrice()) / (10**18);
        //tokenLiquidityForAddress[address(this)] = (y * getTokenPrice()) / (10**18);

    }

    // Swap token for ether.  The ERC-20 smart contract for the token
    // cryptocurrency must be approved to transfer that much into the DEX,
    // and the appropriate amount of ETH is paid back to the caller.
    // This function is defined in the IERC20Receiver.sol file
    //
    function onERC20Received(address from, uint amount, address erc20) public override returns (bool) {
        require(created_pool == true, "Haven't created the pool yet!");
        //hanlde someone sending token and getting back ether
        require(erc20==address(this),"witty error message");

        if (adjustingLiquidity == true) {
               //do nothing
        } else {
            //an exchange
            y = y + amount;

            uint oldx = x;
            x = k / y;
            uint give_eth_back = oldx - x;

            feesEther = feesEther + ((feeNumerator * give_eth_back) / feeDenominator);


            //check the amount of ether dex has to send back
            require(give_eth_back <= address(this).balance, "cannot remove more ether than have");

            //pay ether back
            (bool success, ) = payable(msg.sender).call{value: give_eth_back}("");
            require (success, "erc20 received payment didnt work");


            bool successTwo = ITokenCC(erc20Address).transferFrom(msg.sender, address(this), amount);
            //bool successTwo = ITokenCC(erc20Address).transfer(address(this), amount);
            require(successTwo == true, "Failed to transfer tokens to dex contract in erc receive fn");

            //etherLiquidityForAddress[address(this)] = (x * getEtherPrice()) / (10**18);
            //tokenLiquidityForAddress[address(this)] = (y * getTokenPrice()) / (10**18);
        }

        return true;

    }

    //------------------------------------------------------------
    // Functions for debugging and grading

    // This function allows changing of the contract that provides the current
    // ether price.
    function setEtherPricer(address p) public override {
        etherPricer = p;
    }

    // This gets the address of the etherPricer being used so that we can
    // verify we are using the correct one; this can just be a public variable.
    //function etherPricer() external view returns (address);
    address public override etherPricer;

    // Get the address of the ERC-20 token manager being used for the token
    // cryptocurrency; this can just be a public variable.
    //function erc20Address() external view returns (address);
    address public override erc20Address;

    //------------------------------------------------------------
    // Functions for efficiency

    // this function is just to lower the number of calls to the contract from
    // the dex.php web page; it just returns the information in many of the
    // above calls as a single call.  The information it returns is a tuple
    // and is, in order:
    //
    // 0: the address of *this* DEX contract (address)
    // 1: token cryptocurrency abbreviation (string memory)
    // 2: token cryptocurrency name (string memory)
    // 3: ERC-20 token cryptocurrency address (address)
    // 4: k (uint)
    // 5: ether liquidity (uint)
    // 6: token liquidity (uint)
    // 7: fee numerator (uint)
    // 8: fee denominator (uint)
    // 9: token decimals (uint)
    // 10: fees collected in ether (uint)
    // 11: fees collected in the token CC (uint)
    function getDEXinfo() public override view returns (address, string memory, string memory, 
                            address, uint, uint, uint, uint, uint, uint, uint, uint) {
                                return (address(this), ITokenCC(erc20Address).symbol(), ITokenCC(erc20Address).name(), erc20Address, 
                                k, x, y, feeNumerator, feeDenominator, decimals, feesEther, feesToken);
                            }

    //------------------------------------------------------------
    // Functions for a future assignment

    // This should just revert.  It is going to be used in the Arbitrage
    // assignment, so we are putting it into the interface now.
    function reset() public override pure {
        revert();
    }


    //------------------------------------------------------------
    // Inherited functions

    // From IERC165.sol; this contract supports three interfaces
    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return interfaceId == type(IDEX).interfaceId || interfaceId == type(IERC165).interfaceId || interfaceId == type(IERC20Receiver).interfaceId;
    }

}