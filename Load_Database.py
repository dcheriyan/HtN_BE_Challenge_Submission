import sqlite3
import json

#Load data from a local file for now
data_file = open("HTN_2023_BE_Challenge_Data.json")

starting_data = json.load(data_file)

if __name__ == '__main__':
    #Creates a database in cwd
    conn = sqlite3.connect("HTN_BE_Challenge.db")
    #TODO make sure connection was sucessful

    curs = conn.cursor()

    #Drop Tables for debugging
    #curs.execute("DROP TABLE Personal_Info")
    #curs.execute("DROP TABLE User_Skills")

    #Table A: | User_id	(primary key) | Name | Company | email | phone |
    #Assume Names, Companies, Emails, Phone < 255 char
    curs.execute("CREATE TABLE Personal_Info( User_id int NOT NULL PRIMARY KEY, Name varchar(255), Company varchar(255), Email varchar(255), Phone varchar(255) )")

    #Table B: | Skill_id (primary_key) | User_id | Skill_Name | Rating |
    #Assume Skill_Name < 255 char
    curs.execute("CREATE TABLE User_Skills(Skill_id int NOT NULL PRIMARY KEY, User_id int, Skill_name varchar(255), Rating int)")

    User_id = 0
    Skill_id = 0
    Personal_Info_Instruction_Template = "INSERT INTO Personal_Info VALUES ( "
    User_Skills_Instruction_Template = "INSERT INTO User_Skills VALUES ( "
    Name_Value = "Temp"             # Temp value to define it as a string
    Company_Value = "Temp"          # Temp value to define it as a string
    Email_Value = "Temp"            # Temp value to define it as a string
    Phone_Value = "Temp"            # Temp value to define it as a string
    Skill_Name_Value = "Temp"       # Temp value to define it as a string
    Rating_Value = -1               # Temp value to define it as a int

    Instruction_String = "Temp"     # Temp value to define it as a string

    for person in starting_data:
        Name_Value = person["name"]
        Company_Value = person["company"]
        Email_Value = person["email"]
        Phone_Value = person["phone"]

        for Skills in person["skills"]:
            Skill_Name_Value = Skills["skill"]
            Rating_Value = Skills["rating"]

            Instruction_String = User_Skills_Instruction_Template + str(Skill_id) + ", " + str(User_id) + ", '" + Skill_Name_Value + "', " + str(Rating_Value) + ")"
            curs.execute(Instruction_String)
            conn.commit()
            Skill_id = Skill_id + 1


        #Assuming all fields defined for every user (i.e. no user missing an email, or if they don't have one there is a placeholder in the json)
        Instruction_String = Personal_Info_Instruction_Template + str(User_id) + ", '" + Name_Value + "', '" + Company_Value + "', '"+ Email_Value + "', '"+ Phone_Value + "')"
        curs.execute(Instruction_String)
        conn.commit()
        User_id  = User_id + 1

    print("Finished Setting up Tables")
