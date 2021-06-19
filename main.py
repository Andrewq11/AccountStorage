from home import mainGUI
import PySimpleGUI as sg
from db import accStore_user, encrypt_pass, selectAcc_user, decrypt_pass,\
    generate_key, create_DB, create_DB_user, del_table, del_table_user

titleFnt = 'Arial 18 bold'
listFnt = 'Arial 9'
regFnt = 'Arial 11'

# Checking if an account has ever been set up before.
# If not, will create tables for account info and user info, and generate
# encryption key for passwords
try:
    dbInitial = selectAcc_user()
except:
    create_DB()
    create_DB_user()
    generate_key()
    dbInitial = selectAcc_user()


# GUI layout if user has never been created. Adding user info to db.
if dbInitial == []:

    layout = [  [sg.Sizer(25, 0), sg.Text('Please Input Your Name & Password', font= titleFnt),
                sg.Sizer(25, 0)],

                [sg.Sizer(55, 60), sg.Text('First Name:', font= regFnt), \
                sg.InputText(key='firstName', size= (20, 60))],

                [sg.Sizer(60, 60), sg.Text('Password:', font= regFnt), \
                sg.InputText(key='password', size= (20, 60))],
                
                [sg.Sizer(30, 60), sg.Text('Password Hint:', font= regFnt), \
                sg.InputText(key='hintPass', size= (40, 80))],
                
                [sg.Button('Create Account', key= 'createAcc')]]


    window = sg.Window("Welcome to Your Personal Account Holder", layout, margins=(30, 30))
    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
            break

        # Retrieving user input and storing in userinfo db
        elif event == "createAcc":
            name = values.get('firstName')
            password = values.get('password')
            password = encrypt_pass(password)
            passHint = values.get('hintPass')

            accStore_user(name, password, passHint)
            
            window.close()
            mainGUI(0)
            break

    window.close()

# GUI layout if user has already created an account. Authentication screen.
else:
    # Retrieving stored password and password hint in db
    dbInitial = selectAcc_user()
    dbInitial_pass = decrypt_pass(dbInitial[0][2])
    passHint = dbInitial[0][3]

    layout = [  [sg.Sizer(25, 0), sg.Text('Please Input Your Password', font= titleFnt),
                sg.Sizer(25, 0)],

                [sg.Sizer(50, 60), sg.Text('Password:', font= regFnt), \
                sg.InputText(key='authPass', size= (20, 60))],
                
                [sg.Button('Reset Account', key= 'reset'), sg.Sizer(180, 0), 
                sg.Button('Authenticate', key= 'auth')]]


    i = 0
    j = 0
    window = sg.Window("User Authentication", layout, margins=(30, 30))
    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
            break
        # Checking if the user inputted pass is the same as the one stored in db
        elif event == "auth":
            authPass = values.get('authPass')
            authPass = authPass.strip()

        # If so, user is granted access to home screen
            if authPass == dbInitial_pass:
                window.close()
                mainGUI(0)
                break
        
        # If not, user is prompted to enter password again. If incorrect another
        # time, password hint will display in pop up.
            else:
                i = i + 1
                window['authPass']('')
                if i >= 3:
                    sg.Popup("Hint: " + passHint, keep_on_top= True)
                else:
                    sg.popup("Hmm that's not the correct password. Try again!",\
                        keep_on_top= True)
                    continue
            
        # If user cannot remember account details and must delete account,
        # reset button will do so. 
        elif event == 'reset':
            j = j + 1
            # Account deletion on second consecutive press of 'Reset'
            if j == 2:
                del_table()
                del_table_user()
                open('key.key', 'w').close()
                window.close()
                sg.popup("Account deleted. Please restart the application to create a new account!")
                break

            # Pop up message on first press of reset
            else:
                sg.Popup("""Are you sure you want to reset your account? You will lose \
                    all of your previously stored information. 

If so, please click 'Reset Account' again.""")

    window.close()