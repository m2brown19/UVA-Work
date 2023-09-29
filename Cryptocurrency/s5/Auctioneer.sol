// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

import "./NFTManager.sol";
import "./IAuctioneer.sol";
import "./IERC165.sol";
import "./ERC721.sol";

contract Auctioneer is IAuctioneer {

    constructor() {
        nftmanager = address(new NFTManager());
        deployer = msg.sender; //check
   }

   // The following can just be the automatically created getter functions
    // from public variables

    // The address of the NFT Manager for this Auctioneer; it is meant to be
    // created and deployed when the Auctioneer constructor is called.  This
    // can just be via the getter method from a public variable.
    //function nftmanager() external view returns (address);
    address public override nftmanager;
    

    // How many auctions have been created on this Auctioneer contract; this
    // can just be via the getter method from a public variable.
    //function num_auctions() external view returns (uint);
    uint public override num_auctions;

    // How much fees, in wei, have been collected so far -- the auction
    // collects 1% fees of *successful* auctions; these are the total fees
    // that have been collected, whether paid to the deployer of the contract
    // or not.
    //function totalFees() external view returns (uint);
    uint public override totalFees;


    // How much fees, in wei, have been collected so far but not yet paid to
    // the deployer -- the auction collects 1% fees of *successful* auctions
    //function unpaidFees() external view returns (uint);
    uint public override uncollectedFees;

    // Gets the auction struct for the passed auction id.  If one lists out
    // the individual fields of the Auction struct, then one can just have
    // this be a public mapping (otherwise you run into problems
    // with "Auction memory" versus "Auction storage")
    //function auctions(uint id) external view
            //returns (uint, uint, string memory, uint, address, address, uint, uint, bool);
    mapping (uint => Auction) public override auctions; //Auction is a struct
    

    // Who is the deployer of this contract
    //function deployer() external view returns (address);
    address public override deployer;


    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
       return interfaceId == type(IAuctioneer).interfaceId || interfaceId == type(IERC165).interfaceId;
   }


   //---------------------------------------------------------------------------------

   // The following are functions you must create

    // The deployer of the contract, and ONLY that address, can collect the
    // fees that this auction contract has accumulated; a call to this by any
    // other address should revert.  This causes the fees to be paid to the
    // deployer.
    function collectFees() public override {
        //CHECK THAT ONLY DEPLOYER IS CALLING THIS

        require(msg.sender == deployer, "Only deployer can collect the fees of the auction contract");

        //pay deployer the fees
        (bool success, ) = payable(deployer).call{value: uncollectedFees}("");
        require(success, "Failed to transfer ETH");

        //if successful, remove amount from uncollectedFees
        uncollectedFees = 0;

    }

    // Start an auction.  The first three parameters are the number of
    // minutes, hours, and days for the auction to last -- they can't all be
    // zero.  The data parameter is a textual description of the auction, NOT
    // the file name; it can't be the empty string.  The reserve is the
    // minimum price that will win the auction; this amount is in wei
    // (which is 10^-18 eth), and can be zero.  The nftid is which NFT is
    // being auctioned.  This function has four things it must do: sanity
    // checks (verify valid parameters, ensure no auction with that NFT ID is
    // running), transfer the NFT over to this contract (revert if it can't),
    // create the Auction struct (which effectively starts the auction), and
    // emit the appropriate event. This returns the auction ID of the newly
    // configured auction.  These auction IDs have to start from 0 for the
    // auctions.php web page to work properly.  Note that only the owner of a
    // NFT can start an auction for it, and this should be checked via
    // require().
    function startAuction(uint m, uint h, uint d, string memory data, 
                          uint reserve, uint nftid) public override returns (uint) {
        //INFTManager(nftmanager).approve(address(this), nftid); //CONTRACT IS CALLING TRANSFER FROM. NEED Auctioneer contract to be approved to handle the nft

        require(m !=0 || h != 0 || d != 0, "Invalid time. Must be greater than 0");

        require(!Strings.equal(data, ""), "data describing auction cannot be empty");

        //Check no active auctions are runnning with this nftid
        for (uint i = 0; i < num_auctions; i++) {
            if (auctions[i].active == true) {
                //Only check for active auctions! Inactive auctions dont matter. NFT can be auctioned again!
                require(auctions[i].nftid != nftid, "nft id is already being used in an active auction!");
            }
            
        }

        //Transfer ownership of nft to the auctioneer
        //Check that owner of nft is the initiator of contract
        require(INFTManager(nftmanager).ownerOf(nftid) == msg.sender, "Must be owner of the nft to auction it. Don't scam me");

        //Check
        INFTManager(nftmanager).transferFrom(msg.sender, address(this), nftid);

        //convert to seconds
        h = h * 60 * 60;
        m = m * 60;
        d = d * 24 * 60 * 60;
        uint endTime = block.timestamp;
        endTime += m + h + d;

        //Set winner to be address(0) to start
        //Set reserve price to be highest bid to start

        //Create Auction struct
        auctions[num_auctions] = Auction(num_auctions, 0, data, reserve, address(0), msg.sender, nftid, endTime, true);


        emit auctionStartEvent(num_auctions);
        num_auctions++;

        return num_auctions - 1;



    }

    // This closes out the auction, the ID of which is passed in as a
    // parameter.  It first does the basic sanity checks (you have to figure
    // out what).  If bids were placed, then it will transfer the ether to
    // the initiator.  It will handle the transfer of the  NFT (to the
    // initiator if no bids were placed or to the winner if bids were placed)
    // In the latter case, it keeps 1% fees and emits the appropriate event.
    // The auction is marked as inactive. Note that anybody can call this
    // function, although it will only close auctions whose time has
    // expired.
    function closeAuction(uint id) public override {
        require(id < num_auctions, "Auction id does not exist yet");

        //Ensure it is not already closed...
        require(auctions[id].active, "Auction is not active anymore. Cannot close again!");

        //Ensure time has expired...
        require (auctions[id].endTime < block.timestamp, "not time to close the block yet! ");

        //Handle bids. TODO
        //return nft to initiator if no bids sent
        //TODO - handle fees
        if (auctions[id].num_bids == 0) {
            INFTManager(nftmanager).transferFrom(address(this), auctions[id].initiator, auctions[id].nftid);
        } else {
            INFTManager(nftmanager).transferFrom(address(this), auctions[id].winner, auctions[id].nftid);

            //keep 1% of fees
            uncollectedFees += auctions[id].highestBid / (100);
            totalFees += auctions[id].highestBid / (100);

            (bool success, ) = payable(auctions[id].initiator).call{value: auctions[id].highestBid - (auctions[id].highestBid / 100)}("");
            require(success, "Failed to transfer money to initiator for auction");
        }



        //mark auction inactive
        auctions[id].active = false;
        emit auctionCloseEvent(id);
    }

    // When one wants to submit a bid on a NFT; the ID of the auction is
    // passed in as a parameter, and some amount of ETH is transferred with
    // this function call.  So many sanity checks here!  See the homework
    // description some of various cases where this function should revert;
    // you get to figure out the rest.  On a successful higher bid, it should
    // update the auction struct.  Be sure to refund the previous higher
    // bidder, since they have now been outbid.
    function placeBid(uint id) payable public override {
        //ensure the sender has the specified amount. TODO
        require((msg.sender).balance >= msg.value, "bidder is too broke to bid this much");



        require(id < num_auctions, "Auction id does not exist yet, cant bid");

        //Ensure it is not already closed...
        require(auctions[id].active, "Auction is not active anymore. Cannot bid!");

        //Ensure time has expired...
        require (auctions[id].endTime > block.timestamp, "auction already closed! cant bid ");

        //where is the amount param...?
        require(msg.value > auctions[id].highestBid, "Dont be cheap! cannot bid less than or equal to highest bid!");



        //give money back to other person
        if (auctions[id].num_bids > 0) {
            (bool success, ) = payable(auctions[id].winner).call{value: auctions[id].highestBid}("");
            require(success, "Failed to refund ETH to old highest bidder");
        }
        

        //send money to contract for new highest bidder
        //Check
        //safeTransferFrom(msg.sender, address(this), nftid);

        //cant call this. it is implied already from the call with button. 
        // (bool successTwo, ) = payable(address(this)).call{value: msg.value}("");
        // require(successTwo, "Failed to transfer bid to contract");

        
        auctions[id].highestBid = msg.value;
        auctions[id].num_bids++;
        auctions[id].winner = msg.sender;

        emit higherBidEvent(id);
        

    }

    // The time left (in seconds) for the given auction, the ID of which is
    // passed in as a parameter.  This is a convenience function, since it's
    // much easier to call this rather than get the end time as a UNIX
    // timestamp.
    function auctionTimeLeft(uint id) public override view returns (uint) {
        require(id < num_auctions, "Auction id does not exist yet. Cant call time left on it");
        //require(auctions[id].endTime > block.timestamp, "No time left, it is expired");
        if (auctions[id].endTime > block.timestamp) {
            return auctions[id].endTime - block.timestamp;
        } else {
            return 0;
        }
    }


}