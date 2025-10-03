// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FIRStorage {
    struct FIRRecord {
        string caseId;
        string ipfsHash;
        uint256 timestamp;
        address officerAddress;
    }

    mapping(string => FIRRecord) public firRecords;

    event FIRStored(string caseId, string ipfsHash, address officerAddress);

    // Keep the constructor empty or simple, without any require() statements.
    constructor() {
        // No code here
    }

    function storeFIR(string memory _caseId, string memory _ipfsHash) public {
        require(bytes(_caseId).length > 0, "Case ID cannot be empty");
        require(bytes(_ipfsHash).length > 0, "IPFS hash cannot be empty");

        firRecords[_caseId] = FIRRecord({
            caseId: _caseId,
            ipfsHash: _ipfsHash,
            timestamp: block.timestamp,
            officerAddress: msg.sender
        });

        emit FIRStored(_caseId, _ipfsHash, msg.sender);
    }
    
    function getFIR(string memory _caseId) public view returns (
        string memory,
        string memory,
        uint256,
        address
    ) {
        FIRRecord storage fir = firRecords[_caseId];
        return (fir.caseId, fir.ipfsHash, fir.timestamp, fir.officerAddress);
    }
}