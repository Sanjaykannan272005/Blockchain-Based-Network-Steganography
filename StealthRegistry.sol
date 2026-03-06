// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StealthRegistry {
    enum NetworkStatus { NORMAL, SILENCED }
    NetworkStatus public currentStatus = NetworkStatus.NORMAL;
    address public owner;

    struct Node {
        address wallet;
        string ip;
        string[] channels;
        string publicKey;
        uint256 lastSeen;
        
        bool isActive;
        uint256 reputation; // 0-100
    }

    mapping(address => Node) public nodes;
    address[] public nodeAddresses;
    
    event NodeRegistered(address indexed wallet, string ip);
    event NodeDeRegistered(address indexed wallet);
    event StatusChanged(NetworkStatus newStatus);
    event ReputationUpdated(address indexed node, uint256 newReputation);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function toggleEmergencyStatus() public onlyOwner {
        if (currentStatus == NetworkStatus.NORMAL) {
            currentStatus = NetworkStatus.SILENCED;
        } else {
            currentStatus = NetworkStatus.NORMAL;
        }
        emit StatusChanged(currentStatus);
    }

    function registerNode(string memory _ip, string[] memory _channels, string memory _publicKey) public {
        if (!nodes[msg.sender].isActive) {
            nodeAddresses.push(msg.sender);
        }
        
        nodes[msg.sender] = Node({
            wallet: msg.sender,
            ip: _ip,
            channels: _channels,
            publicKey: _publicKey,
            lastSeen: block.timestamp,
            isActive: true,
            reputation: 100 // Default to max reputation
        });
        
        emit NodeRegistered(msg.sender, _ip);
    }

    function reportNodeFailure(address _node) public {
        require(nodes[_node].isActive, "Node not active");
        if (nodes[_node].reputation >= 10) {
            nodes[_node].reputation -= 10;
        } else {
            nodes[_node].reputation = 0;
            nodes[_node].isActive = false; // Auto-deactivate bad nodes
        }
        emit ReputationUpdated(_node, nodes[_node].reputation);
    }

    function deRegisterNode() public {
        require(nodes[msg.sender].isActive, "Node not registered");
        nodes[msg.sender].isActive = false;
        emit NodeDeRegistered(msg.sender);
    }

    function getAllNodes() public view returns (Node[] memory) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < nodeAddresses.length; i++) {
            if (nodes[nodeAddresses[i]].isActive) {
                activeCount++;
            }
        }

        Node[] memory activeNodes = new Node[](activeCount);
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < nodeAddresses.length; i++) {
            if (nodes[nodeAddresses[i]].isActive) {
                activeNodes[currentIndex] = nodes[nodeAddresses[i]];
                currentIndex++;
            }
        }
        
        return activeNodes;
    }
}
