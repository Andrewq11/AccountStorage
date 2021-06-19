import PySimpleGUI as sg
import db


titleFnt = 'Arial 18 bold'
listFnt = 'Arial 9'
regFnt = 'Arial 11'

# Function to create GUI for account storage page (adding account to db)
def addAccount():

    # Vals for account classification type
    vals = ['Social Media', 'Email', 'Work/School', 'Misc.']

    # Layout for GUI
    layout = [[sg.Sizer(25, 0), sg.Text('Add an Account for Storage', font= titleFnt),
            sg.Sizer(25, 0)],

            [sg.Sizer(0, 20)],

            [sg.Sizer(55, 60), sg.Text('Type of Account:', font= regFnt), \
                sg.Listbox(values= vals, key= 'accType', font= listFnt),],

            [sg.Sizer(50, 60), sg.Text('Username/Email:', font= regFnt), \
                sg.InputText(key='accUser', size= (20, 60))],
            
            [sg.Sizer(104, 60), sg.Text('Platform:', font= regFnt), \
                sg.InputText(key='accPlat', size= (20, 60))],
                
            [sg.Sizer(91, 60), sg.Text('Password:', font= regFnt), \
                sg.InputText(key='accPass', size= (20, 60))],
                
            [sg.Sizer(20, 60), sg.Button('Back', key= 'backBut'), sg.Sizer(210, 0),
                sg.Button('Store Account', key= 'accStore')]]


    window = sg.Window("Add Account", layout, margins=(40,40))
    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
            break
        elif event == 'backBut':
            break

        # Checking for fields which are empty on accStore press
        elif event == 'accStore':
            if values.get('accUser') == '' or values.get('accPass') == '' \
                or values.get('accType') == [] or values.get('accPlat') == '':

                sg.popup("Please make sure all fields are filled out! Try again.")
                continue
            
            # Retrieving user inputted values, encrypting password, and storing
            # in accounts db.
            while True: 
                try:
                    type = values.get('accType')[0]
                    username = values.get('accUser')
                    password = values.get('accPass')
                    platform = values.get('accPlat')
                    
                    # Encrypting the password before storing in db
                    password = db.encrypt_pass(password)



                    # Adding info to db
                    db.accStore(username, password, platform, type)

                    # Resetting input fields for multiple entries
                    window['accUser']('')
                    window['accPass']('')
                    window['accPlat']('')
                    break

                except:
                    print("Error when adding account to db")
                    break

    window.close()