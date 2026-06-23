import base64
import os
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Qryptex: 
    def __init__ (self, iterations: int = 100_000): 
        self.iterations = iterations
        
    def encrypt(self, data: str, password: str) -> str:
        salt = os.urandom(16)   # CSPRNG
        nonce = os.urandom(12)  # GCM (96 bits)
        
        # Key derivation (KDF) - 32 Bytes Key (256 bits)
        key = pbkdf2_hmac('sha256', password.encode(), salt, self.iterations, 32)
        
        # Encryption
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)
        
        # Create payload: Salt + Nonce + Ciphertext
        payload = salt + nonce + ciphertext
        
        # Encoding base64 for QR Code
        return base64.b64encode(payload).decode('utf-8')
    
    def decrypt(self, base64_data: str, password: str) -> str:
        # Base64 decoding
        payload = base64.b64decode(base64_data)
        
        if len(payload) < 28: # 16 (salt) + 12 (nonce)
            raise ValueError("Payload incomplete or corrupted !")
            
        salt = payload[:16]
        nonce = payload[16:28]
        ciphertext = payload[28:]
        
        key = pbkdf2_hmac('sha256', password.encode(), salt, self.iterations, 32)
        
        # Decryption
        aesgcm = AESGCM(key)
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        
        return decrypted_bytes.decode('utf-8')
        
    def generate_qr(self):
        pass
    
    def read_qr(self):
        pass
        
    def generate_pdf(self):
        pass