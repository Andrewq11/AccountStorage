import db
import PySimpleGUI as sg

# File contains functions for fetching stored accounts and building the GUI
# layout based on whether the passwords are in show or hide mode. Default mode
# is hide.

def displayPass():
    # Grabbing rows from DB, adding rows to lists depending on which type of account
    # the username/password is for
    rows = db.selectAcc()

    socMedAccs = []
    emailAccs = []
    workAccs = []
    miscAccs = []
    
    # Adding accounts to corresponding account type lists
    for row in rows:
        if row[4] == 'Social Media':
            socMedAccs.append(row)
        
        elif row[4] == 'Email':
            emailAccs.append(row)

        elif row[4] == 'Work/School':
            workAccs.append(row)
        
        else:
            miscAccs.append(row)


    laySocMed = []
    layEmail = []
    layWork = []
    layMisc = []

    # Taking username of various account types & adding to layout for display.
    # Using the IDs of each row in db to assign key to "Delete Account" button 
    # so when deleting, there is something that can indicate to db which is the 
    # correct row to delete.
    for row in socMedAccs:
        decryptedPassword = db.decrypt_pass(row[2])
        laySocMed.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (225, 25)), 
        sg.Column([[sg.Text("          " + decryptedPassword)]], size= (200, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])


    for row in emailAccs:
        decryptedPassword = db.decrypt_pass(row[2])
        layEmail.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (225, 25)), 
        sg.Column([[sg.Text("          " + decryptedPassword)]], size= (200, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])

    for row in workAccs:
        decryptedPassword = db.decrypt_pass(row[2])
        layWork.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (225, 25)), 
        sg.Column([[sg.Text("          " + decryptedPassword)]], size= (200, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])

    for row in miscAccs:
        decryptedPassword = db.decrypt_pass(row[2])
        layMisc.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (225, 25)), 
        sg.Column([[sg.Text("          " + decryptedPassword)]], size= (200, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])

    return laySocMed, layEmail, layWork, layMisc


def hidePass():
    # Grabbing rows from DB, adding rows to lists depending on which type of account
    # the username/password is for
    rows = db.selectAcc()

    socMedAccs = []
    emailAccs = []
    workAccs = []
    miscAccs = []
    for row in rows:
        if row[4] == 'Social Media':
            socMedAccs.append(row)
        
        elif row[4] == 'Email':
            emailAccs.append(row)

        elif row[4] == 'Work/School':
            workAccs.append(row)
        
        else:
            miscAccs.append(row)


    laySocMed = []
    layEmail = []
    layWork = []
    layMisc = []

    # Taking username of various account types & adding to layout for display
    # Using the IDs of each row to assign key to so when deleting, there is
    # something that can indicate which is the correct row to delete.
    # Only difference is the password can is hidden in this mode.
    for row in socMedAccs:
        laySocMed.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (250, 25)), 
        sg.Column([[sg.Text("          **********")]], size= (170, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])


    for row in emailAccs:
        layEmail.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (250, 25)), 
        sg.Column([[sg.Text("          **********")]], size= (170, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])


    for row in workAccs:
        layWork.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (250, 25)), 
        sg.Column([[sg.Text("          **********")]], size= (170, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])

    for row in miscAccs:
        layMisc.append([sg.Column([[sg.Text(">  " + row[1] + " (" + row[3] + ")")]], size= (250, 25)), 
        sg.Column([[sg.Text("          **********")]], size= (170, 25)), 
        sg.Sizer(30, 0), sg.Checkbox('Delete Account', key='Del ' + str(row[0]))])

    return laySocMed, layEmail, layWork, layMisc