// SPDX-License-Identifier: GPL-3.0-or-later
//Michael Brown (mjb4us)


pragma solidity ^0.8.17;

import "./INFTManager.sol";
import "./ERC721.sol";
import "./Strings.sol";

contract NFTManager is INFTManager, ERC721 {

   constructor() ERC721("MikeNFTManager", "MNM") {
       
   }

   mapping (uint => string) public tokenUrlMap;

   uint public override count; //got rid of view keyword... is this right?


   function mintWithURI(address _to, string memory _uri) public override returns (uint) {
      //require(_to == msg.sender, "new NFT owner is not the sender...");

      require(!Strings.equal(_uri, ""), "don't try making an empty string token...");

      //check if duplicate
      for (uint i = 0; i < count; i++) {
         //compare to each uri
         require(!Strings.equal(tokenUrlMap[i], _uri), "Duplicate! Do not ever try sending a duplicate to mint again CHEATER!");
      }

      

      _mint(_to, count);



      
      tokenUrlMap[count] = _uri;

      count++;

      return count - 1;
   }

   function mintWithURI(string memory _uri) external returns (uint) {
      return mintWithURI(msg.sender, _uri);


   }


   function _baseURI() internal override(ERC721) pure returns (string memory) {
      return "https://andromeda.cs.virginia.edu/ccc/ipfs/files/";
   }


   function tokenURI(uint256 tokenId) public override(ERC721, IERC721Metadata) view returns (string memory) {
      require(tokenId >= 0 && tokenId < count, "invalid token id!");

      return string.concat(_baseURI(), tokenUrlMap[tokenId]);
   }


    function supportsInterface(bytes4 interfaceId) public override(IERC165,ERC721) pure returns (bool) {
       return interfaceId == type(IERC165).interfaceId || interfaceId == type(INFTManager).interfaceId ||
               interfaceId == type(IERC721).interfaceId || interfaceId == type(IERC721Metadata).interfaceId;
   }
}