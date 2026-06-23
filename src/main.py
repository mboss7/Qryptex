import argparse
import textwrap

BANNER = r"""

  ____  _____   __     _______ _______ ______  __   __ 
 / __ \|  __ \  \ \   / /  __ \__   __|  ____| \ \ / / 
| |  | | |__) |  \ \_/ /| |__) | | |  | |__     \ V /  
| |  | |  _  /    \   / |  ___/  | |  |  __|     > <   
| |__| | | \ \     | |  | |      | |  | |____   / . \  
 \___\_\_|  \_\    |_|  |_|      |_|  |______| /_/ \_\ 
=======================================================

Welcom in Qryptex by mboss7

repos: https://github.com/mboss7/Qryptex

=======================================================

    Qryptex – Securely encrypt your recovery codes 
              and text into encrypted QR codes.
              
=======================================================
"""

def main(args):
    
    print(BANNER)
    
    if args.file == None:
        args.file = input("Please enter file path: ")

    print("The selected path is: ", args.file)   

    if args.encrypt is False and args.decrypt is False:
        mode_choice = input("Please select the mode, encrypt (default enter) or decrypt (d):")
        if mode_choice == 'd':
            args.decrypt = True
        else:
            args.encrypt = True
     
    # Enter encrypt mode     
    if args.encrypt:        
        print(r"""
=======================================================

    Qryptex – Encryption mode : 
              
=======================================================
""")        
        if args.secret is None: 
            args.secret = input("Please enter secret to encrypt: ") 
            
        """
        ADD MAIN ENCRYPT FONCTION TODO 
        """
            
        
    # Enter decrypt mode
    elif args.decrypt: 
        print(r"""
=======================================================

    Qryptex – Decryption mode : 
              
=======================================================
""")
        
        """
        ADD MAIN DECRYPT FONCTION TODO 
        """
       
    # ERROR
    else: 
        print("ERROR NO ACTION SELECTED")
    
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Qryptex – Securely encrypt your recovery codes and text into encrypted QR codes.",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-e', '--encrypt', action='store_true', help="encrypt plain text to Qryptex")
    parser.add_argument('-d', '--decrypt', action='store_true', help="decypt Qryptex to plain text")
    parser.add_argument('-f', '--file', help="path to the input or output file")    
    parser.add_argument('-s', '--secret', help="secret to crypt from plain text to Qryptex")
     
    args = parser.parse_args()
    
    main(args)