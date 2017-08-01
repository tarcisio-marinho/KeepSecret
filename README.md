# KeepSecret
This tool help you to keep your files secret with AES-256-CBC.


# Download:
https://sourceforge.net/projects/keepsecret/files/ks/download


# Installation:
    sudo cp ks /usr/bin/ks


# Sintaxe:
    usage: ks [-h] [-e] [-D] [-f] [-d] [-p]

    KeepSecret is a tool to cryptograph your files

    optional arguments:
    -h, --help show this help message and exit

    -e, --encrypt File to be Encrypted/Decrypted

    -D, --decrypt File to be Encrypted/Decrypted

    -f , --file File to be Encrypted/Decrypted

    -d , --directory All files inside this Directory will be
    Encrypted/Decrypted

    -p , --password Password to Encrypt/Decrypt file




# Examples:


    ks -p PASSWORD -f PATH -e

    ks -p PASSWORD -f PATH -D
    
    ks -p PASSWORD -d ~/Desktop/teste/ -e 
    
    ks -p PASSWORD -f ~/Desktop/teste/simple_file.txt -e
    
    ks -p PASSWORD -f ~/Desktop/teste/simple_file.txt.ks -D
    
