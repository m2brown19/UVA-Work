// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

import "./IERC165.sol";
import "./NFTManager.sol";
import "./IDAO.sol";


//TODO
//implement and test functionelity
//verify that i update my pub vars
//emit events check


contract DAO is IDAO {

    constructor() {
        curator = msg.sender;
        tokens = address(new NFTManager());

        string memory uri = substring(Strings.toHexString(curator),2,34);

        INFTManager(tokens).mintWithURI(curator, uri);

    }
     //------------------------------------------------------------
    // These are all just public variables; some of which are set in the
    // constructor and never changed

    // Obtain a given proposal.   If one lists out the individual fields of
    // the Proposal struct, then one can just have this be a public mapping
    // (otherwise you run into problems with "Proposal memory"
    // versus "Proposal storage"
    //
    // @param i The proposal ID to obtain
    // @return The proposal for that ID
    //function proposals(uint i) external view returns (address,uint,string memory,uint,bool,bool,uint,uint,address);
    mapping (uint => Proposal) public override proposals;


    // The minimum debate period that a generic proposal can have, in seconds;
    // this can be set to any reasonable for testing, but should be set to 10
    // minutes (600 seconds) for final submission.  This can be a constant.
    //
    // @return The minimum debating period in seconds
    //function minProposalDebatePeriod() external view returns (uint);
    uint constant public override minProposalDebatePeriod = 600;

    // NFT token contract address
    //
    // @return The contract address of the NFTManager (ERC-721 contract)
    //function tokens() external view returns (address);
    address public override tokens;

    // A string indicating the purpose of this DAO -- be creative!  This can
    // be a constant.
    //
    // @return A string describing the purpose of this DAO
    //function purpose() external view returns (string memory);
    string constant public override purpose = "We are a patriotic organization dedicated to America. We accept anyone who wants to help the country. Be an active member and vote on proposals to help out!";

    // Simple mapping to check if a shareholder has voted for it
    //
    // @param a The address of a member who voted
    // @param pid The proposal ID of a proposal
    // @return Whether the passed member voted yes for the passed proposal
    //function votedYes(address a, uint pid) external view returns (bool);
    mapping (address => mapping(uint => bool)) public override votedYes;

    // Simple mapping to check if a shareholder has voted against it
    //
    // @param a The address of a member who voted
    // @param pid The proposal ID of a proposal
    // @return Whether the passed member voted no for the passed proposal
    //function votedNo(address a, uint pid) external view returns (bool);
    mapping (address => mapping(uint => bool)) public override votedNo;

    // The total number of proposals ever created
    //
    // @return The total number of proposals ever created
    //function numberOfProposals() external view returns (uint);
    uint public override numberOfProposals;

    // A string that states how one joins the DAO -- perhaps contacting the
    // deployer, perhaps some other secret means.  Make this something
    // creative!
    //
    // @return A description of what one has to do to join this DAO
    //function howToJoin() external view returns (string memory);
    //TODO -- more? actual steps?
    string constant public override howToJoin = "First off, Welcome! Be a good person and I welcome you into my DAO! Join by following the proper procedures and don't do dumb stuff! You can use our requestMembership feature or you can have an existing member add you!";

    // This is the amount of ether (in wei) that has been reserved for
    // proposals.  This is increased by the proposal amount when a new
    // proposal is created, thus "reserving" those ether from being spent on
    // another proposal while this one is still being voted upon.  If a
    // proposal succeeds, then the proposal amount is paid out.  In either
    // case, once the voting period for the proposal ends, this amount is
    // reduced by the proposal amount.
    //
    // @return The amount of ether, in wei, reserved for proposals
    //function reservedEther() external view returns (uint);
    uint public override reservedEther;

    // Who is the curator (owner / deployer) of this contract?
    //
    // @return The curator (deployer) of this contract
    //function curator() external view returns (address);
    address public override curator;

    //------------------------------------------------------------
    // Functions to implement

    // This allows the function to receive ether without having a payable
    // function -- it doesn't have to have any code in its body, but it does
    // have to be present.
    receive() external payable {
        //CHECK TODO?
        reservedEther += msg.value;
    }

    // `msg.sender` creates a proposal to send `_amount` Wei to `_recipient`
    // with the transaction data `_transactionData`.  This can only be called
    // by a member of the DAO, and should revert otherwise.
    //
    // @param recipient Address of the recipient of the proposed transaction
    // @param amount Amount of wei to be sent with the proposed transaction
    // @param description String describing the proposal
    // @param debatingPeriod Time used for debating a proposal, at least
    //        `minProposalDebatePeriod()` seconds long.  Note that the 
    //        provided parameter can *equal* the `minProposalDebatePeriod()` 
    //        as well.
    // @return The proposal ID
    function newProposal(address recipient, uint amount, string memory description, uint debatingPeriod) public override payable returns (uint) {
        //TODO -- ensure dao has enough money for this transfer

        
        require(isMember(msg.sender)==true, "You're not a member of our organization. Stop it before I call the cops");
        require(debatingPeriod >= minProposalDebatePeriod, "Not a long enough debate period. Don't try to pull any fast ones on me!");

        //TODO CHECK --- verify the dao has enough ether to pay this proposal if it passes
        //THIS IS THE BALANCE OF ACCOUNT THAT IS NOT RESERVED (RESERVED FOR OTHER PROPOSALS!
        //require(address(this).balance >= amount || msg.value >= amount || msg.value + address(this).balance >= amount);
        require(((msg.value + address(this).balance) - reservedEther) >= amount, "Send in more ether with this new proposal, dao doesnt have enough"); 
        
        //map proposal
        proposals[numberOfProposals] = Proposal(recipient, amount, description, block.timestamp + debatingPeriod, true, false, 0, 0, msg.sender);

        reservedEther += amount;

        //EMIT EVENT
        emit NewProposal(numberOfProposals, recipient, amount, description);

        numberOfProposals++;
        return numberOfProposals - 1;

    }

    // Vote on proposal `_proposalID` with `_supportsProposal`.  This can only
    // be called by a member of the DAO, and should revert otherwise.
    //
    // @param proposalID The proposal ID
    // @param supportsProposal true/false as to whether in support of the
    //        proposal
    function vote(uint proposalID, bool supportsProposal) public override {
        require(isMember(msg.sender) == true, "You are not a member so you can't vote. Do not try corrupting our democratic process!");
        require(block.timestamp < proposals[proposalID].votingDeadline, "The proposal voting is closed already");
        require(proposals[proposalID].open == true, "Proposal not open any more");

        require(votedYes[msg.sender][proposalID] == false && votedNo[msg.sender][proposalID] == false, "You have already voted on this proposal");

        if (supportsProposal == true) {
            //voted yes
            votedYes[msg.sender][proposalID] = true;
            votedNo[msg.sender][proposalID] = false;
            proposals[proposalID].yea++;
        } else {
            //voted no
            votedYes[msg.sender][proposalID] = false;
            votedNo[msg.sender][proposalID] = true;
            proposals[proposalID].nay++;
        }
        
        //emit event
        emit Voted(proposalID, supportsProposal, msg.sender);
    }

    // Checks whether proposal `_proposalID` with transaction data
    // `_transactionData` has been voted for or rejected, and transfers the
    // ETH in the case it has been voted for.  This can only be called by a
    // member of the DAO, and should revert otherwise.  It also reverts if
    // the proposal cannot be closed (time is not up, etc.).
    //
    // @param proposalID The proposal ID
    function closeProposal(uint proposalID) public override {
        require(proposalID < numberOfProposals, "That proposal does not exist yet!");
        require(block.timestamp > proposals[proposalID].votingDeadline, "not time to close it yet! More time is left to vote!");
        require(isMember(msg.sender) == true, "You are not a member. Do not try influencing the results of our voting process!");
        

        //Close it
        proposals[proposalID].open = false;

        if (proposals[proposalID].yea > proposals[proposalID].nay) {
            //it passes
            proposals[proposalID].proposalPassed = true;
            (bool success, ) = payable(proposals[proposalID].recipient).call{value: proposals[proposalID].amount}("");
            require(success, "Failed to transfer money to recipient while trying to close proposal");
        } else {
            //fails to pass
            proposals[proposalID].proposalPassed = false;

        }

        //emit event
        emit ProposalClosed(proposalID, proposals[proposalID].proposalPassed);

        //remove amount from the reservedEther
        reservedEther = reservedEther - proposals[proposalID].amount;


    }

    // Returns true if the passed address is a member of this DAO, false
    // otherwise.  This likely has to call the NFTManager, so it's not just a
    // public variable.  For this assignment, this should be callable by both
    // members and non-members.
    //
    // @param who An account address
    // @return A bool as to whether the passed address is a member of this DAO
    function isMember(address who) public override view returns (bool) {
        bool member = false;
        uint countLocal = INFTManager(tokens).count();
        for (uint i = 0; i < countLocal; i++) {
            if (INFTManager(tokens).ownerOf(i) == who){
                //they are already a member then
                member = true;
                break;
            }
        }
        return member;
    }

    function substring(string memory str, uint startIndex, uint endIndex) public pure returns (string memory) {
    bytes memory strBytes = bytes(str);
    bytes memory result = new bytes(endIndex-startIndex);
    for(uint i = startIndex; i < endIndex; i++)
        result[i-startIndex] = strBytes[i];
    return string(result);
}

    // Adds the passed member.  For this assignment, any current member of the
    // DAO can add members. Membership is indicated by an NFT token, so one
    // must be transferred to this member as part of this call.  This can only
    // be called by a member of the DAO, and should revert otherwise.
    // @param who The new member to add
    //
    // @param who An account address to have join the DAO
    function addMember(address who) public override {
        require(isMember(msg.sender) == true, "Only members can add other people!");

        require(isMember(who) == false, "That person is already a member!");

        //uint nextTokenNum = INFTManager(tokens).count();

        //INFTManager(tokens).mintWithURI(who, Strings.toString(nextTokenNum));
        string memory uri = substring(Strings.toHexString(who),2,34);

        INFTManager(tokens).mintWithURI(who, uri);

    }

    // This is how one requests to join the DAO.  Presumably they called
    // howToJoin(), and fulfilled any requirement(s) therein.  In a real
    // application, this would put them into a list for the owner(s) to
    // approve or deny.  For our uses, this will automatically allow the
    // caller (`msg.sender`) to be a member of the DAO.  This functionality
    // is for grading purposes.  This function should revert if the caller is
    // already a member.
    function requestMembership() public override {
        require(isMember(msg.sender) == false, "You are already a member!");

        //uint nextTokenNum = INFTManager(tokens).count();
        //turn it into a string, mint a new nft 
        string memory uri = substring(Strings.toHexString(msg.sender),2,34);

        //INFTManager(tokens).mintWithURI(msg.sender, Strings.toString(nextTokenNum));
        INFTManager(tokens).mintWithURI(msg.sender, uri);
    }

    // also supportsInterface() from IERC165; it should support two
    // interfaces (IERC165 and IDAO)
    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
       return interfaceId == type(IDAO).interfaceId || interfaceId == type(IERC165).interfaceId;
   }
}