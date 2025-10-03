# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from db.database import add_fir_record, get_fir_by_case_id
from blockchain import store_fir_on_blockchain, get_fir_from_blockchain
from ipfs import upload_fir_to_ipfs
import os

app = FastAPI()

@app.post("/store_fir")
async def store_fir(
    case_id: str,
    officer_address: str,
    file: UploadFile = File(...)
):
    """
    Endpoint for a police officer to store an approved FIR.
    """
    # Step 1: Save the file locally to upload to IPFS
    file_path = f"temp_fir_{case_id}.pdf"
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Step 2: Upload document to IPFS
    ipfs_hash = upload_fir_to_ipfs(file_path)
    os.remove(file_path) # Clean up the temporary file
    if not ipfs_hash:
        raise HTTPException(status_code=500, detail="Failed to upload to IPFS")

    # Step 3: Store hash on the blockchain
    try:
        tx_receipt = store_fir_on_blockchain(case_id, ipfs_hash, officer_address)
        if not tx_receipt:
            raise HTTPException(status_code=500, detail="Blockchain transaction failed.")
        blockchain_tx_hash = tx_receipt.transactionHash.hex()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain transaction failed: {e}")

    # Step 4: Store metadata in MongoDB
    record = {
        "case_id": case_id,
        "ipfs_hash": ipfs_hash,
        "blockchain_tx_hash": blockchain_tx_hash,
        "officer_address": officer_address,
        "status": "Approved"
    }
    add_fir_record(record)
    
    return {"status": "success",
             "message": "FIR stored securely",
             "ipfs_hash": ipfs_hash,
             "blockchain_tx_hash": blockchain_tx_hash}

@app.get("/get_fir_status/{case_id}")
async def get_fir_status(case_id: str):
    """
    Endpoint for citizens/officers to get quick status of an FIR.
    """
    fir = get_fir_by_case_id(case_id)
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    
    return {
        "case_id": fir["case_id"],
        "status": fir["status"],
        "officer_address": fir["officer_address"]
    }

@app.get("/verify_fir/{case_id}")
async def verify_fir(case_id: str):
    """
    Endpoint to perform a full blockchain verification of an FIR.
    """
    fir_record = get_fir_by_case_id(case_id)
    if not fir_record:
        raise HTTPException(status_code=404, detail="Record not found in database")
    
    db_cid = fir_record.get("ipfs_hash")

    blockchain_record = get_fir_from_blockchain(case_id)
    if not blockchain_record:
        raise HTTPException(status_code=404, detail="Record not found on blockchain")

    blockchain_cid = blockchain_record[1]

    is_verified = db_cid == blockchain_cid
    
    return {
        "case_id": case_id,
        "db_cid": db_cid,
        "blockchain_cid": blockchain_cid,
        "verified": is_verified,
        "verification_result": "Verified" if is_verified else "Tampered"
    }