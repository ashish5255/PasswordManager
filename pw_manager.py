from cryptography.fernet import Fernet

# Function to load the key from a file or generate a new one if not found
def load_or_generate_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# Function to encrypt data using Fernet encryption
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Function to decrypt data using Fernet encryption
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Function to set up the master password
def setup_master_password():
    global mp
    key = load_or_generate_key()
    try:
        with open("master_password.txt", "rb") as file:
            encrypted_mp = file.read()
            mp = decrypt_data(encrypted_mp, key)
    except FileNotFoundError:
        mp = input("Set up the master password:")
        encrypted_mp = encrypt_data(mp, key)
        with open("master_password.txt", "wb") as file:
            file.write(encrypted_mp)

# Call the function to set up the master password
setup_master_password()

master_password = input("Enter the master password:")
if master_password == mp:
    key = load_or_generate_key() 
    fer = Fernet(key)

    def view():
        with open('passwords.txt', 'r') as f:
            for line in f:
                site, email, password = line.strip().split('|')
                print("site/app:", site, " Email:", email, " Password:", fer.decrypt(password.encode()).decode())

    def add():
        name = input ("Website/App:")
        email = input("Account Email:")
        password = input("Account Password:")
        with open('passwords.txt', 'a') as f:
            f.write(name + "|"+ email + "|"+ fer.encrypt(password.encode()).decode() + "\n")
        

    while True:
        mode = input("Enter 'add' to add a password or 'view' to view the password, press 'q' to quit:")

        if mode == 'q':
            quit()

        if mode == 'add':
            add()
        
        elif mode == 'view':
            view()
        
        else:
            continue

else:
    quit()
