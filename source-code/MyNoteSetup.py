"""
Initial Setup for MyNote
------------------------
Prerequisites:
    1) MySQL Workbench 8
    2) MySQL Connector (Python)

The Following Tasks will be performed:
    1) Creation of Database
    2) Server Connection

Naming Conventions:
    1) Classes in Camel
    2) Methods and Variables in Hungarian
    3)
    4)
"""
"""
Selfcheck:
* SQL is not case sensitive. That's why the Else block was executed.

?) How to handle the exceptions here
"""

from mysql.connector import connect
from Credentials import Root as rootCreds

myDB = connect(host=rootCreds.host, user=rootCreds.username, passwd=rootCreds.password, database="db_mynote")
print("Database has been successfully connected ")

# creating a cursor object
myCursor = myDB.cursor()

"""     
        # myCursor.execute("show databases")
        # currentDBs = [i[0] for i in myCursor.fetchall()]
        # print(currentDBs)
        # dbReady = 'db_mynote' in currentDBs
        # 
        # # Database Connection Check
        # if  dbReady:
        #     print("Database Exists.")
        # 
        # else:
        #     print("Creating Database...")
        #     myCursor.execute("CREATE DATABASE db_mynote")
        #     print("Database created.")
        # 
        # myDB = connect(host=rootCreds.host, user=rootCreds.username, passwd=rootCreds.password, database="db_mynote")
        # myCursor.execute("USE db_mynote")
        # print("Database Connected.")
"""

"""Default Table Creation"""
# myCursor.execute("create table mynote_users (id VARCHAR(50), passkey VARCHAR(50))")

# myCursor.execute("use db_mynote")
myCursor.execute("show tables;")
print(myCursor.fetchall())