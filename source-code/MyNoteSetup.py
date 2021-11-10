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


from mysql.connector import connect
from Credentials import Root as rootCreds

myServer = connect(host=rootCreds.host, user=rootCreds.username, passwd=rootCreds.password)
print("Server has been successfully connected ")


myCursor = myServer.cursor()
myCursor.execute("show databases")
currentDBs = [i[0] for i in myCursor.fetchall()]
print(currentDBs)
dbReady = 'db_mynote' in currentDBs

if  dbReady:
    print("Connection has been Established")
else:
    print("Creating Database...")
    myCursor.execute("CREATE DATABASE DB_MyNote")





"""
Selfcheck:
* SQL is not case sensitive. That's why the Else block was executed.

?) How to handle the exceptions here
"""