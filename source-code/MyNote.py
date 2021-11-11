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

Public Repo:
    Github: https://github.com/commandantekaustav/Presidio-Cloud-Solutions-Assignment-1
"""

# Imports
from Credentials import Root as rootCreds
from mysql.connector import connect

## Setting Up
def start():
    """All that needs to be done in the begining."""
    connectDB()
    landing()

def connectDB():
    """Connects to the SQL Database"""
    global connector
    connector = connect(host=rootCreds.host, user=rootCreds.username, passwd=rootCreds.password, database="db_mynote")
    print("DATABASE IS UP.")
    global mnCursor
    mnCursor = connector.cursor()
    # mnCursor.execute('use db_mynote')

# # Gateways
def verification(umail) -> bool:
    """Checking if User account exists"""
    mnCursor.execute("select id from mynote_users")
    users = [u[0] for u in mnCursor.fetchall()]
    vfStatus = umail in users
    # print(f"{umail} Verified." if vfStatus else f"{umail} is an invalid Username")
    return vfStatus

def login(mail):
    """Log into the account with previously registered creds"""
    global loginFlag
    loginFlag = False

    print(f"Welcome back, {mail}!")
    password = input("Enter your password to log in to your account:")
    query = "SELECT passkey FROM mynote_users where id = '{}'".format(mail)
    mnCursor.execute(query)
    gotPass = mnCursor.fetchall()[0][0]
    if gotPass == password:
        loginStatusUpdateQuery = "UPDATE db_mynote.mynote_users t SET t.login_status = 1 WHERE t.id LIKE '{}' ESCAPE '#' " \
                                 "AND t.passkey LIKE '{}' ESCAPE '#' AND t.login_status = 0;".format(mail, password)
        mnCursor.execute(loginStatusUpdateQuery)
        connector.commit()
        print("Bingo! You have successfully logged in to your account!")
        loginFlag = True
    else:
        print("Wrong Password!")
        loginFlag = False

    return gotPass == password

def logout(mail):
    """Log out. Setting the active flag OFF."""
    loginStatusUpdateQuery = "UPDATE db_mynote.mynote_users t SET t.login_status = 0 " \
                             "WHERE t.id LIKE '{}' ESCAPE '#' AND t.login_status = 1;".format(mail)
    mnCursor.execute(loginStatusUpdateQuery)
    connector.commit()

    global loginFlag
    loginFlag = False
    print("Bingo! You have successfully logged out from your account!")


def register(mail):
    """Registration of new customers. Recording in DB."""
    if (verification(mail)):
        print("Account already exists.")
        landing()
    else:
        print(f"Welcome to the registration process, {mail}!")
        password = input("Enter your password:")
        query = "INSERT INTO db_mynote.mynote_users (id, passkey) VALUES ('{}', '{}')".format(mail, password)
        mnCursor.execute(query)
        connector.commit()
        print(f"User Registration is: {'Successful' if verification(mail) else 'Failed'}")

# # Menu Handling
def landing():
    """Login-Reg Page"""
    umail = input("Enter your mail id please:")
    print(f"Hello, {umail}! Welcome to MyNote.")

    if (verification(umail)):
        if (login(umail)):
            fetchMenu(umail)
        else:
            print("Passwords did not match")
            landing()

    else:
        register(umail)
        landing()

def fetchMenu(mail):
    """Menu Display and Service Invocation gateway."""

    while loginFlag:
        print("1. Create Content.\t 2. Edit Content.\t  3. Edit Label.\t    4. Edit Date.\n"
              "5. Find by Label.\t  6. Archive.\t  7. Unarchive.\t   8. Delete by ID.\n"
              "9. Show all records.\t 10. Logout.\t         0. Exit.\t")

        if loginFlag:
            print(f"{mail} \'s Dashboard:")
            uChoice = int(input("Choice: "))
            if uChoice == 1:
                Services.writeNote(mail)
            elif uChoice == 2:
                Services.editContent(mail)
            elif uChoice == 3:
                Services.editLabel(mail)
            elif uChoice == 4:
                Services.editDate(mail)
            elif uChoice == 5:
                Services.findByLabel(mail)
            elif uChoice == 6:
                Services.archiveContent(mail)
            elif uChoice == 7:
                Services.unarchiveContent(mail)
            elif uChoice == 8:
                Services.delContent(mail)
            elif uChoice == 9:
                Services.showAll(mail)
            elif uChoice == 10:
                logout(mail)
                landing()
            elif uChoice == 0:
                exit()
            else:
                print("Wrong Choice! ")
                fetchMenu(mail)



class Services:
    """List of all services provided by the note taking app."""

    def writeNote(mail):
        """Create a Note"""
        content = input("Enter your content:")
        query = "INSERT INTO db_mynote.mynote_data (id, content, label, due_date, archived) " \
                "VALUES ('{}', '{}', DEFAULT, DEFAULT, DEFAULT)".format(mail, content)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully added!")

    def editContent(mail):
        """Edit a note."""
        idx = int(input("Enter ID no of the content: "))
        content = input("Enter modified content: ")
        query = "UPDATE db_mynote.mynote_data t SET t.content = '{}' " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(content, mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully modified!")

    def archiveContent(mail):
        """Hiding contents; Default: Shown"""
        idx = int(input("Enter ID no of the content: "))
        query = "UPDATE db_mynote.mynote_data t SET t.archived = 1 " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully archived!")

    def unarchiveContent(mail):
        """Unhiding Contents"""
        idx = int(input("Enter ID no of the content: "))
        query = "UPDATE db_mynote.mynote_data t SET t.archived = 0 " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully un-archived!")

    def delContent(mail):
        """"Deleting particular contents"""
        idx = int(input("Enter ID no of the content: "))
        query = "DELETE FROM db_mynote.mynote_data " \
                "WHERE `id` = '{}' AND `index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully deleted!")

    def editLabel(mail):
        """Editing the label of a specific content"""
        idx = int(input("Enter ID no of the content: "))
        label = input("New Label: ")
        query = "UPDATE db_mynote.mynote_data t SET t.label = '{}' " \
                "WHERE `id` = '{}' AND t.`index` = {}".format(label, mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content\'s label has been successfully modified!")

    def editDate(mail):
        """Editing the date of a specific content"""
        idx = int(input("Enter ID no of the content: "))
        newDate = input("Enter new Date in the following format: YYYY-MM-DD")
        query = "UPDATE db_mynote.mynote_data t SET t.due_date = '{}' " \
                "WHERE t.`index` = {} AND t.`id` = '{}'".format(newDate, idx, mail)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content\'s date has been successfully modified!")


    def findByLabel(mail):
        """Show all contents of a specific type."""
        label = input("Label to find: ")
        query = "SELECT * FROM db_mynote.mynote_data t " \
                "WHERE t.`id` = '{}' AND t.`label` = '{}' AND t.`archived` = 0;".format(mail, label)
        mnCursor.execute(query)
        result = [x[2] for x in mnCursor.fetchall()]
        for content_i in result:
            print(content_i)

    def showAll(mail):
        """Print all the records of an User. (Which are not hiddent"""
        query = "SELECT * FROM db_mynote.mynote_data t " \
                "WHERE t.id = '{}' AND t.archived = 0".format(mail)
        mnCursor.execute(query)
        result = [x[2] for x in mnCursor.fetchall()]
        for content_i in result:
            print(content_i)

if __name__ == "__main__":
    """Main Page"""
    # Starting Appplication
    start()

    # login('asdadc@bca.com') if(verification('asdadc@bca.com')) else register('asdadc@bca.com')
    # logout('asdadc@bca.com')
    # print(verification('abc@bca.com'))
    # print(verification('asdadc@bca.com'))
    # register('asdadc@bca.com')
    # login('asdadc@bca.com')
