# SQLApp-HospitalSystem

### General Functionality

At Login, the user is prompted for credentials for a different level of authority over the database. When typing in the correct credentials, user will be directed to the corresponding menu view with options for each user type:

- Patients can view their appointments, their own personal info, and their assigned doctor.
- Doctors can view, delete, add, and edit Patients’ info, and view their own schedule and patients. They cannot add or delete another doctor.
- Manager has master control over the Database Management System (DBSM). This user can delete or add any patients or doctors they want.

A key point is the Trigger for deleting a user's information. In this database, a patient’s ID (pid) or doctor’s ID (did) is in multiple other tables as Foreign Keys. Now due to this tight requirement that these fields to not be NULL, it is impossible to delete a patient or doctor from the database unless deleting them from other tables where they are Foreign keys. So, the trigger did just that. When deleting patients or doctors, the process is automated and the programmers don’t have to go through the process of using DELETE operations on ALL of those tables. They only need to call DELETE on the Patient or Doctor that needs to be deleted.

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

### ER Diagramm
![](https://github.com/akurbanovv/SQLApp-HospitalSystem/blob/master/ER%20diagram.png)

### Relational table

![](https://github.com/akurbanovv/SQLApp-HospitalSystem/blob/master/Relational%20table.png)

### Objective and Learning Outcome

After this project, anyone of us should be able to understand real-life application of database design. The learning outcome which we have achieved is to be able to:

1. Design and plan a database with the specific perspectives of the users in mind.
2. Understand the constraints and requirements when using MySQL with Python or Java
3. Divide and conquer the workload, which demonstrates our thorough understanding of what needs to be done.
4. Implement complex SQL queries like Triggers to prevent certain failures from SQL DELETE queries.
5. Apply what we learned in class to a real-life scenario.

Given the time constraint that we have, and the 11-hour difference between team members, it was indeed challenging. We could have implemented another user, Staff, which encapsulates nurses, receptionists, etc. Another implementation would be Departments within a hospital. When a Patient is identified to have certain needs, we could assign them to a department, which would automatically assign the available doctor for that appointment time and the nurse. In brief, we would like to expand and approach real-life scenarios if we had more time.

Otherwise, we do not think that we would have done much differently. We definitely chose a topic that was not too familiar to us, thus giving us the most potential to learn. We also chose a complex enough structure to work with. With the target to learn in mind, I think we have achieved what we came for in such a time and environment constraint.
