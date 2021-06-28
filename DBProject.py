import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="kodekode",
  database="dbfinal"
)

mycursor = mydb.cursor()

DOCTOR = "Doctor"
HAS = "Has"
PATIENT = "Patient"

def init_mydb():
    mycursor.execute("CREATE DATABASE dbfinal")
    mycursor.execute("CREATE TABLE Doctor (did int PRIMARY KEY, dname varchar(50))")
    mycursor.execute("CREATE TABLE Patient (pid int PRIMARY KEY, pname varchar(50), page int)")
    mycursor.execute("CREATE TABLE Has (did int, pid int, PRIMARY KEY (did, pid), FOREIGN KEY (did) REFERENCES Doctor (did), FOREIGN KEY (pid) REFERENCES Patient (pid) )")
    mycursor.execute("CREATE TABLE Appointments (App_date DATE NOT NULL, App_time TIME NOT NULL, pid int, did int, memo VARCHAR(255), PRIMARY KEY (App_date, App_time, did), FOREIGN KEY (pid) REFERENCES Patient(pid), FOREIGN KEY (did) REFERENCES Doctor(did))")

    mycursor.execute("INSERT INTO Doctor VALUES (10, 'Avicenna')")
    mycursor.execute("INSERT INTO Doctor VALUES (20, 'Anthony Fauci')")
    mycursor.execute("INSERT INTO Doctor VALUES (30, 'Hippocrates')")
    mycursor.execute("INSERT INTO Doctor VALUES (40, 'Sigmund Freud')")

    mycursor.execute("INSERT INTO Patient VALUES(110, 'Akhmad', 23)")
    mycursor.execute("INSERT INTO Patient VALUES(120, 'Hung', 21)")
    mycursor.execute("INSERT INTO Patient VALUES(130, 'Daria', 49)")
    mycursor.execute("INSERT INTO Patient VALUES(140, 'Sam Ruben', 13)")
    mycursor.execute("INSERT INTO Patient VALUES(150, 'Michael Scott', 3)")

    mycursor.execute("INSERT INTO Has VALUES(10, 110)")
    mycursor.execute("INSERT INTO Has VALUES(10, 120)")
    mycursor.execute("INSERT INTO Has VALUES(10, 130)")
    mycursor.execute("INSERT INTO Has VALUES(10, 140)")
    mycursor.execute("INSERT INTO Has VALUES(20, 110)")
    mycursor.execute("INSERT INTO Has VALUES(20, 120)")
    mycursor.execute("INSERT INTO Has VALUES(20, 130)")
    mycursor.execute("INSERT INTO Has VALUES(30, 120)")
    mycursor.execute("INSERT INTO Has VALUES(30, 130)")
    mycursor.execute("INSERT INTO Has VALUES(40, 140)")

    mycursor.execute("INSERT INTO Appointments VALUES ('2020.05.20', '19:30:00', '120', '10', 'Regular Checkup')")
    mycursor.execute("INSERT INTO Appointments VALUES ('2020.05.7', '9:30:00', '130', '10', 'High Blood Pressure')")
    mycursor.execute("INSERT INTO Appointments VALUES ('2020.05.6', '20:45:00', '110', '30', 'Regular Checkup')")
    mycursor.execute("INSERT INTO Appointments VALUES ('2020.05.6', '12:30:00', '130', '30', 'Fever, cough')")
    mycursor.execute("INSERT INTO Appointments VALUES ('2020.05.20', '19:30:00', '120', '30', 'Past Drug-used')")


    mycursor.execute("DELIMITER $$ CREATE Trigger before_delete_patient BEFORE DELETE ON Patient FOR EACH ROW BEGIN DELETE FROM Appointments WHERE pid = Old.pid; DELETE FROM Has WHERE pid = Old.pid;  END$$ DELIMITER")

    mycursor.execute("DELIMITER $$ CREATE Trigger before_delete_doctor BEFORE DELETE ON Doctor FOR EACH ROW BEGIN DELETE FROM Appointments WHERE did = Old.did; DELETE FROM Has WHERE did = Old.did; END$$ DELIMITER")

    mydb.commit()

def is_in_table(did, pid, table_name):
    if (table_name == PATIENT):
        mycursor.execute("SELECT count(*) FROM %s C WHERE C.pid = %s" % (table_name, pid))
    if (table_name == DOCTOR):
        mycursor.execute("SELECT count(*) FROM %s S WHERE S.did = %s" % (table_name, did))
    if (table_name == HAS):
        if (did is not None and pid is None):
            mycursor.execute("SELECT count(*) FROM %s E WHERE E.did = %s" % (table_name, did))
        elif (pid is not None and did is None):
            mycursor.execute("SELECT count(*) FROM %s E WHERE E.did = %s" % (table_name, pid))
        else:
            mycursor.execute("SELECT count(*) FROM %s E WHERE E.did = %s AND E.pid = %s" % (table_name, did, pid))

    retrn = mycursor.fetchall()
    return retrn[0][0] > 0

def list_all_patients():
    mycursor.execute("SELECT * FROM Patient")
    list = mycursor.fetchall()
    for patient in list: print(patient)

def list_all_doctors():
    mycursor.execute("SELECT * FROM Doctor")
    list = mycursor.fetchall()
    for doctor in list: print(doctor)

def list_all_has():
    mycursor.execute("SELECT * FROM Has")
    list = mycursor.fetchall()
    for entity in list: print(entity)

def list_my_patients(did):
    mycursor.execute("SELECT P.pid, P.pname, P.page FROM Patient P, Has H WHERE H.did=%s AND H.pid=P.pid" % did)
    list = mycursor.fetchall()
    for patient in list: print(patient)

def assign_patient(did):
    pid_to_enr = int(input("Please provide ID of the patient you want to add: \n--> "))

    if (is_in_table(did, pid_to_enr, HAS)):
        print("You already have this patient assigned to you!")
        return

    while (not is_in_table(None, pid_to_enr, PATIENT)):
        pid_to_enr = int(input("There is no patient with provided ID. Please provide a proper ID: \n--> "))

    mycursor.execute("INSERT INTO Has VALUES(%s, %s)" % (did, pid_to_enr))
    mydb.commit()
    print("You successfully added a patient into your list!")

def unassign_patient(did):
    pid_to_rmv = int(input("Please provide an ID of the patient you want to unassign: \n--> "))

    while(not is_in_table(None, pid_to_rmv, PATIENT) or not is_in_table(did, pid_to_rmv, HAS)):
        if (not is_in_table(None, pid_to_rmv, PATIENT)):
            pid_to_rmv = str(input("There is no patient with the provided ID.\n"
                                 + "Please provide a proper patient ID: \n--> "))

        elif (not is_in_table(did, pid_to_rmv, HAS)):
            pid_to_rmv = str(input("This patient is not assigned to you!\n"
                              + "Please provide a proper patient ID: \n--> "))

    mycursor.execute("DELETE FROM Has H WHERE H.did = %s AND H.pid = %s" % (did, pid_to_rmv))
    mydb.commit()
    print("You successfully unassigned the patient!")

def search_patient():
    pname = str(input("Please provide patient's name (or name's substring): \n--> "))
    mycursor.execute("SELECT P.pid, P.pname, P.page FROM PATIENT P WHERE P.pname LIKE"
    + "'" + pname + "%'")
    courses = mycursor.fetchall()
    for record in courses: print(record)

def add_doctor():
    dname = str(input("Please input doctor's name: \n--> "))
    did = str(input("Please input doctor's unique ID: \n--> "))

    while(is_in_table(did, None, DOCTOR)):
        did = str(input("This ID is taken. Provide a proper ID: \n--> "))

    #INSERT INTO Doctor VALUES (10, 'Avicenna')
    mycursor.execute("INSERT INTO Doctor VALUES (%s, '%s')" % (did, dname))
    mydb.commit()

    print("You successfully added a new doctor into the database!")

def add_patient():
    pname = str(input("Please input patient's name: \n--> "))
    page = str(input("Please input patient's age: \n--> "))
    pid = str(input("Please input patient's unique ID: \n--> "))

    while(is_in_table(None, pid, PATIENT)):
        pid = str(input("This ID is taken. Provide a proper ID: \n--> "))

    mycursor.execute("INSERT INTO Patient VALUES (%s, '%s', %s)" % (pid, pname, page))
    mydb.commit()

    print("You successfully added a new patient into the database!")

def del_patient():
    pid_to_del = str(input("Please provide an ID of the patient you want to delete: \n--> "))

    while(not is_in_table(None, pid_to_del, PATIENT)):
        pid_to_del = str(input("There is no patient with the provided ID.\n"+
                               "Please provide a proper patient ID: \n--> "))

    mycursor.execute("DELETE FROM Patient P WHERE P.pid = %s" % pid_to_del)
    mydb.commit()
    print("You successfully deleted the patient!")

def del_doctor():
    did_to_del = str(input("Please provide an ID of the doctor you want to delete: \n--> "))

    while(not is_in_table(did_to_del, None, DOCTOR)):
        did_to_del = str(input("There is no doctor with the provided ID.\n"+
                               "Please provide a proper patient ID: \n--> "))

    mycursor.execute("DELETE FROM Doctor D WHERE D.did = %s" % did_to_del)
    mydb.commit()
    print("You successfully deleted the doctor!")

def show_my_doctor(pid):
    mycursor.execute("SELECT D.dname FROM Doctor D, Has H WHERE H.pid = %s AND D.did=H.did" % pid)
    list = mycursor.fetchall()
    for patient in list: print(patient)

def show_my_records(pid):
    mycursor.execute("SELECT P.pid, P.pname, P.page FROM Patient P WHERE P.pid=%s" % pid)
    list = mycursor.fetchall()
    for patient in list: print(patient)

def doctor_menu(id):
    DOCTOR_INPUTS = ['P', 'MP', 'AP', 'UP', 'S', 'logout', 'exit']
    print("------------------------Doctor Menu-------------------------\n"+
          "You are in the doctor menu! You have the following \n"+
          "commands avaiablbe:\n\n"+
          "P – lists all patients in the hospital.\n"+
          "MP – lists all patients assigned to you.\n"+
          "AP – assigns a new patient to your list.\n"
          "UP – unassigns a patient from your list.\n"
          "S – search patients based on substring of their name.\n\n"
          "Input 'logout' if you want to go back to the main menu, or \n"+
          "'exit' if you want to end your session. ")

    cmd = ""
    while (cmd != 'logout'):
        cmd = str(input("--> "))
        if (cmd in DOCTOR_INPUTS):
            if (cmd == "P"):
                list_all_patients()
            elif (cmd == "MP"):
                list_my_patients(id)
            elif (cmd == "AP"):
                assign_patient(id)
            elif (cmd == "UP"):
                unassign_patient(id)
            elif (cmd == "S"):
                search_patient()
            elif (cmd == "exit"):
                sys.exit(42)
        else:
            print("Wrong menu call! Read menu specifications!")

    print("You are exiting the Doctor Menu. Have a good day!")

def manager_menu():
    MANAGER_INPUTS = ['AP', 'AD', 'DP', 'DD', 'LP', 'LD', 'LH', 'logout', 'exit']

    print("----------------------DB Manager Menu-----------------------\n"+
          "You are in the database manager menu! You have the following\n"+
          "commands avaiablbe:\n\n"+
          "AP – add a new patient into the Patient database.\n"+
          "AD – add a new doctor into the Doctor database.\n"+
          "DP – remove a patient from the Patient database.\n"+
          "DD – remove a doctor from the Doctor database.\n"+
          "LP – list all patients in the Patient database.\n"+
          "LD – list all doctors in the Doctor database.\n"+
          "LH – list all entities in the Has database.\n\n"+
          "Input 'logout' if you want to go back to the main menu, or \n"+
          "'exit' if you want to end your session. ")

    cmd = ""
    while (cmd != 'logout'):
        cmd = str(input("--> "))
        if (cmd in MANAGER_INPUTS):
            if (cmd == "AP"):
                add_patient()
            elif (cmd == "AD"):
                add_doctor()
            elif (cmd == "DP"):
                del_patient()
            elif (cmd == "DD"):
                del_doctor()
            elif (cmd == "LP"):
                list_all_patients()
            elif (cmd == "LD"):
                list_all_doctors()
            elif(cmd == "LH"):
                list_all_has()
            elif (cmd == "exit"):
                sys.exit(42)
        else:
            print("Wrong menu call! Read menu specifications!")

    print("You are exiting the DB Manager menu. Have a good day!")

def patient_menu(id):
    MANAGER_INPUTS = ['MD', 'MR', 'logout', 'exit']

    print("----------------------Patient Menu-----------------------\n"+
          "You are in the patient menu! You have the following\n"+
          "commands avaiablbe:\n\n"+
          "MD – allows you to view your doctor.\n"+
          "MR – allows you to view your own medical records\n\n"+
          "Input 'logout' if you want to go back to the main menu, or \n"+
          "'exit' if you want to end your session. ")

    cmd = ""
    while (cmd != 'logout'):
        cmd = str(input("--> "))
        if (cmd in MANAGER_INPUTS):
            if (cmd == "MD"):
                show_my_doctor(id)
            elif (cmd == "MR"):
                show_my_records(id)
            elif (cmd == "exit"):
                sys.exit(42)
        else:
            print("Wrong menu call! Read menu specifications!")

    print("You are exiting the Patient menu. Have a good day!")

def main():
    # init_mydb() # comment out after running it the first time.

    while (True):
        utype = "A"

        print("------------------------Main Menu---------------------------\n"+
              "Welcome to the Hospital Management System!\n\n"+
              "Created by Hung, Daria and Akhmad!\n")

        while (utype not in "DMP"):
            utype = str(input("Please input D if you are a doctor, P if you are a patient\n"+
              "or M if you are a manager:\n--> "))

        id = str(input("Please provide your ID to log in: \n--> "))

        if (utype == "D"):
            doctor_menu(id)
        if (utype == "M"):
            manager_menu()
        if (utype == "P"):
            patient_menu(id)


if __name__ == "__main__":
    main()
