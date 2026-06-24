import pytest
from qryptex.qryptex import Qryptex

SECRET_TEXTE = "Message secret super important"
PASSWORD = "MonMotDePasseSecurise123!"

def test_qryptex_encryption_decryption_cycle():
    
    # Test init :
    qryptex = Qryptex(iterations=1_000)

    # Encryption and Decryption:
    encrypted_payload = qryptex._encrypt(SECRET_TEXTE, PASSWORD)
    decrypted_text = qryptex._decrypt(encrypted_payload, PASSWORD)

    # Assertions :
    assert decrypted_text == SECRET_TEXTE
    assert encrypted_payload != SECRET_TEXTE

def test_qryptex_qr_generation_read_cycle():
     # Test init :
    qryptex = Qryptex(iterations=1_000)    
    
    # Write and Read QR:
    qryptex.write_qr(SECRET_TEXTE, PASSWORD)    
    decrypted_text = qryptex.read_qr(password=PASSWORD)
    
    # Assertions :
    assert decrypted_text == SECRET_TEXTE