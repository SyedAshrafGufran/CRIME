🔒 Criminal Record Management System (CRMS) 
============================================

This project implements a secure, hybrid record management system using **FastAPI (Python)** for logic, **MongoDB** for fast queries, **IPFS** for decentralized file storage, and **Ethereum/Ganache** for immutable data verification.

This guide covers setting up the core environment and running the backend API.

🏗️ Project Structure
---------------------

The project uses a standard separation for modularity and maintainability:

*   **backend/**: Contains the FastAPI application, API endpoints, and Python business logic.
    
    *   Key files: main.py, blockchain.py, ipfs.py, db/database.py.
        
*   **blockchain-project/**: Contains the Solidity smart contract and deployment artifacts.
    
    *   Key files: truffle-config.js, contracts/FIRStorage.sol, build/contracts/FIRStorage.json.
        

⚙️ Initial Environment Setup (First Time Only)
----------------------------------------------

### 1\. Install Global Tools

You must install **Node.js** (includes npm), **Python (3.8+),** **Ganache**, and **IPFS** on your system.

Tool

Purpose

Key Action

**Node.js/npm**

Dependency Management

Install from nodejs.org

**Truffle**

Contract Compilation/Deployment

npm install -g truffle

**Ganache**

Local Ethereum Blockchain

Install Ganache

**IPFS Daemon**

Decentralized File Storage

Install **go-ipfs v0.7.0** binary (critical for Python compatibility)

### 2\. Install Python Dependencies

Navigate to the **backend** directory and install all required Python packages.

`   cd backend  pip install -r requirements.txt   `


🚀 Step-by-Step Backend Startup
-------------------------------

You must execute the following steps in sequence every time you want to run the full system. **Failure in Phase 1 will cause the FastAPI server to crash.**

### Phase 1: Blockchain and IPFS Setup

**1\. Start the Ganache Blockchain**This runs the local Ethereum network. **Do this first.**

**2\. Deploy the Smart Contract (Critical Step)**This command compiles and deploys your contract, filling the empty networks section of FIRStorage.json with the deployed address.

Directory

Command

**blockchain-project/**

truffle migrate --network development --reset

**3\. Start the IPFS Daemon**This starts the local IPFS node, listening on port 5001.

> **ACTION:** Navigate to the folder containing your **ipfs.exe** (v0.7.0) executable and run: ipfs daemon.

### Phase 2: FastAPI and Database Connection

**4\. Start the FastAPI Server**This launches the backend API, connecting to all external services (Ganache, MongoDB, IPFS).

Directory

**backend/**


Command
uvicorn main:app --reload


🧪 Testing the API Functionality
--------------------------------

Access the interactive API documentation (Swagger UI) in your browser:

http://127.0.0.1:8000/docs
