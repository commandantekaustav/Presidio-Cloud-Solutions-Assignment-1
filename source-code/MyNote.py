from Credentials import Root as rootCreds
from mysql.connector import connect

def start():
    connectDB()

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
    print(f"Welcome back, {mail}!")
    password = input("Enter your password to log in to your account:")
    query = "SELECT passkey FROM mynote_users where id = '{}'".format(mail)
    mnCursor.execute(query)
    gotPass = mnCursor.fetchall()[0][0]
    if gotPass==password:
        loginStatusUpdateQuery = "UPDATE db_mynote.mynote_users t SET t.login_status = 1 WHERE t.id LIKE '{}' ESCAPE '#' " \
                                 "AND t.passkey LIKE '{}' ESCAPE '#' AND t.login_status = 0;".format(mail,password)
        mnCursor.execute(loginStatusUpdateQuery)
        connector.commit()
        print("Bingo! You have successfully logged in to your account!")
    else:
        print("Wrong Password!")

def logout(mail):
    loginStatusUpdateQuery = "UPDATE db_mynote.mynote_users t SET t.login_status = 0 WHERE t.id LIKE '{}' ESCAPE '#' AND t.login_status = 1;".format(mail)
    mnCursor.execute(loginStatusUpdateQuery)
    connector.commit()
    print("Bingo! You have successfully logged out from your account!")


def register(mail):
    print(f"Welcome to the registration process, {mail}!")
    password = input("Enter your password:")
    query = "INSERT INTO db_mynote.mynote_users (id, passkey) VALUES ('{}', '{}')".format(mail, password)
    mnCursor.execute(query)
    connector.commit()
    print(f"User Registration is: {'Successful' if verification(mail) else 'Failed'}")

if __name__ == "__main__":
    """Landing Page"""
    # Starting Appplication
    start()


    # user = input("Enter Your Name: ")
    # print(f"Hello, {user}! Welcome to MyNote.")
    # umail = input("Enter your mail id please:")

    login('asdadc@bca.com') if(verification('asdadc@bca.com')) else register('asdadc@bca.com')
    logout('asdadc@bca.com')
    # print(verification('abc@bca.com'))
    # print(verification('asdadc@bca.com'))
    # register('asdadc@bca.com')
    # login('asdadc@bca.com')

