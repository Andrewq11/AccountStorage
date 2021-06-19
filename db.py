from base64 import encode
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Cursor
from cryptography.fernet import Fernet


# Setting up encryption key, which is generated on account creation.
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


# Loads our stored encryption key from key.key file
def load_key():
    return open("key.key", "rb").read()


# Encrypts password using key previously generated
def encrypt_pass(password):
    key = load_key()
    # Encoding password to UTF-8 by default
    encode_pass = password.encode()
    f = Fernet(key)
    encrypt_pass = f.encrypt(encode_pass)

    return encrypt_pass


# Decrypts password for displaying to user and for user authentications
def decrypt_pass(encryptedPass):
    key = load_key()
    f = Fernet(key)
    decrypt_pass = f.decrypt(encryptedPass)
    decrypt_pass = decrypt_pass.decode()

    return decrypt_pass


# Function to delete userinfo table in database
def del_table_user():
    conn = sqlite3.connect(r"db/sqlite.db")
    curs = conn.cursor()
    curs.execute("DROP TABLE userinfo")
    conn.commit()
    conn.close()


# Function to delete accounts table in database
def del_table():
    conn = sqlite3.connect(r"db/sqlite.db")
    curs = conn.cursor()
    curs.execute("DROP TABLE accounts")
    conn.commit()
    conn.close()



# ---- RELEVANT FUNCTIONS FOR MODIFYING AND CREATING DB ---- #

# Function provides connection object to database
def create_connection(dbFile):
    conn = None
    try:
        conn = sqlite3.connect(dbFile)

    except Error as e:
        print(e)

    return conn



# Function creates a table
def create_table(conn, create_table_sq1):
    try:
        curs = conn.cursor()
        curs.execute(create_table_sq1)

    except Error as e:
        print(e)



# Used for creating new accounts table if not already exists
def create_DB():
    db = r"db/sqlite.db"
    sql_create_account_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text,
                                        platform text,
                                        type text
                                    ); """

    conn = create_connection(db)

    if conn is not None:
        create_table(conn,  sql_create_account_table)
    else:
        print("Error! Cannot create the database connection.")
    
    return conn



# Used for creating new userinfo table if not already exists
def create_DB_user():
    db = r"db/sqlite.db"
    sql_create_info_table = """ CREATE TABLE IF NOT EXISTS userinfo (
                                        id integer PRIMARY KEY,
                                        firstName text NOT NULL,
                                        password text,
                                        passHint text
                                    ); """

    conn = create_connection(db)

    if conn is not None:
        create_table(conn,  sql_create_info_table)
    else:
        print("Error! Cannot create the database connection.")
    
    return conn



# Inserts new row into the table w/ specified arguments for user, pass, plat, type
def create_account(conn, account):
    sql = ''' INSERT INTO accounts(username,password,platform,type)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, account)
    conn.commit()
    return cur.lastrowid


# Function to create now row in userinfo db
def create_account_user(conn, info):
    sql = ''' INSERT INTO userinfo(firstName,password,passHint)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, info)
    conn.commit()
    return cur.lastrowid



# Function to delete a row in the accounts db
def deleteAcc(id):
    db = r"db/sqlite.db"
    conn = create_connection(db)
    curs = conn.cursor()

    deleteRow = """DELETE from accounts where id = ?"""
    curs.execute(deleteRow, (id,))
    
    conn.commit()
    curs.close()



# Function to store an account in the accounts db
def accStore(user, password, platform, type):

    conn = create_DB()

    account = (user, password, platform, type)
    with conn:
        rowID = create_account(conn, account)



# Function to store userinfo in userinfo db
def accStore_user(firstName, password, passHint):

    conn = create_DB_user()

    account = (firstName, password, passHint)
    with conn:
        rowID = create_account_user(conn, account)



# Function gives ALL rows in accounts db for display
def selectAcc():
    db = r"db/sqlite.db"
    conn = create_connection(db)

    curs = conn.cursor()
    curs.execute("SELECT * FROM accounts")

    rows = curs.fetchall()
    
    curs.close()
    
    return rows


# Return row from userinfo db, should be only 1
def selectAcc_user():
    db = r"db/sqlite.db"
    conn = create_connection(db)

    curs = conn.cursor()
    curs.execute("SELECT * FROM userinfo")

    rows = curs.fetchall()
    curs.close()

    return rows








