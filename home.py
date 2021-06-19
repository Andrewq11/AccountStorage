import PySimpleGUI as sg
from addAcc import addAccount, titleFnt
import db
from show import hidePass, displayPass
import random


def mainGUI(id):

    # Checking if passwords should be hidden on home screen or not
    if id == 0:
        lays = hidePass()
    else:
        lays = displayPass()


    # Getting name of user
    userInfo = db.selectAcc_user()
    name = userInfo[0][1]


    # Checking if no accounts are present in the db
    if lays == ([], [], [], []):
        introText = "Add an Account to Get Started!"
        w = 145
        h = 0
        titleFnt = 'Arial 18 bold'
    

    # Various quotes which will display by random if at least 1 account in db
    else:
        j = random.randrange(0, 4)
        if j == 0:
            introText = """Protip: Avoid naming your password 'password'
                                                                  - Andy"""
            titleFnt = 'Arial 13 bold'
            w = 150
            h = 0

        elif j == 1:
            introText = """Treat your password like your toothbrush. Don't let anybody 
            else use it, and get a new one every six months.
                                                                            - Clifford Stole"""
            titleFnt = 'Arial 13 bold'
            w = 90
            h = 0
        
        elif j == 2:
            introText = """Choosing a hard-to-guess, but easy-to-remember password is important!
                                                                                             - Kevin Mitnick"""
            titleFnt = 'Arial 13 bold'
            w = 55
            h = 0

        elif j == 3:
            introText = """My brain's just full of passwords.
                                             - Karl Pilkington"""
            titleFnt = 'Arial 13 bold'
            w = 210
            h = 0
        else: 
            introText= """Truthfully, I built this because I can never remember my email passwords
                                                                                             - Andy """
            titleFnt = 'Arial 13 bold'
            w = 50
            h = 0
    

    # Creating layout for each account type
    accountInfo = [[sg.Frame('Social Media Accounts', font= 'Arial 11 underline', 
        layout=lays[0], border_width= 0)],
        [sg.Sizer(0, 10)],
        [sg.Frame('Email Accounts', font= 'Arial 11 underline', layout=lays[1], border_width= 0)],
        [sg.Sizer(0, 10)],
        [sg.Frame('Work/School Accounts', font= 'Arial 11 underline', layout=lays[2], border_width= 0)],
        [sg.Sizer(0, 10)],
        [sg.Frame('Misc. Accounts', font= 'Arial 11 underline', layout=lays[3], border_width= 0)],]
    

    # Creating layout for GUI which contains above layout in Column
    layout = [[sg.Sizer(w, h), sg.Text(introText, font= titleFnt)],
        [sg.Sizer(50, 40), sg.Button("Hide/Show", key="hide"), sg.Sizer(455, 10),
        sg.Button(button_text= 'Add Account', key= 'addAcc')],
        [sg.Sizer(0, 20)],
        [sg.Sizer(20, 0), sg.Column(accountInfo, size= (620, 300), scrollable= True,)],
        [sg.Sizer(540, 60), sg.Button('Confirm Delete', key='DelButton')]],


    window = sg.Window(name + "'s " + "Account Holder", layout, margins=(30, 30))
    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
            break
        
        # Takes user to addAcc screen on press
        elif event == 'addAcc':
            window.close()
            addAccount()
            window.close()
            mainGUI(id)
            break
        
        # Toggles hide and show mode for passwords
        elif event == 'hide':
            window.close()
            if id == 0:
                id = 1
                mainGUI(id)
            elif id == 1:
                id = 0
                mainGUI(id)


        elif event == 'DelButton':
            # When Confirm Delete pressed, will loop thru all keys in main GUI and
            # add every key after the first two (first two are hide/show & addAcc
            # button). After this, the last key of the GUI will be popped off as
            # this will be assigned to Confirm Delete button. Then, a for loop
            # will loop thru all remaining keys in keysKeys (corresponds to all 
            # delete checkboxes) and if they are True (checked), that row will
            # be deleted from the db. 
            keysKeys = []
            keyCheck = []
            i = 0
            for key in window.AllKeysDict:
                if i == 0 or i == 1:
                    i = i + 1
                    continue
                else:
                    keysKeys.append(key)
                    i = i + 1
                    
            keysKeys.pop(-1)

            # Checking if user pressed 'Confirm Delete' but did not select
            # anything to delete
            for delete in keysKeys:
                if values[delete] == False:
                    keyCheck.append(delete)
                
                if len(keyCheck) == len(keysKeys):
                    sg.popup("Hmm doesn't seem like you've selected an account to delete!")
                    continue
            
            # Deleting accounts as selected by user
            if len(keyCheck) != len(keysKeys):
                for delete in keysKeys:
                    if values[delete] == True:
                        delete = delete.replace('Del', '')
                        delete = int(delete)
                        db.deleteAcc(delete)
            
                window.close()
                mainGUI(id)
            
           

    window.close()
