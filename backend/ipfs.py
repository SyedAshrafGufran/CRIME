# ipfs.py
import ipfshttpclient
import os

def upload_fir_to_ipfs(file_path):
    """Uploads a file to a local IPFS node and returns its CID."""
    try:
        # Check if the IPFS daemon is running
        client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
        res = client.add(file_path)
        return res['Hash']  # This is the CID (Content Identifier)
    except Exception as e:
        print(f"IPFS connection or upload failed: {e}")
        return None