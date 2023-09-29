// SPDX-License-Identifier: GPL-3.0-or-later
//Michael Brown (mjb4us)


pragma solidity ^0.8.17;


import "./ITokenCC.sol";
import "./ERC20.sol";
import "./IERC20Receiver.sol";


contract TokenCC is ITokenCC, ERC20 {


   constructor() ERC20("MagicToken", "MT") {
       _mint(msg.sender, 1000000 * 10**8);
   }




   function decimals() public pure override(ERC20,IERC20Metadata) returns (uint8) {
       return 8;
   }


   function requestFunds() public pure {
       revert();
   }


   function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
       return interfaceId == type(ITokenCC).interfaceId || interfaceId == type(IERC165).interfaceId ||
               interfaceId == type(IERC20).interfaceId || interfaceId == type(IERC20Metadata).interfaceId;
   }

   function _afterTokenTransfer(address from, address to, uint256 amount) internal override {
    if ( to.code.length > 0  && from != address(0) && to != address(0) ) {
        // token recipient is a contract, notify them
        try IERC20Receiver(to).onERC20Received(from, amount, address(this)) returns (bool success) {
            require(success,"ERC-20 receipt rejected by destination of transfer");
        } catch {
            // the notification failed (maybe they don't implement the `IERC20Receiver` interface?)
            // we choose to ignore this case
        }
    }
    }
}

