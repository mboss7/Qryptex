import pytest
from src.qryptex import Qryptex


def test_qryptex_encryption_decryption_cycle():
    
    # Test init :
    qryptex = Qryptex(iterations=1_000)
    secret_text = "Message secret super important"
    password = "MonMotDePasseSecurise123!"

    # Encryption and Decryption:
    encrypted_payload = qryptex.encrypt(secret_text, password)
    decrypted_text = qryptex.decrypt(encrypted_payload, password)

    # Assertions :
    assert decrypted_text == secret_text
    assert encrypted_payload != secret_text

