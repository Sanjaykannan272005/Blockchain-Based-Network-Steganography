// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SecureUserRegistry
 * @dev Smart contract for creating and managing verified secure users
 */
contract SecureUserRegistry {
    
    // Owner and admin management
    address public owner;
    mapping(address => bool) public admins;
    
    // User verification levels
    enum VerificationLevel { NONE, READ_ONLY, BASIC_SENDER, ENCRYPTED_SENDER, TRIGGER_CREATOR, FULL_ACCESS }
    
    // User structure stored on blockchain
    struct SecureUser {
        address userAddress;        // Blockchain address
        string name;               // Real name
        string organization;       // CIA, NSA, etc.
        string securityClearance;  // TOP_SECRET, SECRET, etc.
        bytes32 publicKeyHash;     // Hash of public key
        VerificationLevel level;   // Access level (0-5)
        uint256 registrationTime;  // When registered
        uint256 verificationTime;  // When verified
        address verifiedBy;        // Which admin verified
        bool isActive;            // Account status
        uint256 reputationScore;   // Trust score (0-100)
        bytes32 biometricHash;     // Biometric data hash
    }
    
    // Storage mappings
    mapping(address => SecureUser) public verifiedUsers;
    mapping(address => SecureUser) public pendingUsers;
    mapping(address => bool) public blockedUsers;
    
    // Arrays for enumeration
    address[] public verifiedUsersList;
    address[] public pendingUsersList;
    
    // Events for blockchain logging
    event UserRegistered(address indexed user, string name, string organization);
    event UserVerified(address indexed user, VerificationLevel level, address indexed verifiedBy);
    event UserBlocked(address indexed user, string reason);
    event AdminAdded(address indexed admin);
    event ReputationUpdated(address indexed user, uint256 newScore);
    
    // Access control modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyAdmin() {
        require(admins[msg.sender] || msg.sender == owner, "Only admin can call this function");
        _;
    }
    
    modifier onlyVerifiedUser() {
        require(verifiedUsers[msg.sender].isActive, "Only verified users can call this function");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        admins[msg.sender] = true;
    }
    
    /**
     * @dev Step 1: User registers themselves on blockchain
     */
    function registerUser(
        string memory _name,
        string memory _organization,
        string memory _securityClearance,
        bytes32 _publicKeyHash,
        bytes32 _biometricHash
    ) public {
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(!verifiedUsers[msg.sender].isActive, "User already verified");
        require(pendingUsers[msg.sender].registrationTime == 0, "User already pending");
        require(!blockedUsers[msg.sender], "User is blocked");
        
        // Create pending user record
        pendingUsers[msg.sender] = SecureUser({
            userAddress: msg.sender,
            name: _name,
            organization: _organization,
            securityClearance: _securityClearance,
            publicKeyHash: _publicKeyHash,
            level: VerificationLevel.NONE,
            registrationTime: block.timestamp,
            verificationTime: 0,
            verifiedBy: address(0),
            isActive: false,
            reputationScore: 100, // Start with neutral score
            biometricHash: _biometricHash
        });
        
        pendingUsersList.push(msg.sender);
        
        emit UserRegistered(msg.sender, _name, _organization);
    }
    
    /**
     * @dev Step 2: Admin verifies the user with specific access level
     */
    function verifyUser(
        address _userAddress,
        VerificationLevel _level
    ) public onlyAdmin {
        require(pendingUsers[_userAddress].registrationTime > 0, "User not found in pending list");
        require(_level != VerificationLevel.NONE, "Must assign valid verification level");
        
        // Move from pending to verified
        SecureUser memory user = pendingUsers[_userAddress];
        user.level = _level;
        user.verificationTime = block.timestamp;
        user.verifiedBy = msg.sender;
        user.isActive = true;
        
        // Store in verified users
        verifiedUsers[_userAddress] = user;
        verifiedUsersList.push(_userAddress);
        
        // Remove from pending
        delete pendingUsers[_userAddress];
        _removePendingUser(_userAddress);
        
        emit UserVerified(_userAddress, _level, msg.sender);
    }
    
    /**
     * @dev Step 3: Check user permissions for specific actions
     */
    function hasPermission(address _user, string memory _permission) public view returns (bool) {
        if (!verifiedUsers[_user].isActive || blockedUsers[_user]) {
            return false;
        }
        
        VerificationLevel level = verifiedUsers[_user].level;
        bytes32 permissionHash = keccak256(abi.encodePacked(_permission));
        
        // Define permissions by level
        if (level == VerificationLevel.READ_ONLY) {
            return permissionHash == keccak256("READ_MESSAGES");
        }
        else if (level == VerificationLevel.BASIC_SENDER) {
            return (permissionHash == keccak256("READ_MESSAGES") ||
                    permissionHash == keccak256("SEND_BASIC"));
        }
        else if (level == VerificationLevel.ENCRYPTED_SENDER) {
            return (permissionHash == keccak256("READ_MESSAGES") ||
                    permissionHash == keccak256("SEND_BASIC") ||
                    permissionHash == keccak256("SEND_ENCRYPTED"));
        }
        else if (level == VerificationLevel.TRIGGER_CREATOR) {
            return (permissionHash == keccak256("READ_MESSAGES") ||
                    permissionHash == keccak256("SEND_BASIC") ||
                    permissionHash == keccak256("SEND_ENCRYPTED") ||
                    permissionHash == keccak256("CREATE_TRIGGERS"));
        }
        else if (level == VerificationLevel.FULL_ACCESS) {
            return true; // Full access to everything
        }
        
        return false;
    }
    
    /**
     * @dev Update user reputation based on actions
     */
    function updateReputation(address _user, int256 _change) public onlyAdmin {
        require(verifiedUsers[_user].isActive, "User not verified");
        
        SecureUser storage user = verifiedUsers[_user];
        
        if (_change > 0) {
            user.reputationScore = user.reputationScore + uint256(_change);
            if (user.reputationScore > 100) {
                user.reputationScore = 100;
            }
        } else {
            uint256 decrease = uint256(-_change);
            if (user.reputationScore > decrease) {
                user.reputationScore = user.reputationScore - decrease;
            } else {
                user.reputationScore = 0;
            }
        }
        
        // Auto-block if reputation too low
        if (user.reputationScore < 30) {
            _blockUser(_user, "LOW_REPUTATION");
        }
        
        emit ReputationUpdated(_user, user.reputationScore);
    }
    
    /**
     * @dev Block a user from the system
     */
    function blockUser(address _user, string memory _reason) public onlyAdmin {
        _blockUser(_user, _reason);
    }
    
    function _blockUser(address _user, string memory _reason) internal {
        blockedUsers[_user] = true;
        if (verifiedUsers[_user].isActive) {
            verifiedUsers[_user].isActive = false;
        }
        emit UserBlocked(_user, _reason);
    }
    
    /**
     * @dev Add new admin
     */
    function addAdmin(address _admin) public onlyOwner {
        admins[_admin] = true;
        emit AdminAdded(_admin);
    }
    
    /**
     * @dev Get user information
     */
    function getUserInfo(address _user) public view returns (
        string memory name,
        string memory organization,
        VerificationLevel level,
        uint256 reputationScore,
        bool isActive
    ) {
        SecureUser memory user = verifiedUsers[_user];
        return (user.name, user.organization, user.level, user.reputationScore, user.isActive);
    }
    
    /**
     * @dev Get pending users count
     */
    function getPendingUsersCount() public view returns (uint256) {
        return pendingUsersList.length;
    }
    
    /**
     * @dev Get verified users count
     */
    function getVerifiedUsersCount() public view returns (uint256) {
        return verifiedUsersList.length;
    }
    
    /**
     * @dev Internal function to remove user from pending list
     */
    function _removePendingUser(address _user) internal {
        for (uint i = 0; i < pendingUsersList.length; i++) {
            if (pendingUsersList[i] == _user) {
                pendingUsersList[i] = pendingUsersList[pendingUsersList.length - 1];
                pendingUsersList.pop();
                break;
            }
        }
    }
    
    /**
     * @dev Emergency function to pause all operations
     */
    function emergencyPause() public onlyOwner {
        // Implementation for emergency pause
    }
}