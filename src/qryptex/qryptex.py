import base64
import os
import qrcode
import io
import sys
import uvicorn
from PIL import Image
from pypdf import PdfReader
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pyzbar.pyzbar import decode
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

class Qryptex:   
    
    def __init__(self, iterations: int = 100_000, temp_path: str = r".\qryptex"): 
        self.iterations = iterations
        self.temp_path = temp_path + ".png"
        self.pdf_path = temp_path + ".pdf"
        
    def __repr__(self):
        return '{self.__class__.__name__}(iterations: {self.iterations}, temp_path: {self.temp_path}, pdf_path: {self.pdf_path})'.format(self=self)


    def q_api(self):
        """
        Run Qryptex FastAPI app 
        """


        app = FastAPI()

        @app.get("/")
        def read_root():
            return r"Welcome to Qryptex API !"
        
        @app.get("/crypt/")
        def crypt(secret: str = Query(..., description="text to crypt"),
                   password: str = Query(..., description= "password")):
            encrypted_base64 = self._encrypt(secret, password)
            return {"encrypted": encrypted_base64}

        @app.get("/generate")
        def generate_qr(secret: str = Query(..., description="text to crypt"),
                   password: str = Query(..., description= "password")):
            self.write_qr(secret, password)
    
            if not os.path.exists(self.pdf_path):
                return {"error": "pdf not found"}
        
            return FileResponse(
                path=self.pdf_path,
                media_type="application/pdf",
                filename="generated_qr.pdf"
        )

        uvicorn.run(app, host="0.0.0.0", port=8000)


    def write_qr(self, secret_to_crypt, password, pdf_path = None):
        
        """
        generate qr with secret and password"
        """
        encrypted_base64 = self._encrypt(secret_to_crypt, password)
        self._generate_qr(encrypted_base64)
    
    def read_qr(self, password, pdf_path = None):
        
        """
        read qr with password and qr path
        """
        if pdf_path is None:
            pdf_path = self.pdf_path
            
        reader = PdfReader(pdf_path)
        valeur_decodee = None

        for num_page, page in enumerate(reader.pages, start=1):
            if not page.images:
                continue

            for image_fichier in page.images:
                try:
                    image_bytes = image_fichier.data
                    pil_img = Image.open(io.BytesIO(image_bytes))
                    
                    # Détection directe avec pyzbar
                    decoded_objects = decode(pil_img)
                    if decoded_objects:
                        valeur_decodee = decoded_objects[0].data.decode('utf-8')
                        break # QR trouvé, arrêt de la boucle image
                except Exception as e:
                    print(f"Read QR in pdf failed: {e}")
                    sys.exit(1)
            
            if valeur_decodee:
                break # QR trouvé, arrêt de la boucle page

        if not valeur_decodee:
            raise ValueError("Aucun QR code valide n'a été trouvé dans le PDF.")
                    
                    
                    
        return self._decrypt(valeur_decodee, password)
        
    def _encrypt(self, data: str, password: str) -> str:
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
        encrypted_base64 = base64.b64encode(payload).decode('utf-8')
        
        # Generate QR pdf 
        self._generate_qr(encrypted_base64)
        
        print("Encypted text: ",encrypted_base64)
        return encrypted_base64
                  
    def _decrypt(self, base64_data: str, password: str) -> str:
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
        
    def _generate_qr(self, qr_content):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr.save(self.temp_path)
        self._generate_pdf()
    
    def _generate_pdf(self):         
        c = canvas.Canvas(self.pdf_path, pagesize=A4)   
        c.drawImage(self.temp_path, 147, 271, width=300, height=300)
        c.showPage()
        c.save()
        os.remove(self.temp_path)
    
