import argparse
import sys
import os
import getpass
from qryptex import Qryptex

BANNER = r"""

  ____  _____   __     _______ _______ ______  __   __ 
 / __ \|  __ \  \ \   / /  __ \__   __|  ____| \ \ / / 
| |  | | |__) |  \ \_/ /| |__) | | |  | |__     \ V /  
| |  | |  _  /    \   / |  ___/  | |  |  __|     > <   
| |__| | | \ \     | |  | |      | |  | |____   / . \  
 \___\_\_|  \_\    |_|  |_|      |_|  |______| /_/ \_\ 
=======================================================

Welcome in Qryptex by mboss7

repos: https://github.com/mboss7/Qryptex

=======================================================

    Qryptex – Securely encrypt your recovery codes 
              and text into encrypted QR codes.
              
=======================================================
"""

ENCRYPT_MODE = r"""
=======================================================

    Qryptex – Encryption mode : 
              
=======================================================
"""

DECRYPT_MODE = r"""
=======================================================

    Qryptex – Decryption mode : 
              
=======================================================
"""

def main():
    parser = argparse.ArgumentParser(
        description="Qryptex – Securely encrypt your recovery codes and text into encrypted QR codes.",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-e', '--encrypt', action='store_true', help="encrypt plain text to Qryptex")
    parser.add_argument('-d', '--decrypt', action='store_true', help="decypt Qryptex to plain text")
    parser.add_argument('-f', '--file', help="path to the input or output file")    
    parser.add_argument('-s', '--secret', help="secret to crypt from plain text to Qryptex")
    parser.add_argument('-a', '--api',action='store_true', help="run api web app")
    
    args = parser.parse_args()
    

    qryptex = Qryptex(iterations=100_000) 

    if args.api:
        qryptex.q_api()
        
    
    
    print(BANNER)
    
    
    if args.file is None:
        args.file = os.getcwd()

    print("The selected path is: ", args.file)   

    if args.encrypt is False and args.decrypt is False:
        mode_choice = input("Please select the mode, encrypt (default enter) or decrypt (d):")
        if mode_choice == 'd':
            args.decrypt = True
        else:
            args.encrypt = True
     

    
    # ==================== ENCRYPTION MODE ====================    
    # Enter encrypt mode     
    if args.encrypt:        
        print(ENCRYPT_MODE)        
        if args.secret is None: 
            args.secret = input("Please enter secret to encrypt: ") 
            if not args.secret:
                print("Error: Secret text cannot be empty.")
                sys.exit(1)
        
        password = getpass.getpass("Set encryption password: ")

        try:
            print("Encrypting data...")
            qryptex.write_qr(args.secret, password)

            print(f"Success! Encrypted payload ready for QR Code (Saved to {args.file}).")
            
        except Exception as e:
            print(f"Encryption failed: {e}")
            sys.exit(1)                     
            
    # ==================== DECRYPTION MODE ====================           
    # Enter decrypt mode
    elif args.decrypt: 
        print(DECRYPT_MODE)
        password = getpass.getpass("Enter decryption password: ")

        try:
            print("Reading and decrypting...")            
            decrypted_text = qryptex.read_qr(password=password)
            
            print("DECRYPTED DATA:")
            print(decrypted_text)
            
        except ValueError:
            print("Decryption failed: Invalid password or corrupted QR Code data.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)        

    # ERROR
    else: 
        print("ERROR NO ACTION SELECTED")
                
if __name__ == '__main__':
   main()
