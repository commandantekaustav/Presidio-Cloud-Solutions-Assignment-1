from Credentials import Root as rootCreds
from mysql.connector import connect


def start():
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


def verification(umail) -> bool:
    """Checking if User account exists"""
    mnCursor.execute("select id from mynote_users")
    users = [u[0] for u in mnCursor.fetchall()]
    vfStatus = umail in users
    print(f"{umail} Verified." if vfStatus else f"{umail} is a new User")
    return vfStatus


def login(mail):
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
    loginStatusUpdateQuery = "UPDATE db_mynote.mynote_users t SET t.login_status = 0 WHERE t.id LIKE '{}' ESCAPE '#' AND t.login_status = 1;".format(
        mail)
    mnCursor.execute(loginStatusUpdateQuery)
    connector.commit()
    loginFlag = False
    print("Bingo! You have successfully logged out from your account!")


def register(mail):
    print(f"Welcome to the registration process, {mail}!")
    password = input("Enter your password:")
    query = "INSERT INTO db_mynote.mynote_users (id, passkey) VALUES ('{}', '{}')".format(mail, password)
    mnCursor.execute(query)
    connector.commit()
    print(f"User Registration is: {'Successful' if verification(mail) else 'Failed'}")


def landing():
    umail = input("Enter your mail id please:")
    print(f"Hello, {umail}! Welcome to MyNote.")

    if (verification(umail)):
        if (login(umail)):
            fetchMenu(umail)
        else:
            uChoice = int(input("Passwords did not match.\nPress 1 for Landing Page.. \n "
                                "Press any other number for Registration."))
            landing(umail) if (uChoice == 1) else register(umail)

    else:
        register(umail)
        landing(umail)


def fetchMenu(mail):
    """Menu Display and Service Invocation gateway."""
    opt = {1: Services.writeNote(mail), 0: exit()}
    while (True):
        if (loginFlag):
            print(f"{mail} \'s Dashboard:")
            uChoice = input("1. Create Content.\n"
                            "2. Edit Content.\n"
                            "3. Edit Label.\n"
                            "4. Edit Date.\n"
                            "5. Find by Label.\n"
                            "6. Show All.\n"
                            "7. Archive.\n"
                            "8. Delete by ID.\n"
                            "9. Logout.\n"
                            "0. Exit.\n")
            if (uChoice in opt.keys()):
                opt[uChoice]


class Services:
    def writeNote(mail):
        content = input("Enter your content:")
        query = "INSERT INTO db_mynote.mynote_data (id, content, label, due_date, archived) " \
                "VALUES ('{}', '{}', DEFAULT, DEFAULT, DEFAULT)".format(mail, content)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully added!")

    def editContent(mail):
        idx = int(input("Enter ID no of the content: "))
        content = input("Enter modified content: ")
        query = "UPDATE db_mynote.mynote_data t SET t.content = '{}' " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(content, mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully modified!")

    def archiveContent(mail):
        idx = int(input("Enter ID no of the content: "))
        query = "UPDATE db_mynote.mynote_data t SET t.archived = 1 " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully archived!")

    def unarchiveContent(mail):
        idx = int(input("Enter ID no of the content: "))
        query = "UPDATE db_mynote.mynote_data t SET t.archived = 0 " \
                "WHERE t.`id` = '{}' AND t.`index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully un-archived!")

    def delContent(mail):
        idx = int(input("Enter ID no of the content: "))
        query = "DELETE FROM db_mynote.mynote_data " \
                "WHERE `id` = '{}' AND `index` = {}".format(mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content has been successfully deleted!")

    def editLabel(mail):
        idx = int(input("Enter ID no of the content: "))
        label = input("New Label: ")
        query = "UPDATE db_mynote.mynote_data t SET t.label = '{}' " \
                "WHERE `id` = '{}' AND t.`index` = {}".format(label, mail, idx)
        mnCursor.execute(query)
        connector.commit()
        print(f"Hello, {mail}. Your content\'s label has been successfully modified!")

    def editDate(mail):
        pass


if __name__ == "__main__":
    """Landing Page"""
    # Starting Appplication
    start()

    # login('asdadc@bca.com') if(verification('asdadc@bca.com')) else register('asdadc@bca.com')
    # logout('asdadc@bca.com')
    # print(verification('abc@bca.com'))
    # print(verification('asdadc@bca.com'))
    # register('asdadc@bca.com')
    # login('asdadc@bca.com')
