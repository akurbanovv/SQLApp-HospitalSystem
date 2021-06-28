# SQLApp-HospitalSystem

Application’s main purpose is to facilitate data retrieval for a **hospital management system**. The main users are doctors and patients, with the addition of a Manager.

### General Functionality

At Login, the user is prompted for credentials for a different level of authority over the database. When typing in the correct credentials, user will be directed to the corresponding menu view with options for each user type:

- Patients can view their appointments, their own personal info, and their assigned doctor.
- Doctors can view, delete, add, and edit Patients’ info, and view their own schedule and patients. They cannot add or delete another doctor.
- Manager has master control over the Database Management System (DBSM). This user can delete or add any patients or doctors they want.

A key point that Hung is very proud of is the Trigger for deleting a user's information. In this database, a patient’s ID (pid) or doctor’s ID (did) is in multiple other tables as Foreign Keys. Now due to this tight requirement that these fields to not be NULL, it is impossible to delete a patient or doctor from the database unless deleting them from other tables where they are Foreign keys. So, the trigger did just that. When deleting patients or doctors, the process is automated and the programmers don’t have to go through the process of using DELETE operations on ALL of those tables. They only need to call DELETE on the Patient or Doctor that needs to be deleted.

### Data Requirement

- Patient: pid (PK), pswd, name, age, gender, medication 
- Doctor: did (PK), pswd, name, age, gender, address 
- Has: doctor_id, patient_id (PK)(FK), nurse_id 
- Appointments: Date, Time, doctor_id (FK), patient_id (FK), description 
- Manager: mgid (PK), pswd, name

### Assumptions

- One patient has only one doctor to care for them
- Doctors can care for multiple patients.
- Appointments of a doctor cannot be on the same time i.e. Same (Date, Time) needs different doctors.

![](https://github.com/akurbanovv/SQLApp-HospitalSystem/blob/master/ER%20diagram.png)
