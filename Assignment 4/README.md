##CS641A Assignment 4
###Team Name: Cryptophile

Steps to run `break_DES.py`:
1. Install `sshpass` on the commandline (for Ubuntu: run `sudo apt-get install sshpass`).
2. Ensure `break_DES.py`, `DES.py` and `generate_text.py` are in the same directory.
3. Ensure you're on the IITK network (use VPN) for successfully logging in to the server.
4. Run `python break_DES.py`. (Tested on Python 3.10.2)
5. It will generate 6 files:
    - `input.txt`
    - `output.txt`
    - `plain_text.txt`
    - `plain_text1.txt`
    - `cipher_text.txt`
    - `cipher_text2.txt`
    And will print the rest of the output on STDOUT.
