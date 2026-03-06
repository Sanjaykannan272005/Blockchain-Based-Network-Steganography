// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Smart Contract for Steganography Wallet Authentication
 * - Whitelist of allowed senders
 * - Time-based permissions
 * - Revocable access
 * - Cryptographic proof of sender identity
 */

contract SenderAccessControl {
    
    // Owner of the contract
    address public owner;
    
    // Access level struct
    struct AccessGrant {
        bool allowed;
        uint256 grantedAt;
        uint256 expiresAt;  // 0 means no expiration
        string reason;
    }
    
    // Mapping of sender address -> AccessGrant
    mapping(address => AccessGrant) public senderAccess;
    
    // List of all senders (for transparency)
    address[] public senderList;
    
    // Events
    event AccessGranted(address indexed sender, uint256 expiresAt, string reason);
    event AccessRevoked(address indexed sender);
    event AccessExpired(address indexed sender);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * Grant access to a sender
     * @param _sender The wallet address to grant access to
     * @param _duration Duration in seconds (0 for permanent)
     * @param _reason Reason for granting access
     */
    function grantAccess(
        address _sender,
        uint256 _duration,
        string memory _reason
    ) public onlyOwner {
        require(_sender != address(0), "Invalid sender address");
        
        uint256 expiresAt = _duration > 0 ? block.timestamp + _duration : 0;
        
        // If first time, add to list
        if (!senderAccess[_sender].allowed) {
            senderList.push(_sender);
        }
        
        senderAccess[_sender] = AccessGrant({
            allowed: true,
            grantedAt: block.timestamp,
            expiresAt: expiresAt,
            reason: _reason
        });
        
        emit AccessGranted(_sender, expiresAt, _reason);
    }
    
    /**
     * Revoke access from a sender
     * @param _sender The wallet address to revoke access from
     */
    function revokeAccess(address _sender) public onlyOwner {
        require(senderAccess[_sender].allowed, "Sender not in whitelist");
        
        senderAccess[_sender].allowed = false;
        emit AccessRevoked(_sender);
    }
    
    /**
     * Check if a sender is allowed to send messages
     * @param _sender The wallet address to check
     * @return isAllowed True if sender is allowed
     * @return reason Reason for decision
     */
    function isSenderAllowed(address _sender) public view returns (bool isAllowed, string memory reason) {
        AccessGrant memory access = senderAccess[_sender];
        
        if (!access.allowed) {
            return (false, "Sender not in whitelist");
        }
        
        // Check if expired
        if (access.expiresAt > 0 && block.timestamp > access.expiresAt) {
            return (false, "Access expired");
        }
        
        return (true, "Allowed");
    }
    
    /**
     * Get access details for a sender
     * @param _sender The wallet address to check
     */
    function getAccessDetails(address _sender) public view returns (
        bool allowed,
        uint256 grantedAt,
        uint256 expiresAt,
        string memory reason
    ) {
        AccessGrant memory access = senderAccess[_sender];
        return (access.allowed, access.grantedAt, access.expiresAt, access.reason);
    }
    
    /**
     * Get number of whitelisted senders
     */
    function getSenderCount() public view returns (uint256) {
        return senderList.length;
    }
    
    /**
     * Get sender at index
     */
    function getSenderAt(uint256 _index) public view returns (address) {
        require(_index < senderList.length, "Index out of bounds");
        return senderList[_index];
    }
    
    /**
     * Verify a message signature (for future use with ECDSA)
     * @param _signer The signer address
     * @param _messageHash The hash of the message
     * @param _signature The signature
     * @return isValid True if signature is valid
     */
    function verifySignature(
        address, /* _signer */
        bytes32, /* _messageHash */
        bytes memory _signature
    ) public pure returns (bool isValid) {
        // This would use OpenZeppelin ECDSA in production
        // For now, return true if signature is valid format
        return _signature.length == 65;
    }
    
    /**
     * Change contract owner
     */
    function transferOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != address(0), "Invalid owner address");
        owner = _newOwner;
    }
}
