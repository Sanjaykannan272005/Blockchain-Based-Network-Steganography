// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DeadDrop
 * @dev Secure, asynchronous messaging via blockchain
 */
contract DeadDrop {
    
    struct Message {
        address sender;
        string encryptedContent;
        uint256 timestamp;
        uint256 releaseTime;
    }
    
    // Mapping: Recipient Address -> List of Messages
    mapping(address => Message[]) private inbox;
    
    event MessageSent(address indexed sender, address indexed recipient, uint256 timestamp, uint256 releaseTime);
    
    /**
     * @dev Send an encrypted message to a recipient
     * @param _recipient The wallet address of the receiver
     * @param _encryptedContent The encrypted message string (AES/RSA)
     * @param _releaseTime The unix timestamp when the message becomes readable
     */
    function sendMessage(address _recipient, string memory _encryptedContent, uint256 _releaseTime) public {
        require(_recipient != address(0), "Invalid recipient");
        require(bytes(_encryptedContent).length > 0, "Message cannot be empty");
        
        inbox[_recipient].push(Message({
            sender: msg.sender,
            encryptedContent: _encryptedContent,
            timestamp: block.timestamp,
            releaseTime: _releaseTime
        }));
        
        emit MessageSent(msg.sender, _recipient, block.timestamp, _releaseTime);
    }
    
    /**
     * @dev Retrieve all messages for the caller
     * @return contents Array of encrypted message strings
     * @return senders Array of sender addresses
     * @return timestamps Array of timestamps
     * @return releaseTimes Array of release timestamps
     */
    function getMyMessages() public view returns (
        string[] memory contents,
        address[] memory senders,
        uint256[] memory timestamps,
        uint256[] memory releaseTimes
    ) {
        uint256 count = inbox[msg.sender].length;
        
        contents = new string[](count);
        senders = new address[](count);
        timestamps = new uint256[](count);
        releaseTimes = new uint256[](count);
        
        for (uint256 i = 0; i < count; i++) {
            Message memory msgData = inbox[msg.sender][i];
            
            // If the message is still locked, we return an empty string/placeholder
            if (block.timestamp >= msgData.releaseTime) {
                contents[i] = msgData.encryptedContent;
            } else {
                contents[i] = "[LOCKED]";
            }
            
            senders[i] = msgData.sender;
            timestamps[i] = msgData.timestamp;
            releaseTimes[i] = msgData.releaseTime;
        }
        
        return (contents, senders, timestamps, releaseTimes);
    }
    
    /**
     * @dev Get the number of messages in my inbox
     */
    function getMessageCount() public view returns (uint256) {
        return inbox[msg.sender].length;
    }
}
